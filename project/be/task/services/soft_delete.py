from django.contrib.auth.models import User
from typing import Optional
from django.db.models import QuerySet
from task.models import Task

__all__ = ['archive_task', 'restore_task', 'archive_tasks', 'restore_tasks']

def _soft_delete_all(qs: QuerySet[Task], ids: Optional[list] = None, archive: bool = True) -> None:
    if ids is not None and len(ids) > 0:
        qs = qs.filter(pk__in=ids)

    for task in qs:
        archive_task(task) if archive else restore_task(task)

def archive_task(task: Task):
    task.archive()

def restore_task(task: Task):
    task.restore()

def archive_tasks(user: User, ids: Optional[list] = None) -> None:
    qs: QuerySet[Task] = Task.objects.filter(user=user, is_archived=False)

    _soft_delete_all(qs, ids)

def restore_tasks(user: User, ids: Optional[list] = None) -> None:
    qs: QuerySet[Task] = Task.objects.filter(user=user, is_archived=True)

    _soft_delete_all(qs, ids)