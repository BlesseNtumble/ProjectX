from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView

from railapp import api
from railapp.apps import template
from django.http import HttpResponse

from railapp.forms import RegisterForms


@login_required(login_url='/login')
def index(request):
    context = {'title': 'РЖД Контент'}
    print(api.get_current_station(1))

    return render(request, template + '/index.html', context=context)


@login_required(login_url='/login')
def chat(request):
    context = {'title': 'Чат'}
    return render(request, template + '/chat.html', context=context)


@login_required(login_url='/login')
def profile(request):
    reys = 7978812
    wagoon = 13
    context = {'title': 'Профиль', 'reys': reys, 'wagoon': wagoon}
    return render(request, template + '/profile.html', context=context)


@login_required(login_url='/login')
def routes(request):
    routes={1,2}
    context = {'title': 'Маршрут следования', 'routes': routes}
    return render(request, template + '/routes.html', context=context)


@login_required(login_url='/login')
def settings(request):
    context = {'title': 'Настройки'}
    return render(request, template + '/settings.html', context=context)


@login_required(login_url='/login')
def logout_page(request):
    logout(request)
    return redirect('login')


class LoginUser(LoginView):
    form_class = RegisterForms.LoginUserForm
    template_name = template + '/auth.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('index')


class RegisterUser(CreateView):
    form_class = RegisterForms.RegisterUserForm
    template_name = template + '/auth.html'
    success_url = reverse_lazy('login')
    extra_context = {'title': 'Регистрация'}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

