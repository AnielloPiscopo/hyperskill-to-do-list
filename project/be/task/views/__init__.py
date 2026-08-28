from .crud import TaskListView, TaskDetailView
from .soft_delete import TaskArchiveView, TaskRestoreView, TaskArchiveAllView, TaskRestoreAllView
from .bulk import TaskMoveView, TaskDestroyAllView

__all__ = [
    'TaskListView',
    'TaskDetailView',
    'TaskArchiveView',
    'TaskRestoreView',
    'TaskArchiveAllView',
    'TaskRestoreAllView',
    'TaskMoveView',
    'TaskDestroyAllView'
]
