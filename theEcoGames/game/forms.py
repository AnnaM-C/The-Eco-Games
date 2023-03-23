from django import forms 
from .models import *

class ActivityForm(forms.ModelForm):
    # create meta class
    class Meta:
    # specify model to be used
        model = Activity
        fields = ['title', 'description', 'date', 'author']
        widgets = {
            'title': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Event Title',
            }),
            'description': forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Event Description',
            'rows' : 25,
            'cols' : 60,
            }),
            'date': forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': 'yyyy-mm-dd',
            }),
            'author': forms.HiddenInput(),
        }