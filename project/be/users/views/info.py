import logging
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.utils.logs import LogHelper
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
            401: OpenApiResponse(description='Authentication credentials were not provided.'),
        }
    )
    def get(self, request):
        logger.info(
            f"{LogHelper.build_prefix('users', 'InfoView', 'GET', LogHelper.Direction.REQUEST)} - received")
        serializer = InfoSerializer(request.user)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        logger.info(
            f"{LogHelper.build_prefix('users', 'InfoView', 'GET', LogHelper.Direction.RESPONSE)}"
            f" - status={response.status_code}")
        return response