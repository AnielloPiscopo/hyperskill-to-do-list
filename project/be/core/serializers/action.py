from rest_framework import serializers

__all__ = ['SimpleMessageResponseSerializer']


class SimpleMessageResponseSerializer(serializers.Serializer):
    """Generic response containing a human-readable message, used for
    action endpoints that don't return a resource (e.g. archive, restore)."""

    detail = serializers.CharField()