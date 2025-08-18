from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import RegisterView, LoginView, follow_user, unfollow_user

urlpatterns = [
  path('register/', RegisterView.as_view(), name='register'),
  path('login/', LoginView.as_view(), name='login'),

  path("users/<int:user_id>/follow/", follow_user, name="follow-user"),
  path("users/<int:user_id>/unfollow/", unfollow_user, name="unfollow-user"),
]
