from django.utils import timezone

from railapp.models import Stations


def get_current_station() -> str:
    now_time = timezone.now()
    station = Stations.objects.filter(start_date__time__lte=now_time, end_date__time__gte=now_time).first()
    return station