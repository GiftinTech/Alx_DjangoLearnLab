from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post

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

# ModelForm used for both Create & Update
# - Only exposes title & content; author is set in the view based on the logged-in user.
class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ["title", "content"]
    widgets = {
      "title": forms.TextInput(attrs={"placeholder": "Post title"}),
      "content": forms.Textarea(attrs={"rows": 8, "placeholder": "Write your post..."}),
    }