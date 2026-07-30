from typing import Optional
from django.contrib.auth.models import User
from django.db.models import QuerySet
from board.models import Board

__all__ = ['archive_board', 'restore_board', 'archive_boards', 'restore_boards']


def _soft_delete_all(qs: QuerySet[Board], ids: Optional[list[int]] = None,
                     restore_tasks: bool = False, archive: bool = True) -> None:
    if ids is not None and len(ids) > 0:
        qs = qs.filter(pk__in=ids)

    for board in qs:
        archive_board(board) if archive else restore_board(board, restore_tasks=restore_tasks)


def archive_board(board: Board) -> None:
    board.archive()
    board.tasks.update(is_archived=True)


def restore_board(board: Board, restore_tasks: bool = False) -> None:
    board.restore()
    if restore_tasks:
        board.tasks.filter(is_archived=True).update(is_archived=False)


def archive_boards(user: User, ids: Optional[list[int]] = None) -> None:
    qs: QuerySet[Board] = Board.objects.filter(user=user, is_archived=False)

    _soft_delete_all(qs=qs, ids=ids)


def restore_boards(user: User, ids: Optional[list[int]] = None, restore_tasks: bool = False) -> None:
    qs: QuerySet[Board] = Board.objects.filter(user=user, is_archived=True)

    _soft_delete_all(qs=qs, ids=ids, restore_tasks=restore_tasks, archive=False)
