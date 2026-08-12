from rest_framework import serializers

__all__ = ['TokenResponseSerializer']

class TokenResponseSerializer(serializers.Serializer):
    """Response returned after a successful login, containing the auth token."""
    token = serializers.CharField()