from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from core.permissions import IsAuthorOrReadOnly
from task.models import Task
from task.services import archive_task, restore_task, archive_tasks, restore_tasks

__all__ = ['TaskArchiveView', 'TaskRestoreView', 'TaskArchiveAllView', 'TaskRestoreAllView']


class TaskArchiveView(APIView):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    @swagger_auto_schema(
        operation_summary='Archive a task',
        operation_description='Archives a task. Only the author can archive it.',
        tags=['tasks'],
        responses={
            200: 'Task archived successfully.',
            403: 'Not authorized or not authenticated.',
            404: 'Task not found.'
        }
    )
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user, is_archived=False)
        self.check_object_permissions(request, task)
        archive_task(task)
        return Response({'detail': 'Task archived.'}, status=status.HTTP_200_OK)


class TaskRestoreView(APIView):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    @swagger_auto_schema(
        operation_summary='Restore a task',
        operation_description='Restores an archived task. Only the author can restore it.',
        tags=['tasks'],
        responses={
            200: 'Task restored successfully.',
            403: 'Not authorized or not authenticated.',
            404: 'Task not found.'
        }
    )
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user, is_archived=True)
        self.check_object_permissions(request, task)
        restore_task(task)
        return Response({'detail': 'Task restored.'}, status=status.HTTP_200_OK)

class TaskArchiveAllView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Archive multiple tasks',
        operation_description='Archives all tasks or a subset by ids. If ids is empty or not provided, '
                              'archives all tasks.',
        tags=['tasks'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'ids': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                    description='List of task ids to archive. If empty, archives all.'
                )
            }
        ),
        responses={
            200: 'Tasks archived successfully.',
            403: 'Not authenticated.',
        }
    )
    def post(self, request):
        ids = request.data.get('ids')
        archive_tasks(user=request.user, ids=ids if ids else None)
        return Response({'detail': 'Tasks archived.'}, status=status.HTTP_200_OK)


class TaskRestoreAllView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Restore multiple tasks',
        operation_description='Restores all archived tasks or a subset by ids. If ids is empty or not provided, '
                              'restores all tasks.',
        tags=['tasks'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'ids': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                    description='List of task ids to restore. If empty, restores all.'
                )
            }
        ),
        responses={
            200: 'Tasks restored successfully.',
            403: 'Not authenticated.',
        }
    )
    def post(self, request):
        ids = request.data.get('ids')
        restore_tasks(user=request.user, ids=ids if ids else None)
        return Response({'detail': 'Tasks restored.'}, status=status.HTTP_200_OK)