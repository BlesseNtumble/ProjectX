from django.template.defaulttags import url

from railapp.views import *
from django.urls import path, include, re_path

import notifications.urls

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
    path('logout', logout_page, name='logout'),
    path('update_theme', update_theme, name='update_theme'),
    path('sos_activate', sos_activate, name='sos_activate'),
    path('plus_font', plus_font, name='plus_font'),
    path('minus_font', minus_font, name='minus_font'),
    re_path(r'^inbox/notifications/', include(notifications.urls, namespace='notifications')),
]