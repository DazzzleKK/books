from datetime import datetime

from django.db.models import Count, Max, Sum, F

from .models import Author, Book, BookSale


def get_books_after_date():
    return Book.objects.filter(
        publication_date__gt=datetime(2023, 1, 1),
        is_available=True,
        price__lt=30,
    )


def get_authors_with_most_books():
    authors_with_books_count = Author.objects.annotate(book_count=Count('book'))
    max_book_count = authors_with_books_count.aggregate(max_count=Max('book_count'))['max_count']
    return authors_with_books_count.filter(book_count=max_book_count)


def get_authors_profits():
    return Author.objects.annotate(
        total_profit=Sum(F('book__booksale__quantity') * F('book__price')),
    ).values('name', 'total_profit')


def get_python_books():
    return Book.objects.filter(title__icontains='python')
