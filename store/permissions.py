from django.contrib.auth.models import User
from django.http import HttpRequest
from django.views import View
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrStaffOrReadOnly(BasePermission):
    def has_object_permission(
        self, request: HttpRequest, view: View, obj: User
    ) -> bool:
        return bool(
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and (obj.owner == request.user or request.user.is_staff)
        )
