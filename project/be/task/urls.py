from django.urls import path
from .views import (
    TaskDetailView,
    TaskListView,
    TaskArchiveView,
    TaskRestoreView,
    TaskRestoreAllView,
    TaskArchiveAllView,
    TaskMoveView,
    TaskDestroyAllView,
)

urlpatterns = [
    path('', TaskListView.as_view()),
    path('<int:pk>/', TaskDetailView.as_view()),
    path('archive-all/', TaskArchiveAllView.as_view()),
    path('restore-all/', TaskRestoreAllView.as_view()),
    path('<int:pk>/archive/', TaskArchiveView.as_view()),
    path('<int:pk>/restore/', TaskRestoreView.as_view()),
    path('move/', TaskMoveView.as_view()),
    path('delete-all/', TaskDestroyAllView.as_view()),
]
