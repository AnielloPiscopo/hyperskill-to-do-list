from .base import BaseModelSerializer

__all__ = ['SlugModelSerializer']


class SlugModelSerializer(BaseModelSerializer):
    """Base serializer for models that expose an auto-generated slug field."""

    class Meta(BaseModelSerializer.Meta):
        read_only_fields = BaseModelSerializer.Meta.read_only_fields + ['slug']