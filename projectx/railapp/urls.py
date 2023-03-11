from django.urls import path

from railapp.views import *

urlpatterns = [
    path('', index, name='index')
]