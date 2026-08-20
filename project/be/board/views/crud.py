import logging
from django.db import models
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.exceptions import ValidationError
from core.schema.api import responses as core_responses
from core.utils.logs import LogHelper
from core.permissions import IsAuthorOrReadOnly
from core.mixins import UserScopedQuerysetMixin
from board.constants.api import validation_msg
from board.schema.api import payloads, responses as board_responses
from board.models import Board
from board.serializers import BoardSerializer, BoardDetailSerializer

__all__ = ['BoardListView', 'BoardDetailView']

logger = logging.getLogger(__name__)


class BoardListView(UserScopedQuerysetMixin, generics.ListCreateAPIView):
    request: Request
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']

    @extend_schema(
        summary='List all boards',
        description='Returns all boards.',
        tags=['boards'],
        parameters=[
            OpenApiParameter(
                name='is_archived',
                type=OpenApiTypes.BOOL,
                location='query',
                description='Pass true to return archived boards instead of active ones.',
                required=False,
            )
        ],
        examples=[payloads.BOARD_RESPONSE_EXAMPLE],
        request=None,
        responses={
            200: BoardSerializer(many=True),
            403: core_responses.RESPONSE_403
        }
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        logger.info(
            f"{LogHelper.build_prefix('board', 'BoardListView', 'GET', LogHelper.Direction.REQUEST)} - received")
        response: Response = super().get(request, *args, **kwargs)
        logger.info(
            f"{LogHelper.build_prefix('board', 'BoardListView', 'GET', LogHelper.Direction.RESPONSE)} "
            f" - status={response.status_code}")
        return response

    @extend_schema(
        summary='Create a new board',
        description='Creates a new board. The author is automatically set to the logged in user.',
        tags=['boards'],
        examples=[payloads.BOARD_REQUEST_EXAMPLE, payloads.BOARD_RESPONSE_EXAMPLE],
        request=BoardSerializer,
        responses={
            201: BoardSerializer,
            400: core_responses.RESPONSE_400,
            403: core_responses.RESPONSE_403,
        }
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        logger.info(
            f"{LogHelper.build_prefix('board', 'BoardListView', 'POST', LogHelper.Direction.REQUEST)} - received")
        response: Response = super().post(request, *args, **kwargs)
        logger.info(
            f"{LogHelper.build_prefix('board', 'BoardListView', 'POST', LogHelper.Direction.RESPONSE)} "
            f" - status={response.status_code}")
        return response

    def get_user_queryset(self) -> models.QuerySet[Board]:
        is_archived_param: str | None = self.request.query_params.get('is_archived')
        is_archived: bool = is_archived_param.lower() == 'true' if is_archived_param is not None else False
        return Board.objects.filter(user=self.request.user, is_archived=is_archived).order_by('title')

    def perform_create(self, serializer: BaseSerializer) -> None:
        serializer.save(user=self.request.user)


class BoardDetailView(UserScopedQuerysetMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BoardDetailSerializer
        return BoardSerializer

    @extend_schema(
        summary='Retrieve a board',
        description='Returns the details of a specific board by its ID, including its tasks.',
        tags=['boards'],
        examples=[payloads.BOARD_DETAIL_RESPONSE_EXAMPLE],
        request=None,
        responses={
            200: BoardDetailSerializer,
            403: core_responses.RESPONSE_403,
            404: board_responses.RESPONSE_404,
        }
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        logger.info(
            f"{LogHelper.build_prefix('board', 'BoardDetailView', 'GET', LogHelper.Direction.REQUEST)} - received")
        response: Response = super().get(request, *args, **kwargs)
        logger.info(
            f"{LogHelper.build_prefix('board', 'BoardDetailView', 'GET', LogHelper.Direction.RESPONSE)}"
            f" - status={response.status_code}")
        return response

    @extend_schema(
        summary='Update a board',
        description='Fully updates a board. Only the author can update it.',
        tags=['boards'],
        examples=[payloads.BOARD_REQUEST_EXAMPLE, payloads.BOARD_RESPONSE_EXAMPLE],
        request=BoardSerializer,
        responses={
            200: BoardSerializer,
            400: board_responses.RESPONSE_400_SINGLE_BOARD,
            403: core_responses.RESPONSE_403,
            404: board_responses.RESPONSE_404,
        }
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        logger.info(
            f"{LogHelper.build_prefix('board', 'BoardDetailView', 'PUT', LogHelper.Direction.REQUEST)} - received")
        response: Response = super().put(request, *args, **kwargs)
        logger.info(
            f"{LogHelper.build_prefix('board', 'BoardDetailView', 'PUT', LogHelper.Direction.RESPONSE)}"
            f" - status={response.status_code}")
        return response

    @extend_schema(
        summary='Partially update a board',
        description='Partially updates a board. Only the author can update it.',
        tags=['boards'],
        examples=[payloads.BOARD_REQUEST_EXAMPLE, payloads.BOARD_RESPONSE_EXAMPLE],
        responses={
            200: BoardSerializer,
            400: board_responses.RESPONSE_400_SINGLE_BOARD,
            403: core_responses.RESPONSE_403,
            404: board_responses.RESPONSE_404,
        }
    )
    def patch(self, request: Request, *args, **kwargs) -> Response:
        logger.info(
            f"{LogHelper.build_prefix('board', 'BoardDetailView', 'PATCH', LogHelper.Direction.REQUEST)} - received")
        response: Response = super().patch(request, *args, **kwargs)
        logger.info(
            f"{LogHelper.build_prefix('board', 'BoardDetailView', 'PATCH', LogHelper.Direction.RESPONSE)}"
            f" - status={response.status_code}")
        return response

    @extend_schema(
        summary='Delete a board',
        description='Deletes a board. Only the author can delete it.',
        tags=['boards'],
        request=None,
        responses={
            204: board_responses.RESPONSE_204_DELETED,
            400: board_responses.RESPONSE_400_SINGLE_BOARD_DELETE,
            403: core_responses.RESPONSE_403,
            404: board_responses.RESPONSE_404,
        }
    )
    def delete(self, request: Request, *args, **kwargs) -> Response:
        logger.info(
            f"{LogHelper.build_prefix('board', 'BoardDetailView', 'DELETE', LogHelper.Direction.REQUEST)} - received")
        response: Response = super().delete(request, *args, **kwargs)
        logger.info(
            f"{LogHelper.build_prefix('board', 'BoardDetailView', 'DELETE', LogHelper.Direction.RESPONSE)}"
            f" - status={response.status_code}")
        return response

    def get_user_queryset(self) -> models.QuerySet[Board]:
        return Board.objects.filter(user=self.request.user)

    def perform_update(self, serializer: BaseSerializer) -> None:
        if self.get_object().is_archived:
            raise ValidationError({'detail': validation_msg.UPDATE_NOT_ALLOWED_IF_ARCHIVED})
        serializer.save()

    def perform_destroy(self, instance: Board) -> None:
        if not instance.is_archived:
            raise ValidationError({'detail': validation_msg.DELETE_NOT_ALLOWED_IF_ACTIVE})
        instance.delete()