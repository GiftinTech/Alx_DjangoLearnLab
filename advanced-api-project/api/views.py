from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import generics, viewsets
from django_filters import rest_framework as filters 
from rest_framework.filters import SearchFilter, OrderingFilter 
from .models import Book
from .serializers import BookSerializer

# Create your views here.

class ListView(generics.ListAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  permission_classes = [IsAuthenticatedOrReadOnly]

  """Makes sure filters.OrderingFilter & filters.SearchFilter are included when required"""

  filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
  filterset_fields = ['title', 'author', 'publication_year']  # Filter fields
  search_fields = ['title', 'author']  # Search fields
  ordering_fields = ['title', 'publication_year']  # Ordering fields

"""  
  - ListView supports filtering by title, author and publication year
  - Search is enabled on the title and author fields
  - Ordering is enabled by title and publication year
"""

class DetailView(viewsets.ModelViewSet):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  permission_classes = [IsAuthenticatedOrReadOnly]

class CreateView(viewsets.ModelViewSet):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  permission_classes = [IsAuthenticated]


class UpdateView(viewsets.ModelViewSet):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  permission_classes = [IsAuthenticated]


class DeleteView(viewsets.ModelViewSet):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  permission_classes = [IsAuthenticated]

 