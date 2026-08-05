from typing import Any
from datetime import date
from rest_framework import serializers
from rest_framework.request import Request
from core.constants.api import validation_msg as core_msg
from core.utils import validators
from core.serializers import BaseModelSerializer
from task.constants.api import validation_msg as task_msg
from task.models import Task
from task.enums import TaskStatus, TaskPriority
from board.models import Board

__all__ = ['TaskSerializer']


class TaskSerializer(BaseModelSerializer):
    """Serializer for creating and updating tasks.

    `user` and `is_archived` are excluded because they are managed server-side.
    The `board` field accepts a PK and validates that the board belongs to the
    requesting user, preventing cross-user board assignment.
    """

    board = serializers.PrimaryKeyRelatedField(
        queryset=Board.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta(BaseModelSerializer.Meta):
        model = Task
        exclude = ['user', 'is_archived']

    def validate_title(self, title: str) -> str:  # noqa: field-level validator — DRF calls it via naming convention
        """Reject titles that are blank or contain only whitespace."""
        if not title.strip():
            raise serializers.ValidationError(core_msg.BLANK_OR_WHITESPACE)
        return title

    def validate_board(self, board: Board | None) -> Board | None:
        """Ensure the referenced board belongs to the current user."""
        if board is None:
            return board
        request: Request = self.context.get('request')
        if board.user != request.user:
            raise serializers.ValidationError(task_msg.BOARD_NOT_YOURS)
        return board

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        """Run cross-field validation for date range and priority/status constraints."""
        goal_set_date: date | None = data.get('goal_set_date')
        set_to_complete: date | None = data.get('set_to_complete')

        self._check_dates(goal_set_date, set_to_complete)

        priority: str | None = data.get('priority')
        status: str | None = data.get('status')

        self._check_priority_and_status(priority, status)

        return data

    @staticmethod
    def _check_dates(goal_set_date: date | None, set_to_complete: date | None) -> None:
        """Raise a validation error if the deadline precedes the start date.

        Both dates must be present for the check to run; partial updates that
        supply only one date are allowed through without error.
        """
        if goal_set_date is not None and set_to_complete is not None:
            if not validators.is_valid_date_range(goal_set_date, set_to_complete):
                raise serializers.ValidationError({
                    'set_to_complete': core_msg.DEADLINE_BEFORE_START
                })

    @staticmethod
    def _check_priority_and_status(priority: str | None, status: str | None) -> None:
        """Raise a validation error if a meaningful priority is set on a DONE task.

        ZERO is the only allowed priority for completed tasks because assigning
        urgency to something already finished is semantically inconsistent.
        """
        if priority is not None and priority != TaskPriority.ZERO:
            if status == TaskStatus.DONE:
                raise serializers.ValidationError({
                    'priority': task_msg.PRIORITY_NOT_ALLOWED_ON_DONE
                })
