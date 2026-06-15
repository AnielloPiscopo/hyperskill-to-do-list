from django.urls import path
from ..views import TodoDetailApiView, TodoListApiView

urlpatterns = [
    path('tasks/', TodoListApiView.as_view()),
    path('tasks/<int:pk>/', TodoDetailApiView.as_view()),
]