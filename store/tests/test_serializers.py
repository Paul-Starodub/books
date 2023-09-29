from django.test import TestCase

from store.models import Book
from store.serializers import BooksSerializer


class BooksSerializerTestCase(TestCase):
    def test_ok(self) -> None:
        book_1 = Book.objects.create(
            name="Test book_1", price="25", author_name="name1"
        )
        book_2 = Book.objects.create(
            name="Test book_2", price="55", author_name="name2"
        )
        data = BooksSerializer([book_1, book_2], many=True).data
        expected_data = [
            {
                "id": book_1.id,
                "name": "Test book_1",
                "price": "25.00",
                "author_name": "name1",
            },
            {
                "id": book_2.id,
                "name": "Test book_2",
                "price": "55.00",
                "author_name": "name2",
            },
        ]

        self.assertEqual(data, expected_data)
