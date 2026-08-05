from rest_framework import serializers
from rest_framework.request import Request
from board.models import Board
from task.constants.api import validation_msg as task_msg

__all__ = ['TaskMoveSerializer']

class TaskMoveSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField())
    board = serializers.PrimaryKeyRelatedField(
        queryset=Board.objects.all(),
        allow_null=True,
    )

    def validate_board(self, board: Board | None) -> Board | None:
        if board is None:
            return board

        request: Request = self.context.get('request')

        if board.user != request.user:
            raise serializers.ValidationError(task_msg.BOARD_NOT_YOURS)
        return board