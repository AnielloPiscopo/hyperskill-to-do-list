from rest_framework import serializers
from core.serializers import BaseModelSerializer
from task.serializers import TaskSerializer
from board.models import Board

__all__ = ['BoardSerializer', 'BoardDetailSerializer']

class BoardSerializer(BaseModelSerializer):
    class Meta:
        model = Board
        exclude = ['user', 'is_archived']

class BoardDetailSerializer(BoardSerializer):
    tasks = serializers.SerializerMethodField()

    @staticmethod
    def get_tasks(obj):
        active_tasks = obj.tasks.filter(is_archived=False)
        return TaskSerializer(active_tasks, many=True).data

    class Meta(BoardSerializer.Meta):
        pass
