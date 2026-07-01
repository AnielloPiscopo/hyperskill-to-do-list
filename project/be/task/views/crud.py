from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from core.constants.api import responses as core_responses
from core.permissions import IsAuthorOrReadOnly
from task.constants.api import payloads, responses as task_responses
from task.models import Task
from task.serializers import TaskSerializer

__all__ = ['TaskDetailView', 'TaskListView']


class TaskListView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'board']
    search_fields = ['title', 'description']
    ordering_fields = ['set_to_complete', 'status', 'created_at']

    @extend_schema(
        summary='List all tasks',
        description='Returns all tasks ordered by completion status, deadline and creation date.',
        tags=['tasks'],
        examples=[payloads.TASK_RESPONSE_EXAMPLE],
        responses={
            200: TaskSerializer(many=True),
            403: core_responses.RESPONSE_403,
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary='Create a new task',
        description='Creates a new task. The author is automatically set to the logged in user.',
        tags=['tasks'],
        examples=[payloads.TASK_REQUEST_EXAMPLE, payloads.TASK_RESPONSE_EXAMPLE],
        responses={
            201: TaskSerializer,
            400: core_responses.RESPONSE_400,
            403: core_responses.RESPONSE_403,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet:
        return Task.objects.filter(user=self.request.user, is_archived=False).order_by('set_to_complete', 'status')

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    @extend_schema(
        summary='Retrieve a task',
        description='Returns the details of a specific task by its ID.',
        tags=['tasks'],
        examples=[payloads.TASK_RESPONSE_EXAMPLE],
        responses={
            200: TaskSerializer,
            403: core_responses.RESPONSE_403,
            404: task_responses.RESPONSE_404,
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary='Update a task',
        description='Fully updates a task. Only the author can update it.',
        tags=['tasks'],
        examples=[payloads.TASK_REQUEST_EXAMPLE, payloads.TASK_RESPONSE_EXAMPLE],
        responses={
            200: TaskSerializer,
            400: core_responses.RESPONSE_400,
            403: core_responses.RESPONSE_403,
            404: task_responses.RESPONSE_404,
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary='Partially update a task',
        description='Partially updates a task. Only the author can update it.',
        tags=['tasks'],
        examples=[payloads.TASK_REQUEST_EXAMPLE, payloads.TASK_RESPONSE_EXAMPLE],
        responses={
            200: TaskSerializer,
            400: core_responses.RESPONSE_400,
            403: core_responses.RESPONSE_403,
            404: task_responses.RESPONSE_404,
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary='Delete a task',
        description='Deletes a task. Only the author can delete it.',
        tags=['tasks'],
        responses={
            204: task_responses.RESPONSE_204_DELETED,
            403: core_responses.RESPONSE_403,
            404: task_responses.RESPONSE_404,
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, is_archived=False)
