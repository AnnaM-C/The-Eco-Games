from django.urls import path
from . import views

app_name = "gameapp" # namespace for this app

urlpatterns = [
    # Leaderboard View
    path('leaderboards', views.leaderboards, name='leaderboards'),
    # Profile View
    path('profile', views.profile, name = 'profile'),
    # Maps View
    path('maps', views.maps, name = 'maps'),
    # Activites View
    path('activities', views.activities, name = 'activities')
    
]