from django.db.models import QuerySet

__all__ = ['UserScopedQuerysetMixin']

class UserScopedQuerysetMixin:
    """Mixin that scopes the view's queryset to the currently authenticated user.

    Subclasses must implement `get_user_queryset()` to return the filtered
    queryset. This mixin also handles the drf-spectacular schema generation
    edge case where a fake view is used during introspection.
    """

    queryset: QuerySet

    def get_queryset(self):
        # drf-spectacular sets `swagger_fake_view = True` during schema introspection;
        # returning an empty queryset prevents unintended DB queries at schema build time.
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.model.objects.none()
        return self.get_user_queryset()

    def get_user_queryset(self):
        """Return the queryset filtered to the current user. Must be implemented by subclasses."""
        raise NotImplementedError('Subclasses must implement get_user_queryset()')