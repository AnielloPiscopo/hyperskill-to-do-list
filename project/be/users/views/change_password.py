import logging
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.utils.logs import LogHelper
from users.serializers import ChangePasswordSerializer

__all__ = ['ChangePasswordView']

logger = logging.getLogger(__name__)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Change password',
        description='Changes the password of the currently authenticated user.',
        tags=['auth'],
        request=ChangePasswordSerializer,
        responses={
            200: OpenApiResponse(description='Password changed successfully.'),
            400: OpenApiResponse(description='Bad request — invalid data or wrong password.'),
            401: OpenApiResponse(description='Authentication credentials were not provided.'),
        }
    )
    def post(self, request):
        logger.info(
            f"{LogHelper.build_prefix('users', 'ChangePasswordView', 'POST', LogHelper.Direction.REQUEST)} - received")

        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            logger.info(
                f"{LogHelper.build_prefix('users', 'ChangePasswordView', 'POST', LogHelper.Direction.RESPONSE)}"
                f" - status={response.status_code}, reason=invalid_serializer")
            return response

        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            response = Response(
                {'old_password': 'Wrong password.'},
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