import os
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from django.templatetags.static import static
from django.urls import reverse_lazy
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
# DEBUG включается только явно: DEBUG=True в .env (локально)
DEBUG = os.getenv('DEBUG', 'False').lower() in ('1', 'true', 'yes')

SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = 'django-insecure-local-dev-only-key-do-not-use-in-production'
    else:
        raise ImproperlyConfigured('SECRET_KEY environment variable is not set')

ALLOWED_HOSTS = ['www.findy-job.com', 'findy-job.com', '127.0.0.1', 'localhost', '.onrender.com', '.vercel.app']
CSRF_TRUSTED_ORIGINS = [
    'https://findy-job.com',
    'https://www.findy-job.com',
    'https://*.onrender.com',
    'https://*.vercel.app',
]
# Vercel выставляет VERCEL=1 и в сборке, и во время работы функций
ON_VERCEL = bool(os.getenv('VERCEL'))

# Render терминирует HTTPS на прокси
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    # Начинаем с 1 часа; когда HTTPS стабильно работает — поднять до 31536000
    SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '3600'))

# Application
INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # staticfiles должен идти ДО cloudinary_storage: Cloudinary используется
    # только для media, и collectstatic должен быть стандартным
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'cloudinary_storage',
    'cloudinary',
    'users',
    'resume',
    'cart',
    'anymail',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Jobfinder.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'Jobfinder.context_processors.toasts',
                'Jobfinder.context_processors.vercel',
            ],
        },
    },
]

WSGI_APPLICATION = 'Jobfinder.wsgi.application'

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL', 'postgresql://alens@127.0.0.1:5433/jobfinder')
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
from django.utils.translation import gettext_lazy as _

LANGUAGE_CODE = 'ru'
LANGUAGES = [
    ('kk', _('Kazakh')),
    ('ru', _('Russian')),
    ('en', _('English')),
]
LOCALE_PATHS = [BASE_DIR / 'locale']
LANGUAGE_COOKIE_AGE = 60 * 60 * 24 * 365
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static & media files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

# STATICFILES_STORAGE / DEFAULT_FILE_STORAGE удалены в Django 5.1 и
# игнорируются — хранилища задаются только через STORAGES.
STORAGES = {
    'default': {
        # Cloudinary in production; local disk when Cloudinary isn't configured (local dev)
        'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage'
        if os.getenv('CLOUDINARY_CLOUD_NAME') else 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        # На Vercel collectstatic не запускается, поэтому без манифеста:
        # WhiteNoise отдаёт файлы прямо из static/ и папок приложений
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage' if ON_VERCEL
        else 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}
WHITENOISE_USE_FINDERS = ON_VERCEL
# django-cloudinary-storage 0.3.0 всё ещё читает это имя в своём collectstatic
STATICFILES_STORAGE = STORAGES['staticfiles']['BACKEND']

# Default primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'users.User'
LOGIN_URL = 'login_view'

# Почта: SMTP mail.ru, если задан пароль; иначе Brevo, если задан ключ;
# иначе (локальная разработка) письма печатаются в консоль runserver
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.mail.ru')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '465'))
EMAIL_USE_SSL = EMAIL_PORT == 465
EMAIL_USE_TLS = EMAIL_PORT == 587
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'findy-job.noreply@mail.ru')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_TIMEOUT = 15

if EMAIL_HOST_PASSWORD:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
elif os.getenv('BREVO_API_KEY'):
    EMAIL_BACKEND = 'anymail.backends.brevo.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ANYMAIL = {
    'BREVO_API_KEY': os.getenv('BREVO_API_KEY'),
}
# mail.ru принимает только письма, где From совпадает с ящиком авторизации
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL') or f'Findy-Job <{EMAIL_HOST_USER}>'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Пишем ошибки (включая traceback 500-х) в stdout — их видно в логах Render
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'root': {'handlers': ['console'], 'level': 'INFO'},
    'loggers': {
        'django': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
    },
}

# Admin theme (django-unfold) in the site's navy + teal palette
UNFOLD = {
    'SITE_TITLE': 'Findy-Job admin',
    'SITE_HEADER': 'Findy-Job',
    'SITE_SUBHEADER': 'Resume board',
    'SITE_URL': '/',
    'SITE_SYMBOL': 'work',
    'SITE_FAVICONS': [
        {'rel': 'icon', 'sizes': '32x32', 'type': 'image/png', 'href': lambda request: static('favicon-32x32.png')},
    ],
    'SHOW_HISTORY': True,
    'SHOW_VIEW_ON_SITE': True,
    'BORDER_RADIUS': '8px',
    'THEME': 'dark',  # match the site; hides the light/dark switcher
    'DASHBOARD_CALLBACK': 'Jobfinder.dashboard.dashboard_callback',
    'COLORS': {
        'base': {
            '50': 'oklch(98% .004 250)', '100': 'oklch(95.5% .008 250)', '200': 'oklch(91% .014 250)',
            '300': 'oklch(84% .022 250)', '400': 'oklch(68% .032 250)', '500': 'oklch(54% .038 250)',
            '600': 'oklch(44% .042 250)', '700': 'oklch(35% .045 250)', '800': 'oklch(27% .045 250)',
            '900': 'oklch(21% .042 250)', '950': 'oklch(16% .038 250)',
        },
        'primary': {
            '50': 'oklch(97.5% .03 170)', '100': 'oklch(94% .06 170)', '200': 'oklch(89% .1 170)',
            '300': 'oklch(85% .14 168)', '400': 'oklch(81% .16 167)', '500': 'oklch(73% .155 167)',
            '600': 'oklch(63% .135 168)', '700': 'oklch(53% .115 169)', '800': 'oklch(44% .095 170)',
            '900': 'oklch(37% .08 171)', '950': 'oklch(27% .06 172)',
        },
    },
    'SIDEBAR': {
        'show_search': True,
        'show_all_applications': False,
        'navigation': [
            {
                'title': 'Board',
                'items': [
                    {'title': 'Dashboard', 'icon': 'dashboard', 'link': reverse_lazy('admin:index')},
                    {'title': 'Resumes', 'icon': 'badge', 'link': reverse_lazy('admin:resume_resume_changelist')},
                    {'title': 'Saved lists', 'icon': 'bookmarks', 'link': reverse_lazy('admin:cart_cart_changelist')},
                ],
            },
            {
                'title': 'People',
                'items': [
                    {'title': 'Users', 'icon': 'group', 'link': reverse_lazy('admin:users_user_changelist')},
                    {'title': 'Email verification', 'icon': 'mark_email_read', 'link': reverse_lazy('admin:users_emailverificationtoken_changelist')},
                    {'title': 'Groups', 'icon': 'shield_person', 'link': reverse_lazy('admin:auth_group_changelist')},
                ],
            },
        ],
    },
}
