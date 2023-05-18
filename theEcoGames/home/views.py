from django.shortcuts import render
from .forms import UserCreationWithEmailForm, ContactForm
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from game.models import *
from game.forms import registrationForm
from django.shortcuts import redirect
from decouple import config
import datetime, calendar
import requests
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.urls import reverse_lazy, reverse

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



def contact(request):
    if request.method == "GET":
        form = ContactForm() # Sets up new variable form as the base contact form found in form.py
        #print("Sent GET LULZ")
    else:
        #print("POST!")
        form = ContactForm(request.POST) # Sets up new variable using the data submitted by the user
        if form.is_valid():
            # form.cleaned_data: extracts the data from the form and puts into variables
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email']
            message = name + ':\n' + form.cleaned_data['message'] # Combines name with message to fit within policy
            try:
                send_mail(subject, message, email, ['myemail@mydomain.com']) # Sends the email using the arguments
        
            except BadHeaderError:
                messages.add_message(request, messages.ERROR, 'Message Not Sent') # Error message to user 
                return HttpResponse("Invalid header found.") # Incase of bad header (Something wrong w/ request sent in)
            
            messages.add_message(request, messages.SUCCESS, 'Message Sent')
            return redirect(reverse('homeapp:home')) # Redirects us to the homepage if form was sent

        else:
            messages.add_message(request, messages.ERROR, 'Invalid Form Data; Message Not Sent')

    return render(request, 'home/feedback.html', {"form": form}) # Shows the form if request method was GET