from typing import Optional
from django.contrib.auth.models import User
from django.db.models import QuerySet
from board.models import Board

__all__ = ['delete_boards']

def delete_boards(user: User, ids: Optional[list[int]] = None) -> None:
    """Permanently delete archived boards owned by `user`, or only those matching `ids`.

    Only archived boards are eligible for deletion — active boards are never
    touched by this function, consistent with the single-board delete constraint.
    """
    qs: QuerySet[Board] = Board.objects.filter(user=user, is_archived=True)
    if ids is not None and len(ids) > 0:
        qs = qs.filter(pk__in=ids)
    qs.delete()