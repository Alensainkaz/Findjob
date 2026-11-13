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
    def clean_email(self):
        email=self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('This email already exists')
        return email
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
class UserLoginForm(forms.Form):
    pending_user = None

    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if not email or not password:
            return self.cleaned_data

        user_obj = User.objects.filter(email__iexact=email).first()
        if not user_obj:
            raise forms.ValidationError('Wrong email or password')

        if not user_obj.is_active and user_obj.check_password(password):
            # View sends a fresh code and redirects to the code page
            self.pending_user = user_obj
            raise forms.ValidationError('Please confirm your email first.', code='inactive')

        user = authenticate(username=user_obj.username, password=password)
        if not user:
            raise forms.ValidationError('Wrong email or password')

        self.user = user
        return self.cleaned_data
    def get_user(self):
        return self.user
