import datetime

from django.utils import timezone

from railapp.models import Stations, StationList, Settings, ChatList


def get_setting(setting) -> str:
    return Settings.objects.filter(key=setting).first().value

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