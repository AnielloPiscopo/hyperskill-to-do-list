from rest_framework import serializers

__all__ = ['BaseModelSerializer']

class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        read_only_fields = ['id', 'created_at', 'updated_at']