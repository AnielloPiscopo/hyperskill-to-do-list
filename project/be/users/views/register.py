import logging
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from users.serializers import RegisterSerializer
from core.utils.logs import LogHelper
from core.throttling import LoginRateThrottle
from core.schema.api import responses as core_responses
from users.schema.api import responses as user_responses

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
            201: user_responses.RESPONSE_201_REGISTER,
            400: user_responses.RESPONSE_400_REGISTER,
            429: core_responses.RESPONSE_429,
        }
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        logger.info(
            f"{LogHelper.build_prefix('users', 'RegisterView', 'POST', LogHelper.Direction.REQUEST)} - received")
        response: Response = super().post(request, *args, **kwargs)
        logger.info(
            f"{LogHelper.build_prefix('users', 'RegisterView', 'POST', LogHelper.Direction.RESPONSE)}"
            f" - status={response.status_code}")
        return response