from rest_framework import serializers
from core.serializers import BaseModelSerializer
from task.models import Task

__all__ = ['TaskSerializer']


class TaskSerializer(BaseModelSerializer):
    class Meta:
        model = Task
        exclude = ['user', 'is_archived']

    def validate_board(self, board):
        if board is None:
            return board
        request = self.context.get('request')
        if board.user != request.user:
            raise serializers.ValidationError('This board does not belong to you.')
        return board
