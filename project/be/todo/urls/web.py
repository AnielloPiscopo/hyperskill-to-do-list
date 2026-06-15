from django.urls import path
from ..views import TodoDetailWebView, TodoListWebView

urlpatterns = [
    path('', TodoListWebView.as_view()),
    path('<int:pk>/', TodoDetailWebView.as_view()),
]