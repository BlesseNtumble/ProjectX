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
from railapp.models import Settings


@login_required(login_url='/login')
def index(request):
    context = {'title': 'РЖД Контент'}
    return redirect('profile')
    #return render(request, template + '/index.html', context=context)


@login_required(login_url='/login')
def chat(request):
    reys = {'МСК-ЧИТА, 02.03, 7623415', 'ЧИТА-МСК, 06.03, 7623416'}
    context = {'title': 'Чаты', 'reys': reys, }
    return render(request, template + '/chat.html', context=context)


@login_required(login_url='/login')
def chatdetail(request):
    reys = 'МСК-ЧИТА, 02.03, 7623415'
    context = {'title': 'Чат', 'reys': reys, }
    return render(request, template + '/chat-detail.html', context=context)


@login_required(login_url='/login')
def profile(request):
    reys = request.user.number_route
    wagoon = 13
    context = {'title': 'Профиль', 'reys': reys, 'wagoon': wagoon, }
    return render(request, template + '/profile.html', context=context)


@login_required(login_url='/login')
def routes(request):
    number = Settings.objects.filter(key='current_route').first()
    routes = api.get_station_list(int(number.value), False)
    print(api.get_current_station(int(number.value)))
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

