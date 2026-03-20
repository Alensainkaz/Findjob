from django.shortcuts import render,redirect
from .models import User,EmailVerificationToken
from .forms import UserRegisterForm,UserLoginForm
from django.contrib.auth import login,logout
from django.core.mail import send_mail
from django.urls import reverse
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('index')
    else:
        form = UserLoginForm()
    context = {'form':form}
    return render(request,'users/login.html',context)
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.role='jobfinder'
            user.is_active=False
            user.save()
            token=EmailVerificationToken.objects.create(user=user)
            verify_url=request.build_absolute_uri(
                reverse('verify_email',args=[token.token])
            )
            send_mail(
                subject='Подтвердите ваш email',
                message=f'Перейдите по ссылке: {verify_url}, для подтверждения вашего email. Если это не вы просто проигнорируйте это сообщение. С уважением Findy-Job company.',
                from_email='noreply.findy-job@mail.ru',
                recipient_list=[user.email],
            )
            return redirect('registration_done')
    else:
        form = UserRegisterForm()
    context = {'form':form}
    return render(request,'users/register.html',context)
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
