from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.book_1 = Book.objects.create(
            name="Test book_1", price="25", author_name="Author 1"
        )
        self.book_2 = Book.objects.create(
            name="Test book_2", price="55", author_name="Author 2"
        )
        self.book_3 = Book.objects.create(
            name="Test book_3 Author 1", price="55", author_name="Author 3"
        )

    def test_get(self) -> None:
        url = reverse("book-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            BooksSerializer(
                [self.book_1, self.book_2, self.book_3], many=True
            ).data,
            response.data,
        )

    def test_get_filter(self) -> None:
        url = reverse("book-list")
        response = self.client.get(url, data={"price": 55})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            BooksSerializer([self.book_2, self.book_3], many=True).data,
            response.data,
        )

    def test_get_search(self) -> None:
        url = reverse("book-list")
        response = self.client.get(url, data={"search": "Author 1"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            BooksSerializer([self.book_1, self.book_3], many=True).data,
            response.data,
        )
