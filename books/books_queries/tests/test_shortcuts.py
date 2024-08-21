from datetime import datetime
from decimal import Decimal

from django.test import TestCase
from faker import Faker

from books_queries.models import Author, Book, BookSale
from books_queries.shortcuts import get_books_after_date, get_authors_with_most_books, get_authors_profits, \
    get_python_books


class GetBooksAfterDateTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        fake = Faker('ru_RU')
        fake_author = Author.objects.create(name=fake.name(), email=fake.email())

        cls.fake_books_after_date = Book.objects.bulk_create([
            Book(
                title=fake.text(max_nb_chars=200),
                author=fake_author,
                publication_date=datetime(2024, 1, 1),
                price=25,
                is_available=True,
            ) for _ in range(2)
        ])

    def test_get_books_after_date(self):
        books_after_date = get_books_after_date()
        self.assertCountEqual(books_after_date, self.fake_books_after_date)


class GetAuthorsWithMostBooksTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        fake = Faker('ru_RU')
        cls.author_with_most_books = Author.objects.create(name=fake.name(), email=fake.email())
        cls.author_with_most_books_2 = Author.objects.create(name=fake.name(), email=fake.email())
        cls.author_with_less_books = Author.objects.create(name=fake.name(), email=fake.email())
        cls.author_with_no_books = Author.objects.create(name=fake.name(), email=fake.email())

        Book.objects.bulk_create([
            Book(
                title=fake.text(max_nb_chars=200),
                author=cls.author_with_most_books,
                publication_date=datetime(2024, 1, 1),
                price=25,
                is_available=True,
             ) for _ in range(5)
        ])

        Book.objects.bulk_create([
            Book(
                title=fake.text(max_nb_chars=200),
                author=cls.author_with_most_books_2,
                publication_date=datetime(2024, 1, 1),
                price=25,
                is_available=True,
             ) for _ in range(5)
        ])

        Book.objects.bulk_create([
            Book(
                title=fake.text(max_nb_chars=200),
                author=cls.author_with_less_books,
                publication_date=datetime(2024, 1, 1),
                price=25,
                is_available=True,
             ) for _ in range(2)
        ])

    def test_get_authors_with_most_books(self):
        authors_with_most_books = get_authors_with_most_books()
        self.assertCountEqual(authors_with_most_books, [self.author_with_most_books, self.author_with_most_books_2])


class GetAuthorsProfitsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        fake = Faker('ru_RU')
        author = Author.objects.create(name=fake.name(), email=fake.email())
        book = Book.objects.create(
            title=fake.text(max_nb_chars=200),
            author=author,
            publication_date=datetime(2024, 1, 1),
            price=25,
            is_available=True,
        )
        cls.book_sale = BookSale.objects.create(
            book=book,
            quantity=2,
            sale_date=datetime(2024, 1, 1),
        )

    def test_get_authors_profits(self):
        authors_with_profits = get_authors_profits()
        self.assertEqual(authors_with_profits[0]['total_profit'], Decimal(50))


class GetPythonBooksTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        fake = Faker('ru_RU')
        author = Author.objects.create(name=fake.name(), email=fake.email())
        cls.python_book = Book.objects.create(
            title='Python Book',
            author=author,
            publication_date=datetime(2024, 1, 1),
            price=25,
            is_available=True,
        )
        cls.not_python_book = Book.objects.create(
            title='Java Book',
            author=author,
            publication_date=datetime(2024, 1, 1),
            price=25,
            is_available=True,
        )

    def test_get_python_books(self):
        python_books = get_python_books()
        self.assertIn(self.python_book, python_books)
        self.assertNotIn(self.not_python_book, python_books)

