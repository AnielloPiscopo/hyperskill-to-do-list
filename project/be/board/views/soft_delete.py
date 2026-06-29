from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from board.models import Board
from board.services import archive_board, restore_board, archive_boards, restore_boards
from core.permissions import IsAuthorOrReadOnly

__all__ = ['BoardArchiveView', 'BoardRestoreView', 'BoardArchiveAllView', 'BoardRestoreAllView']


class BoardArchiveView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Archive a board',
        operation_description='Archives a board and all its tasks. Only the author can archive it.',
        tags=['boards'],
        responses={
            200: 'Board archived successfully.',
            403: 'Not authorized or not authenticated.',
            404: 'Board not found.'
        }
    )
    def post(self, request, pk):
        board = get_object_or_404(Board, pk=pk, user=request.user, is_archived=False)
        self.check_object_permissions(request, board)
        archive_board(board)
        return Response({'detail': 'Board archived.'}, status=status.HTTP_200_OK)


class BoardRestoreView(APIView):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    @swagger_auto_schema(
        operation_summary='Restore a board',
        operation_description='Restores an archived board. Pass `?restore_tasks=true` to restore its tasks too.',
        tags=['boards'],
        manual_parameters=[
            openapi.Parameter(
                'restore_tasks',
                openapi.IN_QUERY,
                description='Pass true to restore all tasks associated with the board.',
                type=openapi.TYPE_BOOLEAN
            )
        ],
        responses={
            200: 'Board restored successfully.',
            403: 'Not authorized or not authenticated.',
            404: 'Board not found.'
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

    @swagger_auto_schema(
        operation_summary='Archive multiple boards',
        operation_description='Archives all boards or a subset by ids. If ids is empty or not provided, '
                              'archives all boards.',
        tags=['boards'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'ids': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                    description='List of board ids to archive. If empty or not provided, archives all.'
                )
            }
        ),
        responses={
            200: 'Boards archived successfully.',
            403: 'Not authenticated.',
        }
    )
    def post(self, request):
        ids = request.data.get('ids')
        archive_boards(user=request.user, ids=ids if ids is not None and len(ids) > 0 else None)
        return Response({'detail': 'Boards archived.'}, status=status.HTTP_200_OK)


class BoardRestoreAllView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Restore multiple boards',
        operation_description='Restores all archived boards or a subset by ids. '
                              'Pass `?restore_tasks=true` to restore tasks too.',
        tags=['boards'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'ids': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                    description='List of board ids to restore. If empty or not provided, restores all.'
                )
            }
        ),
        manual_parameters=[
            openapi.Parameter(
                'restore_tasks',
                openapi.IN_QUERY,
                description='Pass true to restore all tasks associated with the board.',
                type=openapi.TYPE_BOOLEAN
            )
        ],
        responses={
            200: 'Boards restored successfully.',
            403: 'Not authenticated.',
        }
    )
    def post(self, request):
        ids = request.data.get('ids')
        restore_tasks = request.query_params.get('restore_tasks') == 'true'
        restore_boards(user=request.user, ids=ids if ids is not None and len(ids) > 0 else None,
                       restore_tasks=restore_tasks)
        return Response({'detail': 'Boards restored.'}, status=status.HTTP_200_OK)
