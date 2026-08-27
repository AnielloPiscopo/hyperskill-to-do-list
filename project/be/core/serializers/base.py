from rest_framework import serializers

__all__ = ['BaseModelSerializer']

class BaseModelSerializer(serializers.ModelSerializer):
    """Base serializer for all model serializers in this project.

    Enforces read-only on common audit fields and automatically strips
    leading/trailing whitespace from all string inputs before validation.
    """

    class Meta:
        # These fields are managed by the DB/model and must never be set by the client
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data: dict) -> dict:
        """Strip leading/trailing whitespace from every string field."""
        for field, value in data.items():
            if isinstance(value, str):
                data[field] = value.strip()
        return data
