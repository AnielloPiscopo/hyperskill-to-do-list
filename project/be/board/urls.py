from django.urls import path
from .views import (
    BoardDetailView,
    BoardListView,
    BoardRestoreView,
    BoardArchiveView,
    BoardRestoreAllView,
    BoardArchiveAllView)

urlpatterns = [
    path('', BoardListView.as_view()),
    path('<int:pk>/', BoardDetailView.as_view()),
    path('<int:pk>/archive/', BoardArchiveView.as_view()),
    path('<int:pk>/restore/', BoardRestoreView.as_view()),
    path('archive-all/', BoardArchiveAllView.as_view()),
    path('restore-all/', BoardRestoreAllView.as_view()),
]