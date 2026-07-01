from collections import OrderedDict
from typing import Any

from rest_framework import serializers
from core.utils import validators
from core.serializers import BaseModelSerializer
from task.serializers import TaskSerializer
from board.models import Board

__all__ = ['BoardSerializer', 'BoardDetailSerializer']


class BoardSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Board
        exclude = ['user', 'is_archived']

    def validate_color(self, color: str) -> str: # noqa
        if not validators.is_valid_hex_color(color):
            raise serializers.ValidationError('Color must be a valid hex color code (e.g. #FF0000).')
        return color.upper()


class BoardDetailSerializer(BoardSerializer):
    tasks = serializers.SerializerMethodField()

    @staticmethod
    def get_tasks(obj: Board) -> list[OrderedDict[str, Any]]:
        active_tasks = obj.tasks.filter(is_archived=False)
        return TaskSerializer(active_tasks, many=True).data

    class Meta(BoardSerializer.Meta):
        pass
