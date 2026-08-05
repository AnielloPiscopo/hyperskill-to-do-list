from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from rest_framework.views import APIView

__all__ = ['IsAuthorOrReadOnly']

class IsAuthorOrReadOnly(BasePermission):
    """Allow read-only access to any authenticated request; write access only to the object's owner.

    Assumes the model has a `user` FK pointing to the Django auth User model.
    """

    def has_object_permission(self, request: Request, view: APIView, obj) -> bool:
        """Return True for safe methods, or if the requester is the object's owner."""
        if request.method in SAFE_METHODS:
            return True
        else:
            return obj.user == request.user