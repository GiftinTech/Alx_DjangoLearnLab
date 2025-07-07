from bookshelf.models import Book

# Create a Book instance

new_book = Book(title="Atomic Habits", author="James Clear", publication_year=2018)
new_book.save()

# Expected output for print(new_book): Book object (1)
