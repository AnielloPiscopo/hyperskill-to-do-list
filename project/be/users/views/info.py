import logging

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from core.utils.logs import LogHelper
from core.schema.api import responses as core_responses
from users.serializers import InfoSerializer

__all__ = ['InfoView']

logger = logging.getLogger(__name__)

class InfoView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Get current user',
        description='Returns the profile of the currently authenticated user.',
        tags=['auth'],
        request=None,
        responses={
            200: InfoSerializer,
            401: core_responses.RESPONSE_401,
        }
    )
    def get(self, request: Request) -> Response:
        logger.info(
            f"{LogHelper.build_prefix('users', 'InfoView', 'GET', LogHelper.Direction.REQUEST)} - received")
        serializer: InfoSerializer = InfoSerializer(request.user)
        response: Response = Response(serializer.data, status=status.HTTP_200_OK)
        logger.info(
            f"{LogHelper.build_prefix('users', 'InfoView', 'GET', LogHelper.Direction.RESPONSE)}"
            f" - status={response.status_code}")
        return response