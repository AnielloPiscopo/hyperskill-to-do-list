import logging
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from core.utils.logs import LogHelper
from core.throttling import LoginRateThrottle
from users.serializers import TokenResponseSerializer

__all__ = ['LoginView']

logger = logging.getLogger(__name__)


class LoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [LoginRateThrottle]

    @extend_schema(
        summary='Login',
        description='Returns a token for the given username and password.',
        tags=['auth'],
        request={
            'application/json': {
                'type': 'object',
                'required': ['username', 'password'],
                'properties': {
                    'username': {'type': 'string'},
                    'password': {'type': 'string'},
                }
            }
        },
        responses={
            200: OpenApiResponse(response=TokenResponseSerializer, description='Token returned successfully.'),
            400: OpenApiResponse(description='Invalid credentials.'),
            429: OpenApiResponse(description='Too many requests — rate limit exceeded.'),
        }
    )
    def post(self, request):
        logger.info(
            f"{LogHelper.build_prefix('users', 'LoginView', 'POST', LogHelper.Direction.REQUEST)} - received")

        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            response = Response({'detail': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)
            logger.info(
                f"{LogHelper.build_prefix('users', 'LoginView', 'POST', LogHelper.Direction.RESPONSE)}"
                f" - status={response.status_code}, reason=invalid_credentials")
            return response

        # Reuse the existing token if one exists; a new one is created only on first login
        # or after it has been explicitly deleted (e.g. on logout or password change).
        token, _ = Token.objects.get_or_create(user=user)
        response = Response({'token': token.key}, status=status.HTTP_200_OK)
        logger.info(
            f"{LogHelper.build_prefix('users', 'LoginView', 'POST', LogHelper.Direction.RESPONSE)}"
            f" - status={response.status_code}")
        return response