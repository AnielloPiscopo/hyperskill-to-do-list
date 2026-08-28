import logging
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from core.schema.api import responses as core_responses
from core.utils.logs import LogHelper
from core.serializers import BulkIdsSerializer
from task.schema.api import payloads, responses as task_responses
from task.serializers import TaskMoveSerializer
from task.services import move_tasks, delete_tasks
from board.models import Board

__all__ = ['TaskMoveView', 'TaskDestroyAllView']

logger = logging.getLogger(__name__)

class TaskMoveView(APIView):
    """View for moving multiple tasks to a board in a single request."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Move tasks to a board',
        description='Moves a list of tasks to a board. Pass `null` as board to remove tasks from their board.',
        tags=['tasks'],
        request=TaskMoveSerializer,
        responses={
            200: task_responses.RESPONSE_200_MOVED,
            400: core_responses.RESPONSE_400,
            403: core_responses.RESPONSE_403,
        }
    )
    def post(self, request: Request) -> Response:
        logger.info(
            f"{LogHelper.build_prefix('task', 'TaskMoveView', 'POST', LogHelper.Direction.REQUEST)} - received")

        serializer: TaskMoveSerializer = TaskMoveSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            response: Response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            logger.info(
                f"{LogHelper.build_prefix('task', 'TaskMoveView', 'POST', LogHelper.Direction.RESPONSE)}"
                f" - status={response.status_code}, reason=invalid_serializer")
            return response

        ids: list[int] = serializer.validated_data.get('ids')
        board: Board = serializer.validated_data.get('board')
        move_tasks(user=request.user, ids=ids, board=board)

        response: Response = Response({'detail': 'Tasks moved.'}, status=status.HTTP_200_OK)
        logger.info(
            f"{LogHelper.build_prefix('task', 'TaskMoveView', 'POST', LogHelper.Direction.RESPONSE)}"
            f" - status={response.status_code}")
        return response


class TaskDestroyAllView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Delete multiple tasks',
        description='Permanently deletes archived tasks, or a subset by ids. '
                    'If ids is empty or not provided, deletes all archived tasks.',
        tags=['tasks'],
        examples=[payloads.TASK_IDS_REQUEST_EXAMPLE, payloads.TASK_IDS_ALL_REQUEST_EXAMPLE],
        request=BulkIdsSerializer,
        responses={
            200: task_responses.RESPONSE_200_DELETED_ALL,
            400: core_responses.RESPONSE_400,
            403: core_responses.RESPONSE_403,
        }
    )
    def post(self, request: Request) -> Response:
        logger.info(
            f"{LogHelper.build_prefix('task', 'TaskDestroyAllView', 'POST', LogHelper.Direction.REQUEST)} - received")

        serializer: BulkIdsSerializer = BulkIdsSerializer(data=request.data)
        if not serializer.is_valid():
            response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            logger.info(
                f"{LogHelper.build_prefix('task', 'TaskDestroyAllView', 'POST', LogHelper.Direction.RESPONSE)}"
                f" - status={response.status_code}, reason=invalid_serializer")
            return response

        ids: list[int] | None = serializer.validated_data.get('ids')
        delete_tasks(user=request.user, ids=ids if ids else None)
        response: Response = Response({'detail': 'Tasks deleted.'}, status=status.HTTP_200_OK)
        logger.info(
            f"{LogHelper.build_prefix('task', 'TaskDestroyAllView', 'POST', LogHelper.Direction.RESPONSE)}"
            f" - status={response.status_code}")
        return response