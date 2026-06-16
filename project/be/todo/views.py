from django.db.models import QuerySet
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Todo
from .serializers import TodoSerializer
from .permissions import IsAuthorOrReadOnly

__all__ = ['TodoDetailView', 'TodoListView']

class TodoListView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='List all tasks',
        operation_description='Returns all tasks ordered by completion status, deadline and creation date.',
        tags=['tasks'],
        responses={
            200: TodoSerializer(many=True),
            403: 'Authentication credentials were not provided.'
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Create a new task',
        operation_description='Creates a new task. The author is automatically set to the logged in user.',
        tags=['tasks'],
        responses={
            201: TodoSerializer,
            400: 'Bad request — invalid data.',
            403: 'Authentication credentials were not provided.'
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet:
        return Todo.objects.all().order_by('is_completed', 'set_to_complete', 'goal_set_date')

    def perform_create(self, serializer) -> None:
        serializer.save(todo_of=self.request.user)

class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    @swagger_auto_schema(
        operation_summary='Retrieve a task',
        operation_description='Returns the details of a specific task by its ID.',
        tags=['tasks'],
        responses={
            200: TodoSerializer,
            403: 'Authentication credentials were not provided.',
            404: 'Task not found.'
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Update a task',
        operation_description='Fully updates a task. Only the author can update it.',
        tags=['tasks'],
        responses={
            200: TodoSerializer,
            400: 'Bad request — invalid data.',
            403: 'Not authorized or not authenticated.',
            404: 'Task not found.'
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Partially update a task',
        operation_description='Partially updates a task. Only the author can update it.',
        tags=['tasks'],
        responses={
            200: TodoSerializer,
            400: 'Bad request — invalid data.',
            403: 'Not authorized or not authenticated.',
            404: 'Task not found.'
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Delete a task',
        operation_description='Deletes a task. Only the author can delete it.',
        tags=['tasks'],
        responses={
            204: 'Task deleted successfully.',
            403: 'Not authorized or not authenticated.',
            404: 'Task not found.'
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)