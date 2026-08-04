import logging
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.utils import OpenApiTypes
from core.constants.api import responses as core_responses
from core.utils.logs import LogHelper
from core.permissions import IsAuthorOrReadOnly
from core.serializers import BulkIdsSerializer
from board.constants.api import payloads, responses as board_responses
from board.models import Board
from board.services import archive_board, restore_board, archive_boards, restore_boards

__all__ = ['BoardArchiveView', 'BoardRestoreView', 'BoardArchiveAllView', 'BoardRestoreAllView']

logger = logging.getLogger(__name__)

class BoardArchiveView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Archive a board',
        description='Archives a board and all its tasks. Only the author can archive it.',
        tags=['boards'],
        request=None,
        responses={
            200: board_responses.RESPONSE_200_ARCHIVED,
            403: core_responses.RESPONSE_403,
            404: board_responses.RESPONSE_404,
        }
    )
    def post(self, request: Request, pk: int) -> Response:
        logger.info(
            f"{LogHelper.build_prefix('board', 'BoardArchiveView', 'POST',
                                      LogHelper.Direction.REQUEST)} - received, pk={pk}")
        board: Board = get_object_or_404(Board, pk=pk, user=request.user, is_archived=False)
        self.check_object_permissions(request, board)
        archive_board(board)
        response = Response({'detail': 'Board archived.'}, status=status.HTTP_200_OK)
        logger.info(
            f"{LogHelper.build_prefix('board', 'BoardArchiveView', 'POST',
                                      LogHelper.Direction.RESPONSE)} - status={response.status_code}")
        return response


class BoardRestoreView(APIView):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    @extend_schema(
        summary='Restore a board',
        description='Restores an archived board. Pass `?restore_tasks=true` to restore its tasks too.',
        tags=['boards'],
        parameters=[
            OpenApiParameter(
                name='restore_tasks',
                type=OpenApiTypes.BOOL,
                location='query',
                description='Pass true to restore all tasks associated with the board.',
                required=False,
            )
        ],
        request=None,
        responses={
            200: board_responses.RESPONSE_200_RESTORED,
            403: core_responses.RESPONSE_403,
            404: board_responses.RESPONSE_404,
        }
    )
    def post(self, request: Request, pk: int):
        logger.info(
            f"{LogHelper.build_prefix('board', 'BoardRestoreView', 'POST',
                                      LogHelper.Direction.REQUEST)} - received, pk={pk}")
        board: Board = get_object_or_404(Board, pk=pk, user=request.user, is_archived=True)
        self.check_object_permissions(request, board)
        restore_tasks: bool = request.query_params.get('restore_tasks') == 'true'
        restore_board(board, restore_tasks=restore_tasks)
        response = Response({'detail': 'Board restored.'}, status=status.HTTP_200_OK)
        logger.info(
            f"{LogHelper.build_prefix('board', 'BoardRestoreView', 'POST',
                                      LogHelper.Direction.RESPONSE)} - status={response.status_code}")
        return response


class BoardArchiveAllView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Archive multiple boards',
        description='Archives all boards or a subset by ids. If ids is empty or not provided, archives all boards.',
        tags=['boards'],
        examples=[payloads.BOARD_IDS_REQUEST_EXAMPLE, payloads.BOARD_IDS_ALL_REQUEST_EXAMPLE],
        request=BulkIdsSerializer,
        responses={
            200: board_responses.RESPONSE_200_ARCHIVED_ALL,
            400: core_responses.RESPONSE_400,
            403: core_responses.RESPONSE_403,
        }
    )
    def post(self, request: Request) -> Response:
        logger.info(
            f"{LogHelper.build_prefix('board', 'BoardArchiveAllView', 'POST', LogHelper.Direction.REQUEST)} - received")

        serializer = BulkIdsSerializer(data=request.data)
        if not serializer.is_valid():
            response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            logger.info(
                f"{LogHelper.build_prefix('board', 'BoardArchiveAllView', 'POST', LogHelper.Direction.RESPONSE)}"
                f" - status={response.status_code}, reason=invalid_serializer")
            return response

        ids: list[int] | None = serializer.validated_data.get('ids')
        archive_boards(user=request.user, ids=ids if ids else None)
        response = Response({'detail': 'Boards archived.'}, status=status.HTTP_200_OK)
        logger.info(
            f"{LogHelper.build_prefix('board', 'BoardArchiveAllView', 'POST', LogHelper.Direction.RESPONSE)}"
            f" - status={response.status_code}")
        return response


class BoardRestoreAllView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Restore multiple boards',
        description='Restores all archived boards or a subset by ids. Pass `?restore_tasks=true` to restore tasks too.',
        tags=['boards'],
        parameters=[
            OpenApiParameter(
                name='restore_tasks',
                type=OpenApiTypes.BOOL,
                location='query',
                description='Pass true to restore all tasks associated with the boards.',
                required=False,
            )
        ],
        examples=[payloads.BOARD_IDS_REQUEST_EXAMPLE, payloads.BOARD_IDS_ALL_REQUEST_EXAMPLE],
        request=BulkIdsSerializer,
        responses={
            200: board_responses.RESPONSE_200_RESTORED_ALL,
            400: core_responses.RESPONSE_400,
            403: core_responses.RESPONSE_403,
        }
    )
    def post(self, request: Request) -> Response:
        logger.info(
            f"{LogHelper.build_prefix('board', 'BoardRestoreAllView', 'POST', LogHelper.Direction.REQUEST)} - received")

        serializer = BulkIdsSerializer(data=request.data)
        if not serializer.is_valid():
            response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            logger.info(
                f"{LogHelper.build_prefix('board', 'BoardRestoreAllView', 'POST', LogHelper.Direction.RESPONSE)}"
                f" - status={response.status_code}, reason=invalid_serializer")
            return response

        ids: list[int] | None = serializer.validated_data.get('ids')
        restore_tasks: bool = request.query_params.get('restore_tasks') == 'true'
        restore_boards(user=request.user, ids=ids if ids else None, restore_tasks=restore_tasks)
        response = Response({'detail': 'Boards restored.'}, status=status.HTTP_200_OK)
        logger.info(
            f"{LogHelper.build_prefix('board', 'BoardRestoreAllView', 'POST', LogHelper.Direction.RESPONSE)}"
            f" - status={response.status_code}")
        return response