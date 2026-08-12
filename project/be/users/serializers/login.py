from rest_framework import serializers

__all__ = ['LoginRequestSerializer', 'TokenResponseSerializer']

class LoginRequestSerializer(serializers.Serializer):
    """Request payload for the login endpoint."""

    username = serializers.CharField()
    password = serializers.CharField()

class TokenResponseSerializer(serializers.Serializer):
    """Response returned after a successful login, containing the auth token."""
    token = serializers.CharField()