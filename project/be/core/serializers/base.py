from rest_framework import serializers

__all__ = ['BaseModelSerializer']

class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data: dict) -> dict:
        for field, value in data.items():
            if isinstance(value, str):
                data[field] = value.strip()
        return data