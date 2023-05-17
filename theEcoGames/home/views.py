from django.shortcuts import render
from .forms import UserCreationWithEmailForm 
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from game.models import *
from game.forms import registrationForm
from django.shortcuts import redirect
from decouple import config
import datetime, calendar
import requests

# Home view

def home(request):
    context = {}
    # Get the logged in user's name

    currentUser = request.user

    context["currentUser"] = currentUser        

    return render(request, 'home/home.html', context)


# Register New User

def registerNewUser(request):
    if request.method == 'POST':
        form = registrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gameapp:profile')
    else:
        form = registrationForm()
    return render(request, 'home/registerNew.html', {'form': form})



# Sign up view

class RegisterUser(CreateView):
    model = User
    form_class = UserCreationWithEmailForm 
    template_name = 'home/register.html'
    success_url = reverse_lazy('login')


def privacyPolicy(request):
    context = {}

    return render(request, 'home/policy.html', context)