from django.urls import path

from railapp.views import *

urlpatterns = [
    path('', index, name='index'),
    path('logout', logout_page, name='logout'),
    path('login', LoginUser.as_view(), name='login'),
    path('chat', name='chat'),
    path('profile', name='profile'),
    path('routes', name='routes'),
    path('settings', name='settings'),
]