from django import forms 
from .models import *
import random

# TO DO: reshuffle everytime app is launched or reshuffle everytime page is reloaded? I have functionality for both

class UserActivityForm(forms.ModelForm):

    # items = list(Activity.objects.all())

    # random_items = random.sample(items, 3)

    # queryset=Activity.objects.filter(id__in=[getattr(id,'id') for id in random_items])

    activities = forms.ModelMultipleChoiceField(queryset=Activity.objects.all(),widget=forms.CheckboxSelectMultiple)
    
    # create meta class

    class Meta:

        model = ActivityLog
        fields = ['date', 'challenger', 'activities']
        widgets= {
            'challenger': forms.HiddenInput(),
        }
        date=forms.DateField()
