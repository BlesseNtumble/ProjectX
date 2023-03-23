from django.utils import timezone

from railapp.models import Stations, StationList


def get_current_station(id) -> str:
    now_time = timezone.now()
    station = StationList.objects.filter(list_id__gte=id, start_date__time__lte=now_time, end_date__time__gte=now_time).first()
    return station

def get_station_list_direct(id):
    station = StationList.objects.filter(list_id__gte=id, type='D').order_by('start_date')
    return station

def get_station_list_reverse(id):
    station = StationList.objects.filter(list_id__gte=id, type='R').order_by('start_date')
    return station