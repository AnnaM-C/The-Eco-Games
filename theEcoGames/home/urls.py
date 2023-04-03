from django.urls import path
from . import views


app_name = "homeapp"

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.RegisterUser.as_view(), name='signup_user'),
]