from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from .models import *
from django.views.generic import ListView, CreateView, DetailView
from .forms import ActivityForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

# contact view
def leaderboards(request):
    context = {}
    return render(request, 'game/leaderboards.html', context)

@login_required
def profile(request):
    context = {}

    currentUser = request.user

    context["currentUser"] = currentUser

    return render(request, 'game/profile.html', context)

def maps(request):
    context = {}
    return render(request, 'game/map.html', context)


# def activities(request):
    # context = {}

    # # get time from post variable
    # time= POST['time']

    # # add time to api string and store the json in a results variable
    # result = 

    # # get the carbon index, need to parse data
    # index = 

    # # get the users id

    # # update the users points in database



    # return render(request, 'game/activities.html', context)

class CreateActivitiesView(LoginRequiredMixin, CreateView):
 model = Activity
 form_class = ActivityForm
 template_name = "game/activities.html"
 def get_initial(self): 
  # set the initial value of our event field
  activity = Activity.objects.get(id=self.kwargs['nid'])
  return {'activity': activity}
 def get_success_url(self): 
  # redirect to the event detail view on success
  return reverse_lazy('events_detail', kwargs={'pk':self.kwargs['nid']})

