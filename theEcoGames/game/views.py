from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from django.views.generic import ListView, CreateView, DetailView, FormView, View
# from .forms import UserActivityForm
from django.urls import reverse_lazy
import requests
from django.contrib.auth.mixins import LoginRequiredMixin
import json
import datetime, calendar
from django.shortcuts import (get_object_or_404, render, redirect)
import os
from decouple import config
from django.http import JsonResponse
import random
from datetime import date
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.core.serializers import deserialize
from django.http import JsonResponse


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

# @login_required
# def createActivitiesView(request):

#     context = {}

#     # Form

#     form = UserActivityForm(request.POST or None,initial={'challenger':request.user})
    
#     # Get all activities

#     # items = list(Activity.objects.all())

#     # # Randomise activity list 

#     # random_items = random.sample(items, 3)

#     # # Convert back to queryset

#     # queryset=Activity.objects.filter(id__in=[getattr(id,'id') for id in random_items])

#     # Reassign activities for form field 

#     # form.fields['activities'].queryset=queryset
#     # queryset=Activity.objects.all().order_by('?')[:3]
#     # form.fields['activities'].queryset=queryset
#     # print(queryset)
#     if(request.method == 'POST'):

#         if form.is_valid():

#             # get date from post variable

#             date=form.cleaned_data['date']

#             # Set API header

#             headers = {
#                 'Accept': 'application/json'
#             }

#             # Set API URL

#             api_url=f'https://api.carbonintensity.org.uk/intensity/{date}'

#             # Request to API

#             response=requests.get(api_url, params={}, headers=headers) 

#             # Get the carbon index

#             js=response.json()

#             #  Parse JSON reponse

#             index=js['data'][0]['intensity']['index']

#             # Get number of logged activities

#             activities=request.POST.getlist('activities')

#             # Get player object

#             player, created = Challenger.objects.get_or_create(user=request.user)

#             # Get the players current score from DB

#             score=player.score

#             # All points for each activity logged, are added to the users current score

#             for id in activities:

#                 # TO DO: in here get the user input of activity time from AJAX,
#                 # then add them to each activity object.

#                 activity=Activity.objects.get(id=id)

#                 # Get points for each activity

#                 points=getattr(activity, 'points')
#                 print(points)
#                 score = score + points

#             # Update the database with players new score

#             player.score=score

#             # Save player

#             player.save()

#             # TO DO: Adapt score/points based on sustainability index

#             form.instance.challenger=request.user

#             form.save()

#             return redirect('gameapp:profile')

#     context['form']= form
#     return render(request, "game/activities.html", context)



def categoriesActivitesView(request):
    context={}
    
    context['category_list'] = Category.objects.all()

    # for category in categories:
    #     name = getattr(category, 'name')
    #     context[name] = name
    return render(request, "game/activitiesCategory.html", context)


class ActivitiesDetailView(LoginRequiredMixin, DetailView):
    model=Category
    template_name="game/activitiesDetail.html"
    def get_context_data(self, **kwargs):
        category=get_object_or_404(Category, pk=self.kwargs['pk'])
        player, created = Challenger.objects.get_or_create(user=self.request.user)
        player.save()
        cart, created = UserCart.objects.get_or_create(challenger=player)
        cart.save()
        context={}
        # if(is_admin(self.request.user)):
        context['activity_list']=Activity.objects.filter(cat=category)
        print(context)
        context['category']=category
        context['cart'] = cart
        # context['line_items'] = LineItem.objects.filter(cart=cart, dateRecorded = date.today()) #set up the line items
        context['line_items'] = LineItem.objects.filter(cart=cart, checkedOut=False, dateRecorded=date.today()) #set up the line items
        test=Activity.objects.filter(id=78)
        print("activity-",test)
        val=test.values('type')
        # val=test.type
        print(val)

        return context



class AddLineItem(LoginRequiredMixin, View):
     def post(self, request):
        duration=request.POST['duration']
        time=request.POST['time']
        activityId=request.POST['activityId']
        activity=get_object_or_404(Activity, id=activityId)
        player = Challenger.objects.get(user=request.user)
        cart = UserCart.objects.get(challenger=player)

        # if statement to check if line item not submitted already exists
        if LineItem.objects.filter(checkedOut=False, activity=activity, cart=cart).exists():
            return JsonResponse({'cart_success': False}, status=200)
        elif LineItem.objects.filter(dateRecorded=date.today(), activity=activity, cart=cart).exists():
            return JsonResponse({'not_cart_success': False}, status=200)
        else:
            # Everytime we add a line item we need to add the cart and activity ourselves
            lineItem=LineItem(timeRecorded=time, dateRecorded=date.today(), activityDuration=duration, activity=activity, cart=cart)
            lineItem.save()
            itemId=getattr(lineItem, 'pk')
            
            line_item_html = render_to_string('game/lineItem.html', {'item': lineItem, 'item-id': itemId})

            # lineItem.activityDuration=time
            return HttpResponse(line_item_html)


# method to calculate all the points and send them to the server
# ajax doesnt have to render anything so no need for server to return anything to ajax
# just a success message will do

class RecordPoints(LoginRequiredMixin, View):
     def post(self, request):
        if request.method == 'POST':
        # grab all those items you got
        # i need to have a list of all the list items pk id
            list_items=request.POST.getlist('list_items[]')
        # then i can filter and get the objects by id
            print(list_items)

            for id in list_items:
                itemQS=LineItem.objects.filter(pk=id)
                itemQS.update(checkedOut=True)

                item=LineItem.objects.get(pk=id)

                activity=getattr(item, 'activity')

                activity_point=getattr(activity,'points')

                # Get player object
                player = Challenger.objects.get(user=request.user)

                # Get the players current score from DB
                old_score=player.score
                print(old_score)
                new_score=old_score+activity_point
                print(new_score)
                player.score=new_score
                player.save()

            return JsonResponse({'message': 'Elements received and processed successfully.'})
        else:
            return JsonResponse({'message': 'No elements found.'})


class SetDurationField(LoginRequiredMixin, View):
    def get(self, request):

        duration_item_html = render_to_string('game/durationField.html')

        # lineItem.activityDuration=time
        return HttpResponse(duration_item_html)

def tipsIndex(request):
    context = {}

    return render(request, "game/tipsIndex.html", context)

