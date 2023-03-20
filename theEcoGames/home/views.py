from django.shortcuts import render

# Create your views here.

# home view
def home(request):
    context = {}
    return render(request, 'home/contact.html', context)

# contact view
def contact(request):
    context = {}
    return render(request, 'home/contact.html', context)