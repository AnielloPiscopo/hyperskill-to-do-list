from typing import Optional
from django.contrib.auth.models import User
from django.db.models import QuerySet
from board.models import Board

__all__ = ['archive_board', 'restore_board', 'archive_boards', 'restore_boards']


def _soft_delete_all(qs: QuerySet[Board], ids: Optional[list[int]] = None,
                     restore_tasks: bool = False, archive: bool = True) -> None:
    """Apply archive or restore to every board in `qs`, optionally filtered by `ids`.

    Iterates instead of using a bulk queryset update so that `archive_board` /
    `restore_board` logic (including cascading to tasks) is executed per board.
    """
    if ids is not None and len(ids) > 0:
        qs = qs.filter(pk__in=ids)

    for board in qs:
        archive_board(board) if archive else restore_board(board, restore_tasks=restore_tasks)


def archive_board(board: Board) -> None:
    """Archive a single board and cascade archival to all its tasks."""
    board.archive()
    board.tasks.update(is_archived=True)


def restore_board(board: Board, restore_tasks: bool = False) -> None:
    """Restore a single board and optionally restore its previously archived tasks.

    When `restore_tasks` is False only the board itself is restored; tasks that
    were archived independently of the board are left untouched.
    """
    board.restore()
    if restore_tasks:
        board.tasks.filter(is_archived=True).update(is_archived=False)


def archive_boards(user: User, ids: Optional[list[int]] = None) -> None:
    """Archive all active boards owned by `user`, or only those matching `ids`."""
    qs: QuerySet[Board] = Board.objects.filter(user=user, is_archived=False)

    _soft_delete_all(qs=qs, ids=ids)


def restore_boards(user: User, ids: Optional[list[int]] = None, restore_tasks: bool = False) -> None:
    """Restore all archived boards owned by `user`, or only those matching `ids`.

    Pass `restore_tasks=True` to also restore tasks that were archived together
    with their board.
    """
    qs: QuerySet[Board] = Board.objects.filter(user=user, is_archived=True)

    _soft_delete_all(qs=qs, ids=ids, restore_tasks=restore_tasks, archive=False)
