from rest_framework import serializers

__all__ = ['BulkIdsSerializer']


class BulkIdsSerializer(serializers.Serializer):
    """Serializer for bulk operations that accept an optional list of integer IDs.

    When `ids` is omitted or empty the corresponding service function is
    expected to apply the operation to all eligible objects owned by the user.
    """

    ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text='List of ids to process. If empty or omitted, applies to all.'
    )