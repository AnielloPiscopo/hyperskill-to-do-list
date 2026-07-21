from rest_framework import serializers
from django.contrib.auth.models import User

__all__ = ['InfoSerializer']

class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id', 'username', 'email']