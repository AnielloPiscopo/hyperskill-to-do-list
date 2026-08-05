from django.db import models


__all__ = ['BaseModel']

class BaseModel(models.Model):
    """Abstract base model providing soft-delete (archive/restore) and audit timestamps.

    All concrete models should inherit from this class to get consistent
    lifecycle management and created/updated tracking.
    """

    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def archive(self):
        """Mark the instance as archived without deleting it from the database."""
        self.is_archived = True
        # Only touch the two relevant fields to avoid overwriting concurrent changes on other fields
        self.save(update_fields=['is_archived', 'updated_at'])

    def restore(self):
        """Revert the archived state, making the instance active again."""
        self.is_archived = False
        self.save(update_fields=['is_archived', 'updated_at'])