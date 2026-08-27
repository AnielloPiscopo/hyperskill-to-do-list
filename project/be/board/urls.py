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
    path('archive-all/', BoardArchiveAllView.as_view()),
    path('restore-all/', BoardRestoreAllView.as_view()),
    path('<slug:slug>/', BoardDetailView.as_view()),
    path('<slug:slug>/archive/', BoardArchiveView.as_view()),
    path('<slug:slug>/restore/', BoardRestoreView.as_view()),
]