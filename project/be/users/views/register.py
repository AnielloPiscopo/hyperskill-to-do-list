from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny
from users.serializers import RegisterSerializer

__all__ = ['RegisterView']

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary='Register a new user',
        operation_description='Creates a new user account. No authentication required.',
        tags=['auth'],
        responses={
            201: 'User created successfully.',
            400: 'Bad request — invalid data or passwords do not match.'
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)