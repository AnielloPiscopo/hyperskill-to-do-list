from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from drf_spectacular.utils import OpenApiTypes
from core.constants.api import responses as core_responses
from core.permissions import IsAuthorOrReadOnly
from board.constants.api import payloads, responses as board_responses
from board.models import Board
from board.services import archive_board, restore_board, archive_boards, restore_boards

__all__ = ['BoardArchiveView', 'BoardRestoreView', 'BoardArchiveAllView', 'BoardRestoreAllView']


class BoardArchiveView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Archive a board',
        description='Archives a board and all its tasks. Only the author can archive it.',
        tags=['boards'],
        responses={
            200: board_responses.RESPONSE_200_ARCHIVED,
            403: core_responses.RESPONSE_403,
            404: board_responses.RESPONSE_404,
        }
    )
    def post(self, request, pk):
        board = get_object_or_404(Board, pk=pk, user=request.user, is_archived=False)
        self.check_object_permissions(request, board)
        archive_board(board)
        return Response({'detail': 'Board archived.'}, status=status.HTTP_200_OK)


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
        responses={
            200: board_responses.RESPONSE_200_RESTORED,
            403: core_responses.RESPONSE_403,
            404: board_responses.RESPONSE_404,
        }
    )
    def post(self, request, pk):
        board = get_object_or_404(Board, pk=pk, user=request.user, is_archived=True)
        self.check_object_permissions(request, board)
        restore_tasks = request.query_params.get('restore_tasks') == 'true'
        restore_board(board, restore_tasks=restore_tasks)
        return Response({'detail': 'Board restored.'}, status=status.HTTP_200_OK)


class BoardArchiveAllView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Archive multiple boards',
        description='Archives all boards or a subset by ids. If ids is empty or not provided, archives all boards.',
        tags=['boards'],
        examples=[payloads.BOARD_IDS_REQUEST_EXAMPLE, payloads.BOARD_IDS_ALL_REQUEST_EXAMPLE],
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'ids': {
                        'type': 'array',
                        'items': {'type': 'integer'},
                        'description': 'List of board ids to archive. If empty, archives all.'
                    }
                }
            }
        },
        responses={
            200: board_responses.RESPONSE_200_ARCHIVED_ALL,
            403: core_responses.RESPONSE_403,
        }
    )
    def post(self, request):
        ids = request.data.get('ids')
        archive_boards(user=request.user, ids=ids if ids is not None and len(ids) > 0 else None)
        return Response({'detail': 'Boards archived.'}, status=status.HTTP_200_OK)


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
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'ids': {
                        'type': 'array',
                        'items': {'type': 'integer'},
                        'description': 'List of board ids to restore. If empty, restores all.'
                    }
                }
            }
        },
        responses={
            200: board_responses.RESPONSE_200_RESTORED_ALL,
            403: core_responses.RESPONSE_403,
        }
    )
    def post(self, request):
        ids = request.data.get('ids')
        restore_tasks = request.query_params.get('restore_tasks') == 'true'
        restore_boards(user=request.user, ids=ids if ids is not None and len(ids) > 0 else None,
                       restore_tasks=restore_tasks)
        return Response({'detail': 'Boards restored.'}, status=status.HTTP_200_OK)