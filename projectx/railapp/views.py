from django.shortcuts import render

# Create your views here.
from railapp import api
from django.http import HttpResponse


def index(request):
    print(api.get_current_station())
    return HttpResponse(f'<html>Здарова, {request.user.role}!</html>')