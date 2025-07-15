from django.urls import path
from .views import book_list
from . import views

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('library/<int:pk>/', views.LibraryDetails.as_view(), name='library_detail'),


]