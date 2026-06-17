from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from rest_framework.views import APIView
from .models import Task

__all__ = ['IsAuthorOrReadOnly']

class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj: Task) -> bool:
        if request.method in SAFE_METHODS:
            return True
        else:
            return obj.user == request.user