from django.urls import path
from . import views

urlpatterns = [
    # Profile View
    path('profile', views.profile, name ='profile'),
    # Leaderboard View
    path('leaderboards', views.leaderboards, name='leaderboards'),
    # Maps View
    path('maps', views.maps, name = 'maps'),
    # Activities View
    path('activities', views.createActivitiesView, name = 'activities'),
]