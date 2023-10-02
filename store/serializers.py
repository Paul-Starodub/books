from rest_framework import serializers

from store.models import Book, UserBookRelation


class BooksSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    annotated_likes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = (
            "id",
            "name",
            "price",
            "author_name",
            "likes_count",
            "annotated_likes",
        )

    #  additional query to db
    def get_likes_count(self, instance: Book) -> UserBookRelation:
        return UserBookRelation.objects.filter(
            book=instance, like=True
        ).count()


class UserBookRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ("book", "like", "in_bookmarks", "rate")
