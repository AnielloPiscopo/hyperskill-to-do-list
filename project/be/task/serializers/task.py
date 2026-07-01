from typing import Any
from datetime import date
from rest_framework import serializers
from core.constants.api import validation_msg as core_msg
from core.utils import validators
from core.serializers import BaseModelSerializer
from task.constants.api import validation_msg as task_msg
from task.models import Task
from board.models import Board

__all__ = ['TaskSerializer']


class TaskSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Task
        exclude = ['user', 'is_archived']

    def validate_title(self, title: str) -> str: # noqa
        if not title.strip():
            raise serializers.ValidationError(core_msg.BLANK_OR_WHITESPACE)
        return title

    def validate_board(self, board: Board | None) -> Board | None:
        if board is None:
            return board
        request = self.context.get('request')
        if board.user != request.user:
            raise serializers.ValidationError(task_msg.BOARD_NOT_YOURS)
        return board

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        goal_set_date: date = data.get('goal_set_date')
        set_to_complete: date = data.get('set_to_complete')

        if goal_set_date is not None and set_to_complete is not None:
            if not validators.is_valid_date_range(goal_set_date, set_to_complete):
                raise serializers.ValidationError({
                    'set_to_complete': core_msg.DEADLINE_BEFORE_START
                })

        return data
