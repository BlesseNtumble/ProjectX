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