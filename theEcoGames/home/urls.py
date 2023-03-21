from django.urls import path
from . import views

app_name = "homeapp" # namespace for this app

urlpatterns = [
    path('', views.home, name='home'),
    path('contact', views.contact, name='contact'),
]