from django.urls import path
from .views import list_books
from . import views

urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetails.as_view(), name='library_detail'),
]