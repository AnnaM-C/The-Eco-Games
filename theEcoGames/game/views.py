from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from django.views.generic import ListView, CreateView, DetailView, FormView, View
#from .forms import UserActivityForm, locationUpdateForm
from .forms import locationUpdateForm
from django.urls import reverse_lazy, reverse
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
from django.db.models import Count
import numpy as np
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse, Http404
from django.contrib import messages

# Profile view

@login_required
def profile(request):

    context = {}
    player, created = Challenger.objects.get_or_create(user=request.user)
    player.save()
    context['line_items']=getCartItems(player)
    # Get riddle object for when a user creates an account
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

        # Save database object
        riddle.save()
        
    # Get current user
    currentUser = request.user

    # Store in context dictionary
    context["currentUser"] = currentUser

    # Get the challenger information
    context["challenger"] = currentUser.challenger

    # Getting the Location Update from
    locationForm = locationUpdateForm(request.POST or None)
    context["locationForm"] = locationForm

    # Get the total activities recorded by the user
    currentUser = request.user
    currentChallenger = currentUser.challenger

    challengerActivity = LineItem.objects.filter(cart__challenger=currentChallenger).count()
    
    context["recordedActivities"] = challengerActivity

    return render(request, 'game/profile.html', context)


def locationUpdateView(request):

    context = {}
    currentUser = request.user

    context["currentUser"] = currentUser
    context["challenger"] = currentUser.challenger

    currentChallenger = get_object_or_404(Challenger, user = currentUser)

    form = locationUpdateForm(request.POST or None, instance = currentChallenger)
    print(form.is_bound)

    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, 'Location Updated')
        return redirect('gameapp:profile')
    
    else:
        messages.add_message(request, messages.ERROR, 'Something went wrong!')
        print("Something went wrong!")
        print(form.errors.as_data())
        #return render(request, 'game/profile.html', context)
        return redirect('gameapp:profile')  


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


def leaderboardUpdater(request):
    context = {}
    # Fetch the latest top challengers and all
    
    # "topChallengers" = Challenger.objects.all().order_by('score').reverse()[:10].values()
    
    topchallengers = Challenger.objects.all().order_by('score').reverse()[:10].values()
    
    topnames = Challenger.objects.all().order_by('score').reverse()[:10].values_list('user__username', flat=True)
   

    return JsonResponse({"challenged": list(topchallengers), "challengedNames": list(topnames)}, status = 200)


# Maps view

@login_required
def maps(request):
    context={}
    DATA_KEY = config('DATA_KEY') # Get API key
    mapdata = { # Holds postal areas and values. Function is used to populatw
            "name": ["score"]
        }
    mapdataRaw = ""
    
    player, created = Challenger.objects.get_or_create(user=request.user)
    player.save()
    context['line_items']=getCartItems(player)

    mapID = "RJrKg"

    '''
    mapdata is shortened to md in function names
    mv in function names refers to map visualtion
    '''

    '''
    Create a new map
    '''
    def mvInit():
        mapID = ""
        # Create a new chart  
        url = f"https://api.datawrapper.de/v3/charts"

        data = {
            "title": "The Eco Games", 
            "type": "d3-maps-choropleth"
                }
        
        headers = {
            "Authorization": f"Bearer {DATA_KEY}",
            "accept": "*/*",
            "content-type": "application/json"
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 201: mapID = response.json()['publicId'] # Get actual areas using 'values'

        # print(response.status_code, response.text)
        print(mapID)
        return mapID

    def mvBaseKey():
        # Add chart data  
        url = f"https://api.datawrapper.de/v3/charts/{mapID}"

        data = {"metadata":{"axes":{"keys":"name","values":"score"},"visualize":{"basemap":"united-kingdom-postal-areas","map-key-attr":"name"}}}
        headers = {
            "Authorization": f"Bearer {DATA_KEY}",
            "accept": "*/*",
            "content-type": "application/json"
        }

        response = requests.patch(url, json=data, headers=headers)

        print(response.status_code, response.text)

    def mvTooltip():
        True

    def mvMetadata():
        True

    def mvPublish():
        url = f"https://api.datawrapper.de/v3/charts/{mapID}/publish"

        headers = {
            "Authorization": f"Bearer {DATA_KEY}"
            # "accept": "*/*",
        }

        response = requests.post(url, headers=headers)

        print(response.status_code, response.text)

        return response.json()['data']['metadata']['publish']['embed-codes']['embed-method-iframe']

        

        # url = f"https://api.datawrapper.de/v3/charts/{mapID}"

        # headers = {
        #     "Authorization": f"Bearer {DATA_KEY}",
        #     "accept": "*/*",
        # }

        # response = requests.get(url, headers=headers)

        # print(response.status_code, response.text)
    

    def mdInit():
        # URL to get constituencies
        url = "https://api.datawrapper.de/v3/basemaps/uk-postal-areas/name"
        headers = {
            "accept": "*/*"
            }
        response = requests.get(url, headers = headers)

        if response.status_code == requests.codes.ok: context['api_response'] = response.json()['values'] # Get actual areas using 'values'
        else: print("Error:", response.status_code, response.text)
        Location.objects.all().delete()
        for i in range(len(context['api_response'])):
            mapdata.update({f"{context['api_response'][i]}":[0]})

            # make all locations
            n = Location(postcode=f"{context['api_response'][i]}")
            n.save()

    def mdUpdate():
        allUsers = Challenger.objects.all() # get all users
        locs = Location.objects.all() # get all locations
        for user in allUsers:
            userScore = user.score # Get the user's score
            rawUserCode = user.postcode # Get the user's postcode
            rawUserCode = rawUserCode.strip() # Remove any trailing blanks etc
            cleanUserCode = ''.join(i for i in rawUserCode if not i.isdigit()) # Remove numbers from postcode 
            # DEBUG: Comment out below line
            print(f'Postcode: {cleanUserCode if cleanUserCode != "" else "__"}, Score: {userScore} {">> Ignore" if cleanUserCode == "" else ">> OK"}')
            # Ignore users with no assigned postcode, for those who do, add their score to the total for the region
            if cleanUserCode != "" and cleanUserCode in mapdata : mapdata[f'{cleanUserCode}'][0] = mapdata[f'{cleanUserCode}'][0] + userScore
        # DEBUG: Comment out below line
        # print(mapdata)
        # mapdata is ready to be processed the way datawrapper likes it

        # iterate over locations, look for loc, get score from dictionary

        for loc in locs:
            locPostcode = loc.postcode # Get postal area
            country = loc.country # postal score

            loc.score = mapdata.get(locPostcode)[0]
            country = "TestCountry"
            loc.save()
            if loc.score > 0:
                print(f"Area: {locPostcode}, Score: {loc.score}")




    
    def mdCSV():
        mapdataRaw = ""
        for key, value in mapdata.items():
            mapdataRaw += f"{key},{value[0]}\n"
        return mapdataRaw

    def mdUpload():
        # Add chart data  
        url = f"https://api.datawrapper.de/v3/charts/{mapID}/data"

        data = mapdataRaw
        headers = {
            "Authorization": f"Bearer {DATA_KEY}",
            "accept": "*/*",
            "content-type": "text/csv"
        }

        response = requests.put(url, data=data, headers=headers)

        print(response.status_code, response.text)

    def mdVerify():
        # Check data added
        url = f"https://api.datawrapper.de/v3/charts/{mapID}/data"
        headers = {
            "Authorization": f"Bearer {DATA_KEY}",
            "accept": "application/json"
            }
        response = requests.get(url, headers=headers)

        print(response.text)

    # mapID = mvInit()

    mdInit()
    mdUpdate()
    
    mapdataRaw = mdCSV()
    
    mdUpload()
    mdVerify()

    # mvBaseKey()
    
    # mvTooltip()
    # mvMetadata()
    
    embedString = mvPublish()

    substring = '"'
    sub_indices = []
    for i in range(len(embedString) - len(substring)):
        if embedString[i:i + len(substring)] == substring: sub_indices.append(i)

    context['map_title'] = embedString[sub_indices[0]+1:sub_indices[1]]
    context['map_id'] = embedString[sub_indices[4]+1:sub_indices[5]]
    context['map_src'] = embedString[sub_indices[6]+1:sub_indices[7]]
    context["challenger"] = request.user.challenger

    print(context)
    
    return render(request, 'game/map.html', context)

@login_required
def competitions(request, compYear, compMonth):
    if compMonth < 1 or compMonth > 12: raise Http404
    context = {}
    context['compYear'] = compYear
    context['compMonth'] = compMonth
    return render(request, 'game/competitions.html', context)

@login_required
def compete(request):
    context = {}

    locs = Location.objects.all() # get all locations
    context["topLocations"] =  Location.objects.all().order_by('score').reverse()[:3]
    context["otherLocations"] =  Location.objects.all().order_by('score').reverse()[3:]

    return render(request, 'game/compete.html', context)

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


def get_weather_data(request):

    # Get API_KEY
    WEATHER_KEY=config('WEATHER_KEY')
    
    """
    Returns weather data from the OpenWeather API for the specified location, or a default location if no location is specified.
    """
    # Get the location parameter from the request, or use the default location Guildford
    location = request.GET.get("location", "Guildford")

    # Make an HTTP GET request to the OpenWeather API
    weather_response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_KEY}")

    # Extract relevant weather data from the API response
    weather_data = weather_response.json()
    temperature = weather_data["main"]["temp"]
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]

    # Return the weather data as a JSON response
    return JsonResponse({
        "temperature": temperature,
        "humidity": humidity,
        "wind_speed": wind_speed
    })

@login_required
def categoriesActivitesView(request):
    context={}
    player, created = Challenger.objects.get_or_create(user=request.user)
    player.save()
    categories=Category.objects.all()
    context['line_items']=getCartItems(player)
    # context['category_list'] = categories

    # for category in categories:
    #     name = getattr(category, 'name')
    #     context[name] = name

    category_counts = {}

    for category in categories:
        activities = Activity.objects.filter(cat=category)
        count = activities.count()
        category_counts[category] = count
        category.count = category_counts.get(category, 0)

    context['category_counts'] = category_counts
    print(context['category_counts'])
    return render(request, "game/activitiesCategory.html", context)
    # return render(request, "game/activitiesCategory.html", context)


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
        print(context['activity_list'])
        print(context['category'])
        # context['line_items'] = LineItem.objects.filter(cart=cart, dateRecorded = date.today()) #set up the line items
        # context['line_items'] = LineItem.objects.filter(cart=cart, checkedOut=False, dateRecorded=date.today()) #set up the line items
        test=Activity.objects.filter(id=78)

        return context


# Method to obtain the activity id and time from the user which is sent via AJAx to the server. One the sever side
# we need to get the users cart to ensure the correct line item is added to the cart.
class AddLineItem(LoginRequiredMixin, View):
     def post(self, request):
        duration=request.POST['duration']
        time=request.POST['time']
        activityId=request.POST['activityId']
        activity=get_object_or_404(Activity, id=activityId)
        player = Challenger.objects.get(user=request.user)
        cart = UserCart.objects.get(challenger=player)

        # If statement to check if line item is checked out
        if LineItem.objects.filter(dateRecorded=date.today(), checkedOut=False, activity=activity, cart=cart).exists():
            return JsonResponse({'cart_success': False}, status=200)
        elif LineItem.objects.filter(dateRecorded=date.today(), checkedOut=True, activity=activity, cart=cart).exists():
            return JsonResponse({'not_cart_success': False}, status=200)
        else:
            lineItem=LineItem(timeRecorded=time, dateRecorded=date.today(), activityDuration=duration, activity=activity, cart=cart)
            lineItem.save()
            itemId=getattr(lineItem, 'pk')
            line_item_html = render_to_string('game/lineItem.html', {'item': lineItem, 'item-id': itemId})
            return HttpResponse(line_item_html)

# Method to calculate all the points and send them to the server
# ajax doesnt have to render anything so no need for server to return anything to ajax
# just a success message will do
class RecordPoints(LoginRequiredMixin, View):
     def post(self, request):
        if request.method == 'POST':
            list_items=request.POST.getlist('list_items[]')
            print(list_items)
            player = Challenger.objects.get(user=request.user)
            postcode=getattr(player, 'postcode')
            for id in list_items:
                item=LineItem.objects.get(pk=id)
                item.checkedOut=True
                item.save()
                time=getattr(item, 'timeRecorded')
                datetime_obj = datetime.datetime.combine(date.today(), time)
                formatted_from_datetime = datetime_obj.strftime("%Y-%m-%dT%H:%MZ")
                toTime=datetime_obj+datetime.timedelta(minutes=30)
                formatted_to_datetime=toTime.strftime("%Y-%m-%dT%H:%MZ")
                print(formatted_to_datetime)
                print(formatted_from_datetime)

                # Set API header               
                headers = {
                'Accept': 'application/json'
                }
                r = requests.get(f'https://api.carbonintensity.org.uk/regional/intensity/{formatted_from_datetime}/{formatted_to_datetime}/postcode/{postcode}', params={}, headers = headers)
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
                # Here will implement dynamically changing score to assign the player with, depending on the state of the index

                match index:
                    case "very low":
                        baseScore = 40
                        bonus = random.randint(20, 80) # Random bonus for logging event, ranges are higher for the index
                        multiplier = 1.2 # Multiplier, adjust depending on other factors, hardcoded for now
                        plus=baseScore * multiplier+bonus # Base score * mp + bonus
                        print("Bonus: ", bonus, " mp: ", multiplier, " plus: ", plus)
                    case "low":
                        baseScore = 30
                        bonus = random.randint(10, 50)
                        multiplier = 1

                        plus = (baseScore * multiplier) + bonus
                        print("Bonus: ", bonus, " mp: ", multiplier, " plus: ", plus)
                    case "moderate":
                        baseScore = 20
                        bonus = random.randint(5, 20)
                        multiplier = 1

                        plus = (baseScore * multiplier) + bonus
                        print("Bonus: ", bonus, " mp: ", multiplier, " plus: ", plus)
                    case "high":
                        baseScore = 10
                        multiplier = 0.8
                        bonus = random.randint(1, 5)
                        #hi = 3
                        plus = (baseScore * multiplier) + bonus
                        print("Bonus: ", bonus, " mp: ", multiplier, " plus: ", plus)
                    case "very-high":
                        baseScore = 0
                        multiplier = 1
                        bonus = random.randint(1, 5)

                        plus = (baseScore * multiplier) + bonus
                        print("Bonus: ", bonus, " mp: ", multiplier, " plus: ", plus)

                # Get the players current score from DB
                old_score=player.score
                # Remember the activity points are added along with the plus value
                new_score=old_score + activity_point + plus
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
    context['line_items']=getCartItems(player)

    def num_lineitems(self):
        num_lineitems = LineItem.objects.all().count
        return num_lineitems

    user_top_activities = Activity.objects.filter(lineitem__cart__challenger=player) \
                .annotate(num_lineitems=Count('lineitem')) \
                .order_by('-num_lineitems')


    total_top_activities = Activity.objects.all() \
                .annotate(num_lineitems=Count('lineitem')) \
                .order_by('-num_lineitems')

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

    # Get API_KEY
    WEATHER_KEY=config('WEATHER_KEY')
    """
    Returns weather data from the OpenWeather API for the specified location, or a default location if no location is specified.
    """
    # Get the postcode parameter from the user for the API)
    location=player.postcode

    # Make an HTTP GET request to the OpenWeather API
    weather_response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?zip={location},{'GB'}&appid={WEATHER_KEY}&units=metric")

    # Extract relevant weather data from the API response
    weather_data = weather_response.json()
    temperature = weather_data["main"]["temp"]
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]

    context['temperature']=int(temperature)
    context['humidity']=humidity
    context['wind_speed']=wind_speed

    return render(request, "game/tipsIndex.html", context)

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


def emptyCart(request):
    player = Challenger.objects.get(user=request.user)
    line_items=getCartItems(player)
    line_items.delete()
    return redirect(reverse('gameapp:categories'))
        