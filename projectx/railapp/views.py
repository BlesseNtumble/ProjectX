from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy

from railapp import api
from railapp.apps import template
from django.http import HttpResponse

from railapp.forms import RegisterForms


@login_required(login_url='/login')
def index(request):
    context = {'title': 'РЖД Контент'}
    print(api.get_current_station())

    return render(request, template + '/index.html', context=context)


@login_required(login_url='/login')
def chat(request):
    context = {'title': 'Чат'}
    return render(request, template + '/chat.html', context=context)


@login_required(login_url='/login')
def profile(request):
    context = {'title': 'Профиль'}
    return render(request, template + '/profile.html', context=context)


@login_required(login_url='/login')
def routes(request):
    context = {'title': 'Маршрут следования'}
    return render(request, template + '/routes.html', context=context)


@login_required(login_url='/login')
def settings(request):
    context = {'title': 'Настройки'}
    return render(request, template + '/settings.html', context=context)


@login_required(login_url='/login')
def logout_page(request):
    logout(request)
    return redirect('login')


def auth(request):
    f = RegisterForms.LoginUserForm
    context = {'form':f, 'title':'Авторизация'}
    return render(request, template + '/auth.html', context=context)


def reg(request):
    f = RegisterForms.RegisterUserForm
    context = {'form':f, 'title':'Регистрация'}
    return render(request, template + '/auth.html', context=context)


class LoginUser(LoginView):
    form_class = RegisterForms.LoginUserForm
    template_name = template + '/auth.html'

    def get_success_url(self):
        return reverse_lazy('index');