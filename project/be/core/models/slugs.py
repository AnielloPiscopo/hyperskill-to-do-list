from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from core.utils import slugs
from .base import BaseModel

__all__ = ['SluggedModel']


class SluggedModel(BaseModel):
    """Abstract base for models that expose an auto-generated, renamable slug.

    Subclasses must have a `title` field and a `user` field (used to scope
    slug uniqueness). The slug regenerates whenever `title` changes; the
    previous slug is kept in SlugHistory so old URLs keep resolving.
    """

    title: str
    slug = models.SlugField(max_length=100, blank=True)
    user: User

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.pk:
            old_title: str = type(self).objects.filter(pk=self.pk).values_list('title', flat=True).first()
            if old_title is not None and old_title != self.title:
                if self.slug:
                    SlugHistory.objects.create(content_object=self, slug=self.slug)
                self.slug = slugs.generate_unique_slug(type(self), self.title, self.user, exclude_pk=self.pk)
        else:
            self.slug = slugs.generate_unique_slug(type(self), self.title, self.user)
        super().save(*args, **kwargs)


class SlugHistory(models.Model):
    """Old slugs kept so previously visited URLs keep resolving after a rename.

    Generic across any SluggedModel subclass (Board, Task, ...) via a
    content-type relation, instead of a dedicated history table per model.
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'core'
        unique_together = ('content_type', 'object_id', 'slug')