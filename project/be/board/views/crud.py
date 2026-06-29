from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from core.permissions import IsAuthorOrReadOnly
from board.models import Board
from board.serializers import BoardSerializer, BoardDetailSerializer

__all__ = ['BoardListView', 'BoardDetailView']

class BoardListView(generics.ListCreateAPIView):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']

    @extend_schema(
        summary='List all boards',
        description='Returns all boards.',
        tags=['boards'],
        responses={
            200: BoardSerializer(many=True),
            403: OpenApiResponse(description='Authentication credentials were not provided.'),
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary='Create a new board',
        description='Creates a new board. The author is automatically set to the logged in user.',
        tags=['boards'],
        responses={
            201: BoardSerializer,
            400: OpenApiResponse(description='Bad request — invalid data.'),
            403: OpenApiResponse(description='Authentication credentials were not provided.'),
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet:
        return Board.objects.filter(user=self.request.user, is_archived=False).order_by('title')

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BoardDetailSerializer
        return BoardSerializer

    @extend_schema(
        summary='Retrieve a board',
        description='Returns the details of a specific board by its ID, including its tasks.',
        tags=['boards'],
        responses={
            200: BoardDetailSerializer,
            403: OpenApiResponse(description='Authentication credentials were not provided.'),
            404: OpenApiResponse(description='Board not found.'),
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary='Update a board',
        description='Fully updates a board. Only the author can update it.',
        tags=['boards'],
        responses={
            200: BoardSerializer,
            400: OpenApiResponse(description='Bad request — invalid data.'),
            403: OpenApiResponse(description='Not authorized or not authenticated.'),
            404: OpenApiResponse(description='Board not found.'),
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary='Partially update a board',
        description='Partially updates a board. Only the author can update it.',
        tags=['boards'],
        responses={
            200: BoardSerializer,
            400: OpenApiResponse(description='Bad request — invalid data.'),
            403: OpenApiResponse(description='Not authorized or not authenticated.'),
            404: OpenApiResponse(description='Board not found.'),
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary='Delete a board',
        description='Deletes a board. Only the author can delete it.',
        tags=['boards'],
        responses={
            204: OpenApiResponse(description='Board deleted successfully.'),
            403: OpenApiResponse(description='Not authorized or not authenticated.'),
            404: OpenApiResponse(description='Board not found.'),
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Board.objects.filter(user=self.request.user, is_archived=False)