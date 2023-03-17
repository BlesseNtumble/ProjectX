from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from railapp.models import CustomUser


class RegisterForms(forms.ModelForm):

    class RegisterUserForm(UserCreationForm):
        username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}))
        email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email адрес'}))
        password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))
        password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повтор пароля'}))

        class Meta:
            model = CustomUser
            fields = ('username', 'email', 'password1', 'password2')

    class LoginUserForm(AuthenticationForm):
        username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}))
        password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))