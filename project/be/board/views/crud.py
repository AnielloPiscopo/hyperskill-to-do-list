from django.db.models import QuerySet
from drf_yasg.utils import swagger_auto_schema
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

    @swagger_auto_schema(
        operation_summary='List all boards',
        operation_description='Returns all boards',
        tags=['boards'],
        responses={
            200: BoardSerializer(many=True),
            403: 'Authentication credentials were not provided.'
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Create a new board',
        operation_description='Creates a new board. The author is automatically set to the logged in user.',
        tags=['boards'],
        responses={
            201: BoardSerializer,
            400: 'Bad request — invalid data.',
            403: 'Authentication credentials were not provided.'
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet:
        return Board.objects.filter(user=self.request.user, is_archived=False).order_by('title')

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)

class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BoardDetailSerializer
        return BoardSerializer

    @swagger_auto_schema(
        operation_summary='Retrieve a board',
        operation_description='Returns the details of a specific board by its ID.',
        tags=['boards'],
        responses={
            200: BoardSerializer,
            403: 'Authentication credentials were not provided.',
            404: 'Board not found.'
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Update a board',
        operation_description='Fully updates a board. Only the author can update it.',
        tags=['boards'],
        responses={
            200: BoardSerializer,
            400: 'Bad request — invalid data.',
            403: 'Not authorized or not authenticated.',
            404: 'Board not found.'
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Partially update a board',
        operation_description='Partially updates a board. Only the author can update it.',
        tags=['boards'],
        responses={
            200: BoardSerializer,
            400: 'Bad request — invalid data.',
            403: 'Not authorized or not authenticated.',
            404: 'Board not found.'
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Delete a board',
        operation_description='Deletes a board. Only the author can delete it.',
        tags=['boards'],
        responses={
            204: 'Board deleted successfully.',
            403: 'Not authorized or not authenticated.',
            404: 'Board not found.'
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Board.objects.filter(user=self.request.user, is_archived=False)