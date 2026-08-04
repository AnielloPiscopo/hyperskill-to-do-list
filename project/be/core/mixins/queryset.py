from django.db.models import QuerySet

__all__ = ['UserScopedQuerysetMixin']

class UserScopedQuerysetMixin:
    queryset: QuerySet

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.model.objects.none()
        return self.get_user_queryset()

    def get_user_queryset(self):
        raise NotImplementedError('Subclasses must implement get_user_queryset()')