from core.serializers import BaseModelSerializer
from board.models import Board

__all__ = ['BoardSerializer']

class BoardSerializer(BaseModelSerializer):
    class Meta:
        model = Board
        exclude = ['user', 'is_archived']
