from django.shortcuts import render
from relationship_app.models import Book, Library
from django.views.generic.detail import DetailView

# Create your views here.
# function based view
def list_books(request):
  books = Book.objects.all()
  context = {'list_books': books}

  return render(request, 'relationship_app/list_books.html', context)

# class based view
class LibraryDetails(DetailView):
	model = Library
	template_name = 'relationship_app/library_detail.html'
	context_object_name = 'library'