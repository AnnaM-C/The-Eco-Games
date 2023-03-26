from django.shortcuts import render
# from .forms import UserCreationWithEmailForm 
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

# Create your views here.

# sing up view
# class RegisterUser(CreateView):
#     model = User
#     form_class = UserCreationWithEmailForm 
#     template_name = 'home/register.html'
#     success_url = reverse_lazy('login')