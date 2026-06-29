from .crud import TaskListView, TaskDetailView
from .soft_delete import TaskArchiveView, TaskRestoreView, TaskArchiveAllView, TaskRestoreAllView

__all__ = [
    'TaskListView',
    'TaskDetailView',
    'TaskArchiveView',
    'TaskRestoreView',
    'TaskArchiveAllView',
    'TaskRestoreAllView'
]
