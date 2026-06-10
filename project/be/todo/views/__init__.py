from .web import TodoListView as TodoListWebView, TodoDetailView as TodoDetailWebView
from .api import TodoListView as TodoListApiView, TodoDetailView as TodoDetailApiView


__all__ = ['TodoListWebView', 'TodoDetailWebView', 'TodoListApiView', 'TodoDetailApiView']