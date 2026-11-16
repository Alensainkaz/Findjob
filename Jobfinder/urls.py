from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from resume import seo

urlpatterns = [
    path('favicon.ico', seo.favicon),
    path('robots.txt', seo.robots_txt),
    path('site.webmanifest', seo.webmanifest),
    path('sitemap.xml', sitemap, {'sitemaps': seo.sitemaps}, name='sitemap'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('', include('resume.urls')),
    path('', include('users.urls')),
    path('cart/', include('cart.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)