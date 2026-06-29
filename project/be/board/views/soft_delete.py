from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from drf_spectacular.utils import OpenApiTypes

from board.models import Board
from board.services import archive_board, restore_board, archive_boards, restore_boards
from core.permissions import IsAuthorOrReadOnly

__all__ = ['BoardArchiveView', 'BoardRestoreView', 'BoardArchiveAllView', 'BoardRestoreAllView']


class BoardArchiveView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Archive a board',
        description='Archives a board and all its tasks. Only the author can archive it.',
        tags=['boards'],
        responses={
            200: OpenApiResponse(description='Board archived successfully.'),
            403: OpenApiResponse(description='Not authorized or not authenticated.'),
            404: OpenApiResponse(description='Board not found.'),
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
            200: OpenApiResponse(description='Board restored successfully.'),
            403: OpenApiResponse(description='Not authorized or not authenticated.'),
            404: OpenApiResponse(description='Board not found.'),
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
            200: OpenApiResponse(description='Boards archived successfully.'),
            403: OpenApiResponse(description='Not authenticated.'),
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
            200: OpenApiResponse(description='Boards restored successfully.'),
            403: OpenApiResponse(description='Not authenticated.'),
        }
    )
    def post(self, request):
        ids = request.data.get('ids')
        restore_tasks = request.query_params.get('restore_tasks') == 'true'
        restore_boards(user=request.user, ids=ids if ids is not None and len(ids) > 0 else None,
                       restore_tasks=restore_tasks)
        return Response({'detail': 'Boards restored.'}, status=status.HTTP_200_OK)
