from django.shortcuts import render
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib import messages



# Create your views here.

# home view
def home(request):
    context = {}
    return render(request, 'home/home.html', context)



def contact(request):
    if request.method == "GET":
        form = ContactForm() # Sets up new variable form as the base contact form found in form.py
        print("Sent GET LULZ")
    else:
        print("POST!")
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
            return redirect(reverse('home')) # Redirects us to the homepage if form was sent

        else:
            messages.add_message(request, messages.ERROR, 'Invalid Form Data; Message Not Sent')

    return render(request, 'home/contact.html', {"form": form}) # Shows the form if request method was GET