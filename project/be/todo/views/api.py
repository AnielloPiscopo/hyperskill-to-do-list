from rest_framework import generics
from ..models import Todo
from ..serializers import TodoSerializer

__all__ = ['TodoDetailView', 'TodoListView']

class TodoListView(generics.ListAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all().order_by('is_completed', 'set_to_complete', 'goal_set_date')

class TodoDetailView(generics.RetrieveAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()