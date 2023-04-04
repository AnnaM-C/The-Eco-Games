from django.urls import path
from . import views

app_name = "gameapp"

urlpatterns = [
    # Profile View
    path('', views.profile, name ='profile'), # Change to account

    # Update Location View
    path('locationupdate', views.locationUpdateView, name = 'locationUpdater'),

    # Leaderboard View
    path('leaderboards', views.leaderboards, name='leaderboards'),

    # Maps View
    path('maps', views.maps, name = 'maps'),

    # Activities View
    path('activities', views.createActivitiesView, name = 'activities'),
    
    # Tips View
    path('tips', views.tipsIndex, name = 'tips'),
]