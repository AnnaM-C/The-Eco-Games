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

    context = {}
    player, created = Challenger.objects.get_or_create(user=request.user)
    player.save()
    # Get riddle object for when a user creates an account
    # riddle=Riddles.objects.get(r_id=1)
    rid=Riddles.objects.latest('text')
    ridtext=rid.text

    # Define API URL.
    QUOTE_URL = 'https://api.api-ninjas.com/v1/riddles'

    # Get API_KEY
    API_KEY=config('API_KEY')

    # Get todays date
    today = datetime.date.today()

    # Condition for API call
    if calendar.monthrange(today.year, today.month)[1] == today.day and rid.used==False:
        response = requests.get(QUOTE_URL, headers={'X-Api-Key': API_KEY})

        # If API is successful, store riddle in context dictionary
        if response.status_code == requests.codes.ok:
            data=response.json()
            question=data[0]['question']
            context['api_response']=question

            # # update riddle in database for future use
            # riddle.text=question
            r=Riddles(text=question)
            rid.used=True
            # # Save database object
            r.save()
            rid.save()
                
        else:
            print("Error:", response.status_code, response.text)
    else:

        # Did not call API for new riddle. Use existing riddle
        # r=getattr(riddle,'text')

        # r=Riddles.objects.latest().text

        # Store in context dictionary
        context['api_response']=ridtext

        # Save database object
        # rid.save()
        

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