from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class UserCreationWithEmailForm(UserCreationForm): 
    email = forms.EmailField(required=True, label='Email')
    class Meta:
        model = User
        fields = ("username", "email")
        User._meta.get_field('email')._unique = True

class ContactForm(forms.Form):
    # name = forms.CharField(required=True)
    # subject = forms.CharField(required=True)
    # email = forms.EmailField(required=True)
    # message = forms.CharField(widget=forms.Textarea, required=True)

    # Has the name formfield to allow us to modify it in base.scss
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=True)