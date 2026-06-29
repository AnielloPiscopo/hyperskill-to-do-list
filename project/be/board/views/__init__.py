from .crud import BoardListView, BoardDetailView
from .soft_delete import BoardArchiveView, BoardRestoreView, BoardArchiveAllView, BoardRestoreAllView

__all__ = [
    'BoardListView',
    'BoardDetailView',
    'BoardArchiveView',
    'BoardRestoreView',
    'BoardArchiveAllView',
    'BoardRestoreAllView',
]
