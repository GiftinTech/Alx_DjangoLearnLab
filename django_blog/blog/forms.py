from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

""" 
  Custom registration form extending Django's built-in UserCreationForm
  Adds an email field and keeps password handling secure by default
"""
class RegisterForm(UserCreationForm):
  email = forms.EmailField(required=True) # Require an email address

  class Meta:
    model = User
     # Fields shown in the registration form
    fields = ['username', 'email', 'password1', 'password2']
