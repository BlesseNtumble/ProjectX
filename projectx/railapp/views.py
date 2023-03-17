from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy

from railapp import api
from railapp.apps import template
from django.http import HttpResponse

from railapp.forms import RegisterForms


@login_required(login_url='/login')
def index(request):
    context = {'title': 'РЖД Контент'}
    print(api.get_current_station())

    return render(request, template + '/index.html', context=context)


@login_required(login_url='/login')
def logout_page(request):
    logout(request)
    return redirect('login')


class LoginUser(LoginView):
    form_class = RegisterForms.LoginUserForm
    template_name = template + '/login.html'

    def get_success_url(self):
        return reverse_lazy('index');