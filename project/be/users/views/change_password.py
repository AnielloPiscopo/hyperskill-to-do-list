import logging
from django.contrib.auth.models import User
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
from users.serializers import ChangePasswordSerializer

__all__ = ['ChangePasswordView']

logger = logging.getLogger(__name__)


class ChangePasswordView(APIView):
    request: Request
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Change password',
        description='Changes the password of the currently authenticated user.',
        tags=['auth'],
        request=ChangePasswordSerializer,
        responses={
            200: user_responses.RESPONSE_200_CHANGE_PASSWORD,
            400: user_responses.RESPONSE_400_CHANGE_PASSWORD,
            401: core_responses.RESPONSE_401,
        }
    )
    def post(self, request: Request) -> Response:
        logger.info(
            f"{LogHelper.build_prefix('users', 'ChangePasswordView', 'POST', LogHelper.Direction.REQUEST)} - received")

        serializer: ChangePasswordSerializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            response: Response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            logger.info(
                f"{LogHelper.build_prefix('users', 'ChangePasswordView', 'POST', LogHelper.Direction.RESPONSE)}"
                f" - status={response.status_code}, reason=invalid_serializer")
            return response

        user: User = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            response: Response = Response(
                {'old_password': ['Wrong password.']},
                status=status.HTTP_400_BAD_REQUEST
            )
            logger.info(
                f"{LogHelper.build_prefix('users', 'ChangePasswordView', 'POST', LogHelper.Direction.RESPONSE)}"
                f" - status={response.status_code}, reason=wrong_password")
            return response

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        # Invalidate the existing auth token so the client must log in again
        # with the new password; avoids stale tokens remaining valid after a
        # password change.
        Token.objects.filter(user=user).delete()
        response = Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        logger.info(
            f"{LogHelper.build_prefix('users', 'ChangePasswordView', 'POST', LogHelper.Direction.RESPONSE)}"
            f" - status={response.status_code}")
        return response