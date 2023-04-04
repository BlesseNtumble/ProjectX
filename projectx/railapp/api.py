import datetime

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone

from railapp.models import Stations, StationList, Settings, ChatList, CustomUser


def get_setting(setting) -> str:
    setting = Settings.objects.filter(key=setting).first()
    if setting is not None:
        return Settings.objects.filter(key=setting).first().value
    return None

def get_current_station(id) -> str:
    now = datetime.datetime.now().time()
    station = StationList.objects.filter(list_id=id, start_date__time__lte=now, end_date__time__gte=now).first()
    return station

def get_next_station(id) -> str:
    now = datetime.datetime.now().time()
    station = StationList.objects.filter(list_id=id, start_date__time__gte=now).first()
    return station

def get_station_list_direct(id):
    station = StationList.objects.filter(list_id=id, type='D').order_by('start_date')
    return station

def get_station_list_reverse(id):
    station = StationList.objects.filter(list_id=id, type='R').order_by('start_date')
    return station

def get_chat_list():
    chats = ChatList.objects.all()
    return chats

def get_all_logged_in_users():
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    return User.objects.filter(id__in=uid_list)