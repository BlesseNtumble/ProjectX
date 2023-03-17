from django.urls import path

from railapp.views import *

urlpatterns = [
    path('', index, name='index'),
    path('logout', logout_page, name='logout'),
    path('login', auth, name='login'),
    path('chat', chat, name='chat'),
    path('profile', profile, name='profile'),
    path('routes', routes, name='routes'),
    path('settings', settings, name='settings'),
]