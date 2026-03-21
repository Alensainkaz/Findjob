from django.shortcuts import render, redirect
from .models import User, EmailVerificationToken
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'jobfinder'
            user.is_active = False
            user.save()
            token = EmailVerificationToken.objects.create(user=user)
            verify_url = request.build_absolute_uri(
                reverse('verify_email', args=[token.token])
            )
            html_message = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body style="margin:0;padding:0;background:#f4f5f7;font-family:Arial,sans-serif;">
    <div style="max-width:520px;margin:40px auto;background:#fff;border-radius:12px;border:1px solid #e8e8e8;overflow:hidden;">
        <div style="background:#111;padding:24px 32px;">
            <h1 style="margin:0;color:#fff;font-size:1.4rem;font-weight:700;">Findy-Job</h1>
        </div>
        <div style="padding:32px;">
            <h2 style="margin:0 0 10px;font-size:1.2rem;color:#111;">Подтвердите ваш email</h2>
            <p style="color:#555;font-size:0.95rem;margin:0 0 24px;line-height:1.6;">
                Привет, <strong>{user.username}</strong>! Вы зарегистрировались на Findy-Job.
                Нажмите кнопку ниже чтобы активировать аккаунт.
            </p>
            <a href="{verify_url}"
               style="display:inline-block;padding:12px 28px;background:#111;color:#fff;border-radius:6px;text-decoration:none;font-weight:600;font-size:0.95rem;">
                Подтвердить email
            </a>
            <p style="color:#999;font-size:0.8rem;margin-top:24px;line-height:1.5;">
                Если вы не регистрировались на Findy-Job — просто проигнорируйте это письмо.
            </p>
        </div>
        <div style="padding:16px 32px;border-top:1px solid #eee;text-align:center;">
            <p style="color:#aaa;font-size:0.8rem;margin:0;">© 2025 Findy-Job</p>
        </div>
    </div>
</body>
</html>"""
            send_mail(
                subject='Подтвердите ваш email — Findy-Job',
                message=f'Перейдите по ссылке: {verify_url}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
                html_message=html_message,
            )
            return redirect('registration_done')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def verify_email(request, token):
    try:
        token_obj = EmailVerificationToken.objects.get(token=token)
        user = token_obj.user
        user.is_active = True
        user.save()
        token_obj.is_verified = True
        token_obj.save()
        login(request, user)
        return redirect('index')
    except EmailVerificationToken.DoesNotExist:
        return render(request, 'users/invalid_token.html')


def registration_done(request):
    return render(request, 'users/registration_done.html')


def logout_view(request):
    logout(request)
    return redirect('index')