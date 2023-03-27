# # Forms are sourced from this file

# from django import forms


# # Charfield: Short Text Field
# # EmailField: Email Field (Valid email addresses only)

# class ContactForm(forms.Form):
#     # name = forms.CharField(required=True)
#     # subject = forms.CharField(required=True)
#     # email = forms.EmailField(required=True)
#     # message = forms.CharField(widget=forms.Textarea, required=True)

#     # Has the name formfield to allow us to modify it in base.scss
#     name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     subject = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

#     message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=True)
