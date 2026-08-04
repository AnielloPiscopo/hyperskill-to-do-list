from rest_framework import serializers

__all__ = ['BulkIdsSerializer']


class BulkIdsSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text='List of ids to process. If empty or omitted, applies to all.'
    )