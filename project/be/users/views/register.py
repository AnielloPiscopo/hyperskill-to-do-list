import logging
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import generics
from rest_framework.permissions import AllowAny
from users.serializers import RegisterSerializer
from core.utils.logs import LogHelper
from core.throttling import LoginRateThrottle

__all__ = ['RegisterView']

logger = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    throttle_classes = [LoginRateThrottle]

    @extend_schema(
        summary='Register a new user',
        description='Creates a new user account. No authentication required.',
        tags=['auth'],
        request=RegisterSerializer,
        responses={
            201: OpenApiResponse(description='User created successfully.'),
            400: OpenApiResponse(description='Bad request — invalid data or passwords do not match.'),
            429: OpenApiResponse(description='Too many requests — rate limit exceeded.'),
        }
    )
    def post(self, request, *args, **kwargs):
        logger.info(
            f"{LogHelper.build_prefix('users', 'RegisterView', 'POST', LogHelper.Direction.REQUEST)} - received")
        response = super().post(request, *args, **kwargs)
        logger.info(
            f"{LogHelper.build_prefix('users', 'RegisterView', 'POST', LogHelper.Direction.RESPONSE)}"
            f" - status={response.status_code}")
        return response