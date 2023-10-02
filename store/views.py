from django.db.models import Count, Case, When, Avg
from django.http import HttpRequest
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet

from store.models import Book, UserBookRelation
from store.permissions import IsOwnerOrStaffOrReadOnly
from store.serializers import BooksSerializer, UserBookRelationSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = books = Book.objects.annotate(
        annotated_likes=Count(Case(When(relation__like=True, then=1))),
        rating=Avg("relation__rate"),
    ).order_by("id")
    serializer_class = BooksSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filterset_fields = ["price"]
    search_fields = ["name", "author_name"]
    ordering_fields = ["price", "author_name"]

    def perform_create(self, serializer: Serializer) -> None:
        serializer.save(owner=self.request.user)


class UserBookRelationView(mixins.UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    lookup_field = "book"

    def get_object(self) -> None:
        obj, _ = UserBookRelation.objects.get_or_create(
            user=self.request.user, book_id=self.kwargs["book"]
        )
        return obj


def auth(request: HttpRequest):
    return render(request, "oauth.html")
