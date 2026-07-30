from django.db import models


__all__ = ['BaseModel']

class BaseModel(models.Model):
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def archive(self):
        self.is_archived = True
        self.save(update_fields=['is_archived', 'updated_at'])

    def restore(self):
        self.is_archived = False
        self.save(update_fields=['is_archived', 'updated_at'])