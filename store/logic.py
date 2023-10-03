from django.db.models import Avg

from store.models import Book, UserBookRelation


def set_rating(book: Book) -> None:
    rating = (
        UserBookRelation.objects.filter(book=book)
        .aggregate(rating=Avg("rate"))
        .get("rating")
    )
    book.rating = rating
    book.save()
