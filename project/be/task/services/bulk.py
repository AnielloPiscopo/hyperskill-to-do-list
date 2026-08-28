from typing import Optional
from django.contrib.auth.models import User
from django.db.models import QuerySet
from task.models import Task
from board.models import Board

__all__ = ['move_tasks', 'delete_tasks']

def move_tasks(user, ids: list[int], board: Board | None) -> None:
    """Reassign a list of tasks to `board`, scoped to the given user.

    Passing `board=None` detaches the tasks from any board (sets the FK to NULL).
    Uses a single bulk UPDATE query instead of iterating to keep DB round-trips minimal.
    """
    Task.objects.filter(user=user, pk__in=ids).update(board=board)

def delete_tasks(user: User, ids: Optional[list[int]] = None) -> None:
    """Permanently delete archived tasks owned by `user`, or only those matching `ids`."""
    qs: QuerySet[Task] = Task.objects.filter(user=user, is_archived=True)
    if ids is not None and len(ids) > 0:
        qs = qs.filter(pk__in=ids)
    qs.delete()