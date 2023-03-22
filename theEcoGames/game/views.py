from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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


def activities(request):
    context = {}
    return render(request, "game/activities.html", context)
