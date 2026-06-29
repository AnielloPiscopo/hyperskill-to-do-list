from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import generics
from rest_framework.permissions import AllowAny
from users.serializers import RegisterSerializer

__all__ = ['RegisterView']

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        summary='Register a new user',
        description='Creates a new user account. No authentication required.',
        tags=['auth'],
        responses={
            201: OpenApiResponse(description='User created successfully.'),
            400: OpenApiResponse(description='Bad request — invalid data or passwords do not match.'),
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)