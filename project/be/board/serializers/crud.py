from collections import OrderedDict
from typing import Any

from rest_framework import serializers
from django.db import models
from drf_spectacular.utils import extend_schema_field
from core.constants.api import validation_msg
from core.utils import validators
from core.serializers import BaseModelSerializer
from task.serializers import TaskSerializer
from task.models import Task
from board.models import Board

__all__ = ['BoardSerializer', 'BoardDetailSerializer']


class BoardSerializer(BaseModelSerializer):
    """Serializer for creating and updating boards.

    `user` and `is_archived` are excluded because they are set server-side
    (user is derived from the request; archival is handled via dedicated endpoints).
    """

    class Meta(BaseModelSerializer.Meta):
        model = Board
        exclude = ['user', 'is_archived']

    def validate_color(self, color: str) -> str:  # noqa: field-level validator — DRF calls it via naming convention
        """Validate that the color is a proper 6-digit hex string and normalise it to uppercase."""
        if not validators.is_valid_hex_color(color):
            raise serializers.ValidationError(validation_msg.INVALID_HEX_COLOR)
        return color.upper()


class BoardDetailSerializer(BoardSerializer):
    """Read-only serializer that extends BoardSerializer with the board's active tasks."""

    tasks = serializers.SerializerMethodField()

    @extend_schema_field(TaskSerializer(many=True))
    def get_tasks(self, obj: Board) -> list[OrderedDict[str, Any]]:
        """Return only the non-archived tasks for the board."""
        active_tasks: models.QuerySet[Task] = obj.tasks.filter(is_archived=False)
        return TaskSerializer(active_tasks, many=True).data

    class Meta(BoardSerializer.Meta):
        pass
