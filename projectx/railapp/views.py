import datetime

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import QuerySet
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView

from railapp import api
from railapp.apps import template
from django.http import HttpResponse

from railapp.forms import RegisterForms
from railapp.models import Settings, ChatList, Chat, Roles


@login_required(login_url='/login')
def index(request):
    context = {'title': 'РЖД Контент'}
    return redirect('profile')
    #return render(request, template + '/index.html', context=context)


@login_required(login_url='/login')
def chat(request):
    chats = api.get_chat_list()
    context = {'title': 'Чаты', 'chats': chats, }

    role = Roles.objects.filter(name='Проводник').first()
    current_chatid = api.get_setting('current_chatid')

    if request.user.role == role:
        return redirect('chat-detail', slug=current_chatid)

    if request.POST:
        name = request.POST.get('chat_name', api.get_setting('current_route'))
        if name == '':
            return redirect('chat')
        chat = ChatList()
        chat.chat_name = name
        chat.created_date = datetime.datetime.now()
        chat.is_readonly = False
        chat.save()

    return render(request, template + '/chat.html', context=context)


@login_required(login_url='/login')
def chatdetail(request, slug):

    chatlist = ChatList.objects.filter(id=int(slug)).first()
    messages = Chat.objects.filter(chat_id=chatlist)
    can_write = True

    context = {'title': 'Чат', 'chatlist': chatlist, 'messages': messages, 'can_write': can_write }

    if request.POST:
        text = request.POST.get('text', None)
        if text:
            message = Chat()
            message.chat_id = chatlist
            message.user = request.user
            message.text = text
            message.date = timezone.now()
            message.save()

    return render(request, template + '/chat-detail.html', context=context)


@login_required(login_url='/login')
def profile(request):
    reys = api.get_setting('current_route')
    wagoon = 'Заказчик сказал что поезд без вагонов'

    number = api.get_setting('current_routelist')
    current_station = api.get_current_station(int(number))
    next_station = api.get_next_station(int(number))


    context = {'title': 'Профиль', 'reys': reys, 'wagoon': wagoon, 'current_station': current_station, 'next_station': next_station }
    return render(request, template + '/profile.html', context=context)


@login_required(login_url='/login')
def routes(request):
    number = api.get_setting('current_routelist')
    routes_d = api.get_station_list_direct(int(number))
    routes_r = api.get_station_list_reverse(int(number))
    next_station = api.get_next_station(int(number))

    routes = routes_d | routes_r

    context = {'title': 'Маршрут следования', 'routes': routes, 'routes_len': len(routes), 'next_station': next_station}
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

