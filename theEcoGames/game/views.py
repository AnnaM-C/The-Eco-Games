from django.shortcuts import render

# Create your views here.

# contact view
def leaderboards(request):
    context = {}
    return render(request, 'game/leaderboards.html', context)

def profile(request):
    context = {}
    return render(request, 'game/profile.html', context)

def maps(request):
    context = {}
    return render(request, 'game/map.html', context)
