# Retrieve and delete the book

new_book = Book.objects.get(title="Nineteen Eighty-Four")
new_book.delete()

# (1, {'bookshelf.Book': 1})

# Confirm deletion

Book.objects.all() # Expected output: <QuerySet []>
