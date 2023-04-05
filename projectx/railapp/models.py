from datetime import datetime

from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Roles(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'


class CustomUser(AbstractUser):
    role = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True, blank=False)
    number_route = models.CharField(max_length=20, null=True, blank=False)
    number_wagon = models.IntegerField(null=True, blank=False)


class Stations(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Станция'
        verbose_name_plural = 'Станции'


class StationList(models.Model):
    routes_type = [('D', 'Прямой'), ('R', 'Обратный'),]
    list_id = models.IntegerField(null=False, blank=False)
    station = models.ForeignKey(Stations, on_delete=models.CASCADE, null=False, blank=False)
    start_date = models.DateTimeField(null=False, blank=False)
    end_date = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=1,choices=routes_type, default='D')

    def __str__(self):
        return f'[{self.list_id}] {self.station}'

    class Meta:
        verbose_name = 'Маршрутный лист'
        verbose_name_plural = 'Маршрутные листы'

    def on_station(self):
        now = datetime.now().astimezone()
        start = self.start_date
        end = self.end_date
        return (now > start and now < end)

    def minus(self):
        start = self.start_date
        if self.on_station():
            start = datetime.now().astimezone()
        end = self.end_date
        res = 0
        if end is not None:
            res = (end - start).seconds

        return "%02d:%02d:%02d" % self._convert_to_preferred_format(res)


    def in_30_min(self):
        now = datetime.now().astimezone()
        start = self.start_date.astimezone()
        end = self.end_date
        res = (start - now)
        if res.days >= 0:
            time = self._convert_to_preferred_format(res.seconds)
            return time[1] + 1
        return -1



    def _convert_to_preferred_format(self, sec):
        sec = sec % (24 * 3600)
        hour = sec // 3600
        sec %= 3600
        min = sec // 60
        sec %= 60

        return (hour, min, sec)

class ChatList(models.Model):
    chat_name = models.CharField(max_length=256, null=False, blank=False)
    created_date = models.DateTimeField(null=False, blank=False)
    closed_date = models.DateTimeField(null=True, blank=True)
    is_readonly = models.BooleanField()

    def __str__(self):
        return f'{self.chat_name}'

    class Meta:
        verbose_name = 'Список чатов'
        verbose_name_plural = 'Список чатов'


class Chat(models.Model):
    chat_id = models.ForeignKey(ChatList, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField(null=False, blank=False)
    date = models.DateTimeField(null=False, blank=False)

    def __str__(self):
        return f'[{self.chat_id}] <{self.date}> {self.user}: {self.text}'

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чат'


class Settings(models.Model):
    key = models.CharField(max_length=256, null=False, blank=False)
    value = models.CharField(max_length=256, null=False, blank=False)
    description = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return f'{self.key}'

    class Meta:
        verbose_name = 'Настройки'
        verbose_name_plural = 'Настройки'