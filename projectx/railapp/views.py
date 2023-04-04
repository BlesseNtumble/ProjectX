import datetime

from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import QuerySet
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import CreateView

from railapp import api
from railapp.apps import template
from django.http import HttpResponse, HttpResponseNotAllowed

from railapp.forms import RegisterForms
from railapp.models import Settings, ChatList, Chat, Roles


@login_required(login_url='/login')
def index(request):
    context = {'title': 'РЖД Контент'}
    return redirect('profile')
    # return render(request, template + '/index.html', context=context)


@login_required(login_url='/login')
def chat(request):
    chats = api.get_chat_list()
    context = {'title': 'Чаты', 'chats': chats,
               'sos': api.get_setting('sos_active').__contains__('[1,'),
               'sos_wagon': api.get_setting('sos_active')[3:-1],
               'alert_np': api.get_setting('alert_np')}

    role = Roles.objects.filter(name='Проводник').first()
    current_chatid = api.get_setting('current_chatid')

    if request.user.role == role:
        return redirect('chat-detail', slug=current_chatid)

    if request.POST:
        # name = request.POST.get('chat_name', api.get_setting('current_route'))
        route = api.get_setting('current_route')
        tabel = api.get_setting('current_tabel')

        chat = ChatList()
        chat.chat_name = f'{route}, {tabel}'
        chat.created_date = datetime.datetime.now()
        chat.is_readonly = False
        chat.save()

        stg = Settings.objects.filter(key='current_chatid').first()
        stg.value = str(chat.id)
        stg.save()

    return render(request, template + '/chat.html', context=context)


@login_required(login_url='/login')
def chatdetail(request, slug):
    chatlist = ChatList.objects.filter(id=int(slug)).first()
    chat = Chat.objects.filter(chat_id=chatlist)
    can_write = True

    context = {'title': 'Чат', 'chatlist': chatlist, 'chat': chat, 'can_write': can_write,
               'sos': api.get_setting('sos_active').__contains__('[1,'),
               'sos_wagon': api.get_setting('sos_active')[3:-1],
               'alert_np': api.get_setting('alert_np')}

    if request.POST and not chatlist.is_readonly:
        text = request.POST.get('text', None)
        if text:
            message = Chat()
            message.chat_id = chatlist
            message.user = request.user
            message.text = text
            message.date = timezone.now()
            message.save()

            if request.user.role.name == 'Начальник поезда':
                messages.info(request, text)

    return render(request, template + '/chat-detail.html', context=context)


@login_required(login_url='/login')
def profile(request):
    route = api.get_setting('current_route')
    tabel = api.get_setting('current_tabel')
    wagoon = 'Заказчик сказал что поезд без вагонов'

    number = api.get_setting('current_routelist')
    current_station = api.get_current_station(int(number))
    next_station = api.get_next_station(int(number))

    context = {'title': 'Рейс', 'route': route, 'tabel': tabel, 'wagoon': wagoon, 'current_station': current_station,
               'next_station': next_station, 'sos': api.get_setting('sos_active').__contains__('[1,'),
               'sos_wagon': api.get_setting('sos_active')[3:-1],
               'alert_np': api.get_setting('alert_np')}
    return render(request, template + '/profile.html', context=context)


@login_required(login_url='/login')
def routes(request):
    number = api.get_setting('current_routelist')
    routes_d = api.get_station_list_direct(int(number))
    routes_r = api.get_station_list_reverse(int(number))
    next_station = api.get_next_station(int(number))

    routes = routes_d | routes_r

    context = {'title': 'Маршрут', 'routes': routes, 'routes_len': len(routes),
               'next_station': next_station, 'sos': api.get_setting('sos_active').__contains__('[1,'),
               'sos_wagon': api.get_setting('sos_active')[3:-1],
               'alert_np': api.get_setting('alert_np')}
    return render(request, template + '/routes.html', context=context)


@login_required(login_url='/login')
def settings(request):
    context = {'title': 'Настройки', 'sos': api.get_setting('sos_active').__contains__('[1,'),
               'sos_wagon': api.get_setting('sos_active')[3:-1],
               'alert_np': api.get_setting('alert_np')}
    return render(request, template + '/settings.html', context=context)


@login_required(login_url='/login')
def logout_page(request):
    logout(request)
    return redirect('login')


def update_theme(request):
    if not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])

    if not request.session.__contains__('theme'):
        request.session['theme'] = 'light'

    if request.session['theme'] == 'dark':
        request.session['theme'] = 'light'
    else:
        request.session['theme'] = 'dark'

    return HttpResponse('ok')


def sos_activate(request):
    if not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])

    if api.get_setting('sos_active') is None:
        stg = Settings()
        stg.key = 'sos_active'
        stg.value = '[0,-1]'
        stg.save()

    if api.get_setting('sos_active').__contains__('[1,'):
        stg = Settings.objects.filter(key='sos_active').first()
        stg.value = '[0,-1]'
        stg.save()
    else:
        stg = Settings.objects.filter(key='sos_active').first()
        stg.value = f'[1, {request.user.number_wagon}]'
        stg.save()

    return HttpResponse('ok')


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
