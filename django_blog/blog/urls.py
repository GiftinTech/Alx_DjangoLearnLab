from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import register_view, profile_view

# URL routes for authentication & profile management
urlpatterns = [
  path('', include('blog.urls')),

  # Built-in login view, using custom template
  path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
  
  # Built-in logout view, using custom template
  path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
  
  # Custom registration view
  path('register/', register_view, name='register'),
  
  # Profile page (requires login)
  path('profile/', profile_view, name='profile'),
]
