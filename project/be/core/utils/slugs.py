from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models import QuerySet, Model
from typing import Type, TypeVar

ModelT = TypeVar('ModelT', bound=Model)

def generate_unique_slug(
        model: Type[ModelT],
        title: str,
        user: User,
        exclude_pk: int | None = None,
        max_length: int = 100,
) -> str:
    """Generate a slug unique among this user's rows of `model`, appending -2, -3, ... on collision."""
    base: str = slugify(title)[:max_length]
    slug: str = base
    counter: int = 2
    while True:
        qs: QuerySet[ModelT] = model.objects.filter(user=user, slug=slug)
        if exclude_pk:
            qs = qs.exclude(pk=exclude_pk)
        if not qs.exists():
            return slug
        slug = f'{base}-{counter}'
        counter += 1