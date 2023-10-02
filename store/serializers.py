from rest_framework import serializers

from store.models import Book, UserBookRelation


class BooksSerializer(serializers.ModelSerializer):
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(
        max_digits=3, decimal_places=2, read_only=True
    )

    class Meta:
        model = Book
        fields = (
            "id",
            "name",
            "price",
            "author_name",
            "annotated_likes",
            "rating",
        )


class UserBookRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ("book", "like", "in_bookmarks", "rate")
