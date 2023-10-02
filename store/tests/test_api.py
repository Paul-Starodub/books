import json

from django.contrib.auth.models import User
from django.db.models import Count, Case, When
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="test username")
        self.book_1 = Book.objects.create(
            name="Test book_1",
            price="25",
            author_name="Author 1",
            owner=self.user,
        )
        self.book_2 = Book.objects.create(
            name="Test book_2", price="55", author_name="Author 2"
        )
        self.book_3 = Book.objects.create(
            name="Test book_3 Author 1", price="55", author_name="Author 3"
        )

    def test_get(self) -> None:
        url = reverse("book-list")
        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(relation__like=True, then=1)))
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            BooksSerializer(books, many=True).data,
            response.data,
        )

    def test_get_filter(self) -> None:
        url = reverse("book-list")
        books = Book.objects.filter(
            id__in=[self.book_2.id, self.book_3.id]
        ).annotate(
            annotated_likes=Count(Case(When(relation__like=True, then=1)))
        )
        response = self.client.get(url, data={"price": 55})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            BooksSerializer(books, many=True).data,
            response.data,
        )

    def test_get_search(self) -> None:
        url = reverse("book-list")
        books = Book.objects.filter(
            id__in=[self.book_1.id, self.book_3.id]
        ).annotate(
            annotated_likes=Count(Case(When(relation__like=True, then=1)))
        )
        response = self.client.get(url, data={"search": "Author 1"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            BooksSerializer(books, many=True).data,
            response.data,
        )

    def test_create(self) -> None:
        self.assertEqual(Book.objects.count(), 3)
        url = reverse("book-list")
        data = {"name": "Python3", "price": 150, "author_name": "Idiot"}
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(
            url, data=json_data, content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(Book.objects.last().owner, self.user)

    def test_update(self) -> None:
        url = reverse("book-detail", args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 575,
            "author_name": self.book_1.author_name,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(
            url, data=json_data, content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book_1.refresh_from_db()
        self.assertEqual(self.book_1.price, 575)

    def test_delete(self) -> None:
        self.assertEqual(Book.objects.count(), 3)
        url = reverse("book-detail", args=(self.book_1.id,))
        self.client.force_login(self.user)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)
        self.assertFalse(Book.objects.filter(id=self.book_1.id).exists())

    def test_update_not_owner(self) -> None:
        self.user2 = User.objects.create(username="test username2")

        url = reverse("book-detail", args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 575,
            "author_name": self.book_1.author_name,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(
            url, data=json_data, content_type="application/json"
        )

        self.assertEqual(
            response.data,
            {
                "detail": ErrorDetail(
                    string="You do not have permission to perform this action.",
                    code="permission_denied",
                )
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.book_1.refresh_from_db()
        self.assertEqual(self.book_1.price, 25)

    def test_update_not_owner_but_staff(self) -> None:
        self.user2 = User.objects.create(
            username="test username2", is_staff=True
        )

        url = reverse("book-detail", args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 575,
            "author_name": self.book_1.author_name,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(
            url, data=json_data, content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book_1.refresh_from_db()
        self.assertEqual(self.book_1.price, 575)


class BookRelationTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="test username")
        self.user2 = User.objects.create(username="test username2")
        self.book_1 = Book.objects.create(
            name="Test book_1",
            price="25",
            author_name="Author 1",
            owner=self.user,
        )
        self.book_2 = Book.objects.create(
            name="Test book_2", price="55", author_name="Author 2"
        )

    def test_like(self) -> None:
        url = reverse("userbookrelation-detail", args=(self.book_1.id,))
        data = {"like": True}
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(
            url, data=json_data, content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        relation = UserBookRelation.objects.get(
            user=self.user, book=self.book_1
        )
        self.assertTrue(relation.like)

        data = {"in_bookmarks": True}
        json_data = json.dumps(data)
        response = self.client.patch(
            url, data=json_data, content_type="application/json"
        )
        relation = UserBookRelation.objects.get(
            user=self.user, book=self.book_1
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(relation.in_bookmarks)

    def test_rate(self) -> None:
        url = reverse("userbookrelation-detail", args=(self.book_1.id,))
        data = {"rate": 3}
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(
            url, data=json_data, content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        relation = UserBookRelation.objects.get(
            user=self.user, book=self.book_1
        )
        self.assertEqual(relation.rate, 3)

    def test_rate_wrong(self) -> None:
        url = reverse("userbookrelation-detail", args=(self.book_1.id,))
        data = {"rate": 6}
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(
            url, data=json_data, content_type="application/json"
        )

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data
        )
