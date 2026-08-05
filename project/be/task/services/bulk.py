from task.models import Task
from board.models import Board

__all__ = ['move_tasks']

def move_tasks(user, ids: list[int], board: Board | None) -> None:
    """Reassign a list of tasks to `board`, scoped to the given user.

    Passing `board=None` detaches the tasks from any board (sets the FK to NULL).
    Uses a single bulk UPDATE query instead of iterating to keep DB round-trips minimal.
    """
    Task.objects.filter(user=user, pk__in=ids).update(board=board)