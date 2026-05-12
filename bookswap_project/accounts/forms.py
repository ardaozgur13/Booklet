from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='E-posta')
    first_name = forms.CharField(max_length=50, required=True, label='Ad')
    last_name = forms.CharField(max_length=50, required=True, label='Soyad')

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'gender', 'city', 'phone', 'profile_photo', 'password1', 'password2')


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone', 'gender', 'city', 'profile_photo')


class LoginForm(forms.Form):
    username = forms.CharField(label='Kullanıcı Adı')
    password = forms.CharField(widget=forms.PasswordInput, label='Şifre')
