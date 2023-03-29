from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from railapp.models import CustomUser


class RegisterForms(forms.ModelForm):

    class RegisterUserForm(UserCreationForm):
        username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control m-2',
                                                                 'style': 'border-color:#C52E32;', 'placeholder': 'Логин'}))
        email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control m-2',
                                                                'style': 'border-color:#C52E32;', 'placeholder': 'Email адрес'}))
        password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control m-2',
                                                                      'style': 'border-color:#C52E32;', 'placeholder': 'Пароль'}))
        password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control m-2',
                                                                      'style': 'border-color:#C52E32;', 'placeholder': 'Повтор пароля'}))

        class Meta:
            model = CustomUser
            fields = ('username', 'email', 'password1', 'password2')

    class LoginUserForm(AuthenticationForm):
        username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control m-2',
                                                                 'style': 'border-color:#C52E32;', 'placeholder': 'Логин'}))
        password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control m-2',
                                                                     'style': 'border-color:#C52E32;', 'placeholder': 'Пароль'}))