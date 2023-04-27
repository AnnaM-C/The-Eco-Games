from django import forms 
from .models import *
import random
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
# from django import forms 
# from .models import *
# # import random

# # TO DO: reshuffle everytime app is launched or reshuffle everytime page is reloaded in view? I have functionality for both
# # PROS and CONS
# # Filtering in form; advantage is if user comes back to page it won't change; disadvantage is won't get variety
# # Filtering in view; advantage is that user is presented with other options more frequently

# class UserActivityForm(forms.ModelForm):

#     # items = list(Activity.objects.all())

#     # random_items = random.sample(items, 3)

#     # queryset=Activity.objects.filter(id__in=[getattr(id,'id') for id in random_items])

#     activities = forms.ModelMultipleChoiceField(queryset=Activity.objects.all(),widget=forms.CheckboxSelectMultiple)
    
    
#     # create meta class

#     class Meta:

        # model = ActivityLog
        # fields = ['date', 'challenger', 'activities']
        # widgets= {
        #     'challenger': forms.HiddenInput(),
        # }
        # date=forms.DateField()

postcodeRegex = RegexValidator("[A-Z]{2}[0-9]{2}|[A-Z]{2}[0-9]|[A-Z]{1}[0-9]{2}\Z|[A-Z]{1}[0-9]{1}\Z", "Must be a valid postcode!") 


class locationUpdateForm(forms.ModelForm):

    postcode = forms.CharField(validators=[postcodeRegex], max_length=4)

    class Meta:
        
        model = Challenger
        fields = ['postcode']

        widgets = {
            'postcode': forms.TextInput(attrs={
            'class': 'form-control', # Bootstrap and all
            'placeholder': 'Enter your postcode:',
            }),
        }

        
#         model = ActivityLog
#         fields = ['date', 'challenger', 'activities']
#         widgets= {
#             'challenger': forms.HiddenInput(),
#         }
#         date=forms.DateField()




# New registration page with postcode field

# [A-Z]{2}[0-9]{2} - eg. RG40
# 




# class registrationForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     postcode = forms.CharField(required=True, max_length=4, validators=[postcodeRegex])

#     def save(self, commit=True):
#         #instance = super().save(commit=True)
#         challenger = Challenger(user=instance, postcode = self.cleaned_data['postcode'])
#         challenger.save()

#         instance.email = self.cleaned_data["email"]
        
#         return instance


class registrationForm(UserCreationForm):
    username = forms.CharField(label = 'Username', min_length=5, max_length=20)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    postcode = forms.CharField(required=True, max_length=4, validators=[postcodeRegex])

    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username

    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError("Email Already Exist")  
        return email

    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  

    def save(self, commit = True):  
        user = User.objects.create_user(  
            self.cleaned_data['username'],  
            self.cleaned_data['email'],  
            self.cleaned_data['password1']  
        )

        challenger = Challenger(user=user, postcode = self.cleaned_data['postcode'])
        challenger.save()


        return user