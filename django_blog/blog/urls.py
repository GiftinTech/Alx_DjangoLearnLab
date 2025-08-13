from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, profile_view, PostListView,PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

# URL routes for authentication & profile management
urlpatterns = [
  # Built-in login view, using custom template
  path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
  
  # Built-in logout view, using custom template
  path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
  
  # Custom registration view
  path('register/', register_view, name='register'),
  
  # Profile page (requires login)
  path('profile/', profile_view, name='profile'),

  # /posts/ → list
  path("posts/", PostListView.as_view(), name="post-list"),
  # /posts/new/ → create
  path("posts/new/", PostCreateView.as_view(), name="post-create"),
  # /posts/<pk>/ → detail
  path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
  # /posts/<pk>/edit/ → update
  path("posts/<int:pk>/edit/", PostUpdateView.as_view(), name="post-update"),
  # /posts/<pk>/delete/ → delete
  path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
]
