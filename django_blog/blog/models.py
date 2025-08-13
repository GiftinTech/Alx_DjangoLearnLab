from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
  title = models.CharField(max_length=200) # Post title
  content = models.TextField() # Post content
  published_date = models.DateTimeField(auto_now_add=True) # Set post date when created
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post') # Link to the User model

  def __str__(self):
    return self.title # Display name in admin and shell