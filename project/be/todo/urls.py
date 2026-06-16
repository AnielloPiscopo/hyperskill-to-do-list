from django.urls import path
from .views import TodoDetailView, TodoListView

urlpatterns = [
    path('tasks/', TodoListView.as_view()),
    path('tasks/<int:pk>/', TodoDetailView.as_view()),
]