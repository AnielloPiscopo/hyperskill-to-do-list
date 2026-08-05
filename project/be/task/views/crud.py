import logging
from django.db import models
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from django_filters.rest_framework import DjangoFilterBackend
from core.constants.api import responses as core_responses
from core.utils.logs import LogHelper
from core.permissions import IsAuthorOrReadOnly
from core.mixins import UserScopedQuerysetMixin
from task.constants.api import payloads, responses as task_responses
from task.models import Task
from task.serializers import TaskSerializer
from task.enums import TaskStatus, TaskPriority

__all__ = ['TaskDetailView', 'TaskListView']

logger = logging.getLogger(__name__)


class TaskListView(UserScopedQuerysetMixin, generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'priority', 'board']
    search_fields = ['title', 'description']
    ordering_fields = ['set_to_complete', 'status', 'priority', 'created_at']

    @extend_schema(
        summary='List all tasks',
        description='Returns all tasks ordered by completion status, deadline and creation date.',
        tags=['tasks'],
        examples=[payloads.TASK_RESPONSE_EXAMPLE],
        request=None,
        responses={
            200: TaskSerializer(many=True),
            403: core_responses.RESPONSE_403,
        }
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        logger.info(
            f"{LogHelper.build_prefix('task', 'TaskListView', 'GET', LogHelper.Direction.REQUEST)} - received")
        response = super().get(request, *args, **kwargs)
        logger.info(
            f"{LogHelper.build_prefix('task', 'TaskListView', 'GET',
                                      LogHelper.Direction.RESPONSE)} - status={response.status_code}")
        return response

    @extend_schema(
        summary='Create a new task',
        description='Creates a new task. The author is automatically set to the logged in user.',
        tags=['tasks'],
        examples=[payloads.TASK_REQUEST_EXAMPLE, payloads.TASK_RESPONSE_EXAMPLE],
        request=TaskSerializer,
        responses={
            201: TaskSerializer,
            400: core_responses.RESPONSE_400,
            403: core_responses.RESPONSE_403,
        }
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        logger.info(
            f"{LogHelper.build_prefix('task', 'TaskListView', 'POST', LogHelper.Direction.REQUEST)} - received")
        response = super().post(request, *args, **kwargs)
        logger.info(
            f"{LogHelper.build_prefix('task', 'TaskListView', 'POST',
                                      LogHelper.Direction.RESPONSE)} - status={response.status_code}")
        return response

    def get_user_queryset(self) -> models.QuerySet[Task]:
        # Annotate each task with a numeric sort key so the list is ordered by
        # urgency: active high-priority tasks appear first, DONE tasks last.
        # The specific integer values (0–7, 100) are arbitrary rank slots;
        # only their relative order matters.
        return Task.objects.filter(user=self.request.user, is_archived=False).annotate(
            order=models.Case(
                models.When(status=TaskStatus.DONE, then=models.Value(100)),  # DONE always sinks to the bottom
                models.When(priority=TaskPriority.HIGH, status=TaskStatus.IN_PROGRESS, then=models.Value(0)),
                models.When(priority=TaskPriority.HIGH, status=TaskStatus.TODO, then=models.Value(1)),
                models.When(priority=TaskPriority.MEDIUM, status=TaskStatus.IN_PROGRESS, then=models.Value(2)),
                models.When(priority=TaskPriority.MEDIUM, status=TaskStatus.TODO, then=models.Value(3)),
                models.When(priority=TaskPriority.LOW, status=TaskStatus.IN_PROGRESS, then=models.Value(4)),
                models.When(priority=TaskPriority.LOW, status=TaskStatus.TODO, then=models.Value(5)),
                models.When(priority=TaskPriority.ZERO, status=TaskStatus.IN_PROGRESS, then=models.Value(6)),
                models.When(priority=TaskPriority.ZERO, status=TaskStatus.TODO, then=models.Value(7)),
                output_field=models.IntegerField()
            )
        ).order_by('order')

    def perform_create(self, serializer: BaseSerializer) -> None:
        serializer.save(user=self.request.user)


class TaskDetailView(UserScopedQuerysetMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    @extend_schema(
        summary='Retrieve a task',
        description='Returns the details of a specific task by its ID.',
        tags=['tasks'],
        examples=[payloads.TASK_RESPONSE_EXAMPLE],
        request=None,
        responses={
            200: TaskSerializer,
            403: core_responses.RESPONSE_403,
            404: task_responses.RESPONSE_404,
        }
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        logger.info(
            f"{LogHelper.build_prefix('task', 'TaskDetailView', 'GET', LogHelper.Direction.REQUEST)} - received")
        response = super().get(request, *args, **kwargs)
        logger.info(
            f"{LogHelper.build_prefix('task', 'TaskDetailView', 'GET',
                                      LogHelper.Direction.RESPONSE)} - status={response.status_code}")
        return response

    @extend_schema(
        summary='Update a task',
        description='Fully updates a task. Only the author can update it.',
        tags=['tasks'],
        examples=[payloads.TASK_REQUEST_EXAMPLE, payloads.TASK_RESPONSE_EXAMPLE],
        request=TaskSerializer,
        responses={
            200: TaskSerializer,
            400: core_responses.RESPONSE_400,
            403: core_responses.RESPONSE_403,
            404: task_responses.RESPONSE_404,
        }
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        logger.info(
            f"{LogHelper.build_prefix('task', 'TaskDetailView', 'PUT', LogHelper.Direction.REQUEST)} - received")
        response = super().put(request, *args, **kwargs)
        logger.info(
            f"{LogHelper.build_prefix('task', 'TaskDetailView', 'PUT',
                                      LogHelper.Direction.RESPONSE)} - status={response.status_code}")
        return response

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
    def patch(self, request: Request, *args, **kwargs) -> Response:
        logger.info(
            f"{LogHelper.build_prefix('task', 'TaskDetailView', 'PATCH', LogHelper.Direction.REQUEST)} - received")
        response = super().patch(request, *args, **kwargs)
        logger.info(
            f"{LogHelper.build_prefix('task', 'TaskDetailView', 'PATCH',
                                      LogHelper.Direction.RESPONSE)} - status={response.status_code}")
        return response

    @extend_schema(
        summary='Delete a task',
        description='Deletes a task. Only the author can delete it.',
        tags=['tasks'],
        request=None,
        responses={
            204: task_responses.RESPONSE_204_DELETED,
            403: core_responses.RESPONSE_403,
            404: task_responses.RESPONSE_404,
        }
    )
    def delete(self, request: Request, *args, **kwargs) -> Response:
        logger.info(
            f"{LogHelper.build_prefix('task', 'TaskDetailView', 'DELETE', LogHelper.Direction.REQUEST)} - received")
        response = super().delete(request, *args, **kwargs)
        logger.info(
            f"{LogHelper.build_prefix('task', 'TaskDetailView', 'DELETE',
                                      LogHelper.Direction.RESPONSE)} - status={response.status_code}")
        return response

    def get_user_queryset(self) -> models.QuerySet[Task]:
        return Task.objects.filter(user=self.request.user, is_archived=False)