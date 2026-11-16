import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext as _
from django.views.decorators.http import require_GET, require_POST

from .forms import UserRegisterForm, UserLoginForm
from .models import User, EmailVerificationToken

logger = logging.getLogger(__name__)

PENDING_KEY = 'pending_user_id'


def _form_errors(form):
    """Serialize Django form errors for the Vue form components."""
    return {field: [str(e) for e in errs] for field, errs in form.errors.items()}


def _send_code(user, code):
    context = {'user': user, 'code': code, 'minutes': int(EmailVerificationToken.CODE_TTL.total_seconds() // 60)}
    send_mail(
        subject=_('%(code)s is your Findy-Job verification code') % {'code': code},
        message=render_to_string('users/email/verify_code.txt', context),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
        html_message=render_to_string('users/email/verify_code.html', context),
    )


def _start_verification(request, user):
    """Issue a code for `user`, email it and remember the user in the session."""
    token, _created = EmailVerificationToken.objects.get_or_create(user=user)
    code = token.issue_code()
    _send_code(user, code)
    request.session[PENDING_KEY] = user.pk


def _mask_email(email):
    name, _at, domain = email.partition('@')
    visible = name[:2] if len(name) > 2 else name[:1]
    return f'{visible}{"•" * max(1, len(name) - len(visible))}@{domain}'


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.GET.get('next', '')
            if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
                next_url = 'index'
            return redirect(next_url)
        if form.pending_user is not None:
            token = EmailVerificationToken.objects.filter(user=form.pending_user).first()
            try:
                if token is None or token.resend_available_in == 0:
                    _start_verification(request, form.pending_user)
                else:
                    request.session[PENDING_KEY] = form.pending_user.pk
            except Exception:
                logger.exception('Could not send verification code to %s', form.pending_user.email)
                form.add_error(None, _('We could not send the confirmation code. Please try again later.'))
            else:
                messages.info(request, _('Your email is not confirmed yet. We sent you a code.'))
                return redirect('verify_code')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {
        'form': form,
        'props': {
            'initial': {'email': form.data.get('email', '')},
            'errors': _form_errors(form),
            'registerUrl': reverse('register_view'),
        },
    })


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save(commit=False)
                    user.role = 'jobfinder'
                    user.is_active = False
                    user.save()
                    _start_verification(request, user)
            except Exception:
                logger.exception('Registration failed for %s', form.cleaned_data.get('email'))
                request.session.pop(PENDING_KEY, None)
                form.add_error(None, _('We could not send the confirmation code. Please try again later.'))
            else:
                return redirect('verify_code')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {
        'form': form,
        'props': {
            'initial': {'username': form.data.get('username', ''), 'email': form.data.get('email', '')},
            'errors': _form_errors(form),
            'checkUrl': reverse('check_availability'),
            'loginUrl': reverse('login_view'),
        },
    })


def _pending_token(request):
    user_id = request.session.get(PENDING_KEY)
    if not user_id:
        return None
    return EmailVerificationToken.objects.select_related('user').filter(
        user_id=user_id, user__is_active=False
    ).first()


def verify_code(request):
    token = _pending_token(request)
    if token is None:
        return redirect('register_view')

    error = ''
    if request.method == 'POST':
        code = ''.join(ch for ch in request.POST.get('code', '') if ch.isdigit())
        ok, error = token.check_code(code)
        if ok:
            user = token.user
            user.is_active = True
            user.save(update_fields=['is_active'])
            token.is_verified = True
            token.code_hash = ''
            token.save(update_fields=['is_verified', 'code_hash'])
            request.session.pop(PENDING_KEY, None)
            login(request, user)
            messages.success(request, _('Welcome to Findy-Job, %(name)s!') % {'name': user.username})
            return redirect('index')

    return render(request, 'users/verify_code.html', {
        'props': {
            'email': _mask_email(token.user.email),
            'error': error,
            'resendIn': token.resend_available_in,
            'resendUrl': reverse('resend_code'),
        },
    })


@require_POST
def resend_code(request):
    token = _pending_token(request)
    if token is None:
        return JsonResponse({'ok': False, 'error': _('Your session expired. Please sign up again.')}, status=400)
    wait = token.resend_available_in
    if wait:
        return JsonResponse({'ok': False, 'error': _('Please wait %(seconds)d s.') % {'seconds': wait}, 'resendIn': wait}, status=429)
    try:
        code = token.issue_code()
        _send_code(token.user, code)
    except Exception:
        logger.exception('Could not resend verification code to %s', token.user.email)
        return JsonResponse({'ok': False, 'error': _('We could not send the code. Try again later.')}, status=502)
    return JsonResponse({'ok': True, 'resendIn': token.resend_available_in})


@require_GET
def check_availability(request):
    """Used by the registration form for live username/email checks."""
    result = {}
    username = request.GET.get('username', '').strip()
    email = request.GET.get('email', '').strip()
    if username:
        result['usernameTaken'] = User.objects.filter(username__iexact=username).exists()
    if email:
        result['emailTaken'] = User.objects.filter(email__iexact=email).exists()
    return JsonResponse(result)


def logout_view(request):
    logout(request)
    return redirect('index')
