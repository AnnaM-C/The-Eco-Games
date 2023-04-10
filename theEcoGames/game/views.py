from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from django.views.generic import ListView, CreateView, DetailView, FormView, View
#from .forms import UserActivityForm, locationUpdateForm
from .forms import locationUpdateForm
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
from django.db.models import Count
import numpy as np
from django.utils import timezone
from datetime import timedelta


from django.http import HttpResponse
from django.contrib import messages
# Profile view

@login_required
def profile(request):

    context = {}
    player, created = Challenger.objects.get_or_create(user=request.user)
    player.save()
    context['line_items']=getCartItems(player)
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

    # Get the challenger information

    context["challenger"] = currentUser.challenger



    # Getting the Location Update from
    locationForm = locationUpdateForm(request.POST or None)
    context["locationForm"] = locationForm

    return render(request, 'game/profile.html', context)


def locationUpdateView(request):

    print("Started!")

    context = {}
    currentUser = request.user

    context["currentUser"] = currentUser
    context["challenger"] = currentUser.challenger

    currentChallenger = get_object_or_404(Challenger, user = currentUser)

    form = locationUpdateForm(request.POST or None, instance = currentChallenger)
    print(form.is_bound)

    if form.is_valid():
        print("HAYA")
        form.save()
        messages.add_message(request, messages.SUCCESS, 'Location Updated')
        return redirect('gameapp:profile')
    
    else:
        messages.add_message(request, messages.ERROR, 'Something went wrong!')
        print("Something went wrong!")
        print(form.errors.as_data())
        return render(request, 'game/profile.html', context)    


# TO DO: Leaderboard view

@login_required
def leaderboards(request):
    context = {}

    user = request.user
    context['currentUser'] = user
    # Important to reverse the list otherwise it counts lowest number first
    context["topChallengers"] =  Challenger.objects.all().order_by('score').reverse()[:10]


    player, created = Challenger.objects.get_or_create(user=request.user)
    player.save()
    context['line_items']=getCartItems(player)
    return render(request, 'game/leaderboards.html', context)

# TO DO: Maps view

@login_required
def maps(request):
    context={}
    player, created = Challenger.objects.get_or_create(user=request.user)
    player.save()
    context['line_items']=getCartItems(player)
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


@login_required
def categoriesActivitesView(request):
    context={}
    player, created = Challenger.objects.get_or_create(user=request.user)
    player.save()
    context['line_items']=getCartItems(player)
    context['category_list'] = Category.objects.all()

    # for category in categories:
    #     name = getattr(category, 'name')
    #     context[name] = name
    return render(request, "game/activitiesCategory.html", context)


class ActivitiesDetailView(LoginRequiredMixin, DetailView):
    model=Category
    template_name="game/activitiesDetail.html"
    def get_context_data(self, **kwargs):
        context={}
        category=get_object_or_404(Category, pk=self.kwargs['pk'])
        player, created = Challenger.objects.get_or_create(user=self.request.user)
        player.save()
        context['line_items']=getCartItems(player)

        cart, created = UserCart.objects.get_or_create(challenger=player)
        cart.save()

        context['activity_list']=Activity.objects.filter(cat=category)
        context['category']=category
        context['cart'] = cart
        # context['line_items'] = LineItem.objects.filter(cart=cart, dateRecorded = date.today()) #set up the line items
        # context['line_items'] = LineItem.objects.filter(cart=cart, checkedOut=False, dateRecorded=date.today()) #set up the line items
        test=Activity.objects.filter(id=78)

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
        if LineItem.objects.filter(dateRecorded=date.today(), checkedOut=False, activity=activity, cart=cart).exists():
            return JsonResponse({'cart_success': False}, status=200)
        elif LineItem.objects.filter(dateRecorded=date.today(), checkedOut=True, activity=activity, cart=cart).exists():
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
            player = Challenger.objects.get(user=request.user)
            postcode=getattr(player, 'postcode')

            for id in list_items:
                itemQS=LineItem.objects.filter(pk=id)
                itemQS.update(checkedOut=True)
                item=LineItem.objects.get(pk=id)
                time=getattr(item, 'timeRecorded')
                print(time)
                # reformat date and time
                # Convert time string to time object
                # time_obj = datetime.datetime.strptime(time, "%H:%M:%S.%f")

                # # Convert date string to date object
                # date_obj = datetime.datetime.strptime(date.today(), "%Y-%m-%d")

                # Combine date and time objects
                datetime_obj = datetime.datetime.combine(date.today(), time)

                # Format as string in "YYYY-MM-DDThh:mmZ" format
                formatted_from_datetime = datetime_obj.strftime("%Y-%m-%dT%H:%MZ")

                toTime=datetime_obj+datetime.timedelta(minutes=30)
                formatted_to_datetime=toTime.strftime("%Y-%m-%dT%H:%MZ")

                # Set API header               
                headers = {
                'Accept': 'application/json'
                }
                
                r = requests.get(f'https://api.carbonintensity.org.uk/regional/intensity/{formatted_from_datetime}/{formatted_to_datetime}/postcode/RG10', params={}, headers = headers)
                
                # Get the carbon index
                js=r.json()

                #  Parse JSON reponse
                index=js['data']['data'][0]['intensity']['index']
                activity=getattr(item, 'activity')
                activity_point=getattr(activity,'points')
                print(index)
                # Get player object
                player = Challenger.objects.get(user=request.user)

                plus=0
                # Adjust score based on index
                match index:
                    case "very low":
                        plus=40
                    case "low":
                        plus=30
                    case "moderate":
                        plus=20
                    case "high":
                        plus=10
                    case "very-high":
                        plus=0

                # Get the players current score from DB
                old_score=player.score

                new_score=old_score+activity_point+plus

                player.score=new_score
                player.save()

            return JsonResponse({'message': 'Elements received and processed successfully.'})
        else:
            return JsonResponse({'message': 'No elements found.'})


@login_required
def tipsIndex(request):
    context = {}
    player, created = Challenger.objects.get_or_create(user=request.user)
    player.save()

    # context['line_items']=getCartItems(player)

    # player_line_items=getCartItems(player)

    def num_lineitems(self):
        num_lineitems = LineItem.objects.all().count()
        return num_lineitems

    user_top_activities = Activity.objects.filter(lineitem__cart__challenger=player) \
                .annotate(num_lineitems=Count('lineitem')) \
                .order_by('-num_lineitems')[:3]


    total_top_activities = Activity.objects.all() \
                .annotate(num_lineitems=Count('lineitem')) \
                .order_by('-num_lineitems')[:3]
    

    print(total_top_activities)
    print(user_top_activities)


    # Most popular user specific activities
    context['heating_user_popular'] = getActivityByCategory(user_top_activities, "Heating")
    context['washing_user_popular']= getActivityByCategory(user_top_activities, "Washing")
    context['bathroom_user_popular']= getActivityByCategory(user_top_activities, "Bathroom")
    context['devices_user_popular']= getActivityByCategory(user_top_activities, "Electronics")


    user_cart = UserCart.objects.get(challenger=player)
    one_week_ago = timezone.now() - timedelta(days=7)
    user_log = LineItem.objects.filter(dateRecorded__range=[one_week_ago, timezone.now()], cart=user_cart)
    user_activities = [getattr(log, 'activity') for log in user_log]
    all=Activity.objects.all()
    all_activities=list(all)

    # Personalised recommendations based on logged activities for the week
    recommendations=[activity for activity in all_activities if activity not in user_activities]

    # Personalised recommendations for users
    context['heating_recommendations'] = getActivityByCategory(recommendations, "Heating")
    context['washing_recommendations']= getActivityByCategory(recommendations, "Washing")
    context['bathroom_recommendations']= getActivityByCategory(recommendations, "Bathroom")
    context['devices_recommendations']= getActivityByCategory(recommendations, "Electronics")


    # Most popular user specific activities
    context['heating_popular'] = getActivityByCategory(total_top_activities, "Heating")
    context['washing_popular']= getActivityByCategory(total_top_activities, "Washing")
    context['bathroom_popular']= getActivityByCategory(total_top_activities, "Bathroom")
    context['devices_popular']= getActivityByCategory(total_top_activities, "Electronics")

    return render(request, "game/tipsIndex.html", context)

login_required
def getActivityByCategory(list, category):
    newlist=[]
    for act in list:
        if act.cat.name == category:
            newlist.append(act)
    return newlist

    
@login_required
def getCartItems(player):
    cart, created = UserCart.objects.get_or_create(challenger=player)
    cart.save()
    context={}
    context['line_items'] = LineItem.objects.filter(cart=cart, checkedOut=False, dateRecorded=date.today()) #set up the line items
    return context['line_items']
