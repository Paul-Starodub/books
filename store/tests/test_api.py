from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
    def test_get(self) -> None:
        book_1 = Book.objects.create(name="Test book_1", price="25")
        book_2 = Book.objects.create(name="Test book_2", price="55")
        url = reverse("book-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            BooksSerializer([book_1, book_2], many=True).data, response.data
        )
