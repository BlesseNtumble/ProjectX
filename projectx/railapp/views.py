from django.shortcuts import render

# Create your views here.
from railapp import api
from railapp.apps import template
from django.http import HttpResponse


def index(request):
    context = {'title': 'РЖД Контент'}
    print(api.get_current_station())

    return render(request, template + '/index.html', context=context)