import logging
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from core.constants.api import responses as core_responses
from core.utils.logs import LogHelper
from core.permissions import IsAuthorOrReadOnly
from task.constants.api import payloads, responses as task_responses
from task.models import Task
from task.services import archive_task, restore_task, archive_tasks, restore_tasks

__all__ = ['TaskArchiveView', 'TaskRestoreView', 'TaskArchiveAllView', 'TaskRestoreAllView']

logger = logging.getLogger(__name__)

class TaskArchiveView(APIView):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    @extend_schema(
        summary='Archive a task',
        description='Archives a task. Only the author can archive it.',
        tags=['tasks'],
        request=None,
        responses={
            200: task_responses.RESPONSE_200_ARCHIVED,
            403: core_responses.RESPONSE_403,
            404: task_responses.RESPONSE_404,
        }
    )
    def post(self, request: Request, pk: int) -> Response:
        logger.info(
            f"{LogHelper.build_prefix('task', 'TaskArchiveView', 'POST',
                                      LogHelper.Direction.REQUEST)} - received, pk={pk}")
        task: Task = get_object_or_404(Task, pk=pk, user=request.user, is_archived=False)
        self.check_object_permissions(request, task)
        archive_task(task)
        response = Response({'detail': 'Task archived.'}, status=status.HTTP_200_OK)
        logger.info(
            f"{LogHelper.build_prefix('task', 'TaskArchiveView', 'POST',
                                      LogHelper.Direction.RESPONSE)} - status={response.status_code}")
        return response


class TaskRestoreView(APIView):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    @extend_schema(
        summary='Restore a task',
        description='Restores an archived task. Only the author can restore it.',
        tags=['tasks'],
        request=None,
        responses={
            200: task_responses.RESPONSE_200_RESTORED,
            403: core_responses.RESPONSE_403,
            404: task_responses.RESPONSE_404,
        }
    )
    def post(self, request: Request, pk: int) -> Response:
        logger.info(
            f"{LogHelper.build_prefix('task', 'TaskRestoreView', 'POST',
                                      LogHelper.Direction.REQUEST)} - received, pk={pk}")
        task: Task = get_object_or_404(Task, pk=pk, user=request.user, is_archived=True)
        self.check_object_permissions(request, task)
        restore_task(task)
        response = Response({'detail': 'Task restored.'}, status=status.HTTP_200_OK)
        logger.info(
            f"{LogHelper.build_prefix('task', 'TaskRestoreView', 'POST',
                                      LogHelper.Direction.RESPONSE)} - status={response.status_code}")
        return response


class TaskArchiveAllView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Archive multiple tasks',
        description='Archives all tasks or a subset by ids. If ids is empty or not provided, archives all tasks.',
        tags=['tasks'],
        examples=[payloads.TASK_IDS_REQUEST_EXAMPLE, payloads.TASK_IDS_ALL_REQUEST_EXAMPLE],
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'ids': {
                        'type': 'array',
                        'items': {'type': 'integer'},
                        'description': 'List of task ids to archive. If empty, archives all.'
                    }
                }
            }
        },
        responses={
            200: task_responses.RESPONSE_200_ARCHIVED_ALL,
            403: core_responses.RESPONSE_403,
        }
    )
    def post(self, request: Request) -> Response:
        logger.info(
            f"{LogHelper.build_prefix('task', 'TaskArchiveAllView', 'POST', LogHelper.Direction.REQUEST)} - received")
        ids: list[int] | None = request.data.get('ids')
        archive_tasks(user=request.user, ids=ids if ids else None)
        response = Response({'detail': 'Tasks archived.'}, status=status.HTTP_200_OK)
        logger.info(
            f"{LogHelper.build_prefix('task', 'TaskArchiveAllView', 'POST',
                                      LogHelper.Direction.RESPONSE)} - status={response.status_code}")
        return response


class TaskRestoreAllView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Restore multiple tasks',
        description='Restores all archived tasks or a subset by ids. If ids is empty or not provided, '
                    'restores all tasks.',
        tags=['tasks'],
        examples=[payloads.TASK_IDS_REQUEST_EXAMPLE, payloads.TASK_IDS_ALL_REQUEST_EXAMPLE],
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'ids': {
                        'type': 'array',
                        'items': {'type': 'integer'},
                        'description': 'List of task ids to restore. If empty, restores all.'
                    }
                }
            }
        },
        responses={
            200: task_responses.RESPONSE_200_RESTORED_ALL,
            403: core_responses.RESPONSE_403,
        }
    )
    def post(self, request: Request) -> Response:
        logger.info(
            f"{LogHelper.build_prefix('task', 'TaskRestoreAllView', 'POST',
                                      LogHelper.Direction.REQUEST)} - received")
        ids: list[int] | None = request.data.get('ids')
        restore_tasks(user=request.user, ids=ids if ids else None)
        response = Response({'detail': 'Tasks restored.'}, status=status.HTTP_200_OK)
        logger.info(
            f"{LogHelper.build_prefix('task', 'TaskRestoreAllView', 'POST',
                                      LogHelper.Direction.RESPONSE)} - status={response.status_code}")
        return response
