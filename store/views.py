from django.http import HttpRequest
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

from store.models import Book
from store.serializers import BooksSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsAuthenticated]
    filterset_fields = ["price"]
    search_fields = ["name", "author_name"]
    ordering_fields = ["price", "author_name"]


def auth(request: HttpRequest):
    return render(request, "oauth.html")
