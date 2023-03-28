from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from django.views.generic import ListView, CreateView, DetailView, FormView
from .forms import UserActivityForm
from django.urls import reverse_lazy
import requests
from django.contrib.auth.mixins import LoginRequiredMixin
import json
import datetime, calendar
from django.shortcuts import (get_object_or_404, render, redirect)
import os
from decouple import config
import random

# Comment

# Profile view

@login_required
def profile(request):

    context = {}

    # Get riddle object 1.

    riddle=Riddles.objects.get(r_id=1)

    # Define API URL.

    QUOTE_URL = 'https://api.api-ninjas.com/v1/riddles'

    # Get API_KEY

    API_KEY=config('API_KEY')

    # Get todays date

    today = datetime.date.today()

    # Condition for API call

    if calendar.monthrange(today.year, today.month)[1] == today.day:
        response = requests.get(QUOTE_URL, headers={'X-Api-Key': API_KEY})

        # If API is successful, store riddle in context dictionary

        if response.status_code == requests.codes.ok:
            data=response.json()
            question=data[0]['question']
            context['api_response']=question

            # update riddle in database for future use

            riddle.text=question

            # Save database object

            riddle.save()
                
        else:
            print("Error:", response.status_code, response.text)
    else:

        # Did not call API for new riddle. Use existing riddle

        r=getattr(riddle,'text')

        # Store in context dictionary

        context['api_response']=r

    # Get current user

    currentUser = request.user

    # Store in context dictionary

    context["currentUser"] = currentUser

    # Render profile page

    return render(request, 'game/profile.html', context)


# TO DO: Leaderboard view

@login_required
def leaderboards(request):
    context = {}
    return render(request, 'game/leaderboards.html', context)

# TO DO: Maps view

@login_required
def maps(request):
    context = {}
    return render(request, 'game/map.html', context)

# Activities view
# TO DO: Form validation - Add in messages.add_message(request, messages.SUCCESS, 'Event Created' / messages.add_message(request, messages.ERROR, 'Invalid Form Data; Event not created')
# TO DO: Adapt score/points based on sustainability index

@login_required
def createActivitiesView(request):

    context = {}

    # Form

    form = UserActivityForm(request.POST or None,initial={'challenger':request.user})
    
    # Get all activities

    # items = list(Activity.objects.all())

    # # Randomise activity list 

    # random_items = random.sample(items, 3)

    # # Convert back to queryset

    # queryset=Activity.objects.filter(id__in=[getattr(id,'id') for id in random_items])

    # Reassign activities for form field 

    # form.fields['activities'].queryset=queryset
    # queryset=Activity.objects.all().order_by('?')[:3]
    # form.fields['activities'].queryset=queryset
    # print(queryset)
    if(request.method == 'POST'):

        if form.is_valid():

            # get date from post variable

            date=form.cleaned_data['date']

            # Set API header

            headers = {
                'Accept': 'application/json'
            }

            # Set API URL

            api_url=f'https://api.carbonintensity.org.uk/intensity/{date}'

            # Request to API

            response=requests.get(api_url, params={}, headers=headers) 

            # Get the carbon index

            js=response.json()

            #  Parse JSON reponse

            index=js['data'][0]['intensity']['index']

            # Get number of logged activities

            activities=request.POST.getlist('activities')

            # Get player object

            player, created = Challenger.objects.get_or_create(user=request.user)

            # Get the players current score from DB

            score=player.score

            # All points for each activity logged, are added to the users current score

            for id in activities:

                activity=Activity.objects.get(id=id)

                # Get points for each activity

                points=getattr(activity, 'points')
                print(points)
                score = score + points

            # Update the database with players new score

            player.score=score

            # Save player

            player.save()

            # TO DO: Adapt score/points based on sustainability index

            form.instance.challenger=request.user

            form.save()

            return redirect('profile')

    context['form']= form
    return render(request, "game/activities.html", context)

