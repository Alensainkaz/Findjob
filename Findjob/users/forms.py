from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    username=forms.CharField(
        label='Username',
    )
    password1= forms.CharField(
            label='Password',
            widget=forms.PasswordInput(attrs={'placeholder':'Password'}),
            help_text=''
    )
    password2=forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(attrs={'placeholder':'Repeat password'}),
        help_text=''
    )
    email=forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder':'Email'}),
        help_text=''
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
class UserLoginForm(forms.Form):
    email=forms.EmailField(label='Email')
    password=forms.CharField(label='Password',widget=forms.PasswordInput)
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError('Пользователь с таким email не найден')
        user=authenticate(username=user.username, password=password)
        if not user:
            raise forms.ValidationError('Неверный пароль')

        self.user = user
        return self.cleaned_data

    def get_user(self):
        return self.user
