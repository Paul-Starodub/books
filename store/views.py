from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from store.models import Book
from store.serializers import BooksSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["price"]
