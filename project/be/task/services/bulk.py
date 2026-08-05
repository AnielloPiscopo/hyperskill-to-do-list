from task.models import Task
from board.models import Board

__all__ = ['move_tasks']

def move_tasks(user, ids: list[int], board: Board | None) -> None:
    Task.objects.filter(user=user, pk__in=ids).update(board=board)