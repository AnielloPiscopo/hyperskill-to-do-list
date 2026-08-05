from rest_framework import serializers
from django.contrib.auth.models import User

__all__ = ['InfoSerializer']

class InfoSerializer(serializers.ModelSerializer):
    """Read-only serializer that exposes basic profile information for the current user."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id', 'username', 'email']