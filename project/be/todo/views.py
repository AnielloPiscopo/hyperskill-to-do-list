from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Todo
from .serializers import TodoSerializer
from .permissions import IsAuthorOrReadOnly

__all__ = ['TodoDetailView', 'TodoListView']

class TodoListView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        return Todo.objects.all().order_by('is_completed', 'set_to_complete', 'goal_set_date')

    def perform_create(self, serializer) -> None:
        serializer.save(todo_of=self.request.user)

class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]