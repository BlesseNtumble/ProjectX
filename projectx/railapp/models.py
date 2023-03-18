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


class Stations(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)
    start_date = models.DateTimeField(null=False, blank=False)
    end_date = models.DateTimeField(null=False, blank=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Станция'
        verbose_name_plural = 'Станции'


class StationList(models.Model):
    list_id = models.IntegerField(null=False, blank=False)
    station = models.ForeignKey(Stations, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f'[{self.list_id}] {self.station}'

    class Meta:
        verbose_name = 'Маршрутный лист'
        verbose_name_plural = 'Маршрутные листы'


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
