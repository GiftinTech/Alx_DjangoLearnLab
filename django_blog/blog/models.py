from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Post(models.Model):
  title = models.CharField(max_length=200) # Post title
  content = models.TextField() # Post content
  published_date = models.DateTimeField(auto_now_add=True) # Set post date when created
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post') # Link to the User model

  def __str__(self):
    return self.title # Display name in admin and shell
  
   # Handy for redirects after create/update/delete (used by CBVs and templates)
  def get_absolute_url(self):
    return reverse('post-detail', kwargs={'pk': self.pk}) 