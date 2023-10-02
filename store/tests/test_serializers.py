from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BooksSerializerTestCase(TestCase):
    def test_ok(self) -> None:
        user1 = User.objects.create(username="user1")
        user2 = User.objects.create(username="user2")
        user3 = User.objects.create(username="user3")
        book_1 = Book.objects.create(
            name="Test book_1", price="25", author_name="name1"
        )
        book_2 = Book.objects.create(
            name="Test book_2", price="55", author_name="name2"
        )
        UserBookRelation.objects.create(
            user=user1, book=book_1, like=True, rate=5
        )
        UserBookRelation.objects.create(
            user=user2, book=book_1, like=True, rate=5
        )
        UserBookRelation.objects.create(
            user=user3, book=book_1, like=True, rate=4
        )

        UserBookRelation.objects.create(
            user=user1, book=book_2, like=True, rate=3
        )
        UserBookRelation.objects.create(
            user=user2, book=book_2, like=True, rate=4
        )
        UserBookRelation.objects.create(user=user3, book=book_2, like=False)

        books = Book.objects.annotate(
            annotated_likes=Count(Case(When(relation__like=True, then=1))),
            rating=Avg("relation__rate"),
        ).order_by("id")
        data = BooksSerializer(books, many=True).data
        expected_data = [
            {
                "id": book_1.id,
                "name": "Test book_1",
                "price": "25.00",
                "author_name": "name1",
                "annotated_likes": 3,
                "rating": "4.67",
            },
            {
                "id": book_2.id,
                "name": "Test book_2",
                "price": "55.00",
                "author_name": "name2",
                "annotated_likes": 2,
                "rating": "3.50",
            },
        ]

        self.assertEqual(data, expected_data)
