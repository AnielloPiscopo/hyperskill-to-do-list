import logging
from drf_spectacular.utils import extend_schema
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from core.utils.logs import LogHelper
from core.schema.api import responses as core_responses
from users.schema.api import responses as user_responses

__all__ = ['LogoutView']

logger = logging.getLogger(__name__)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Logout',
        description='Invalidates the current token.',
        tags=['auth'],
        request=None,
        responses={
            200: user_responses.RESPONSE_200_LOGOUT,
            401: core_responses.RESPONSE_401,
        }
    )
    def post(self, request: Request) -> Response:
        logger.info(
            f"{LogHelper.build_prefix('users', 'LogoutView', 'POST', LogHelper.Direction.REQUEST)} - received")
        Token.objects.filter(user=request.user).delete()
        response: Response = Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)
        logger.info(
            f"{LogHelper.build_prefix('users', 'LogoutView', 'POST', LogHelper.Direction.RESPONSE)}"
            f" - status={response.status_code}")
        return response