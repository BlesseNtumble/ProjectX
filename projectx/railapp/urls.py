from django.urls import path

from railapp.views import *

urlpatterns = [
    path('', index, name='index'),
    path('logout', logout_page, name='logout'),
    path('login', LoginUser.as_view(), name='login'),
    path('chat', chat, name='chat'),
    path('chat-detail/<slug:slug>', chatdetail, name='chat-detail'),
    path('profile', profile, name='profile'),
    path('routes', routes, name='routes'),
    path('settings', settings, name='settings'),
    path('register', RegisterUser.as_view(), name='register'),
    path('logout', logout_page, name='logout')
]