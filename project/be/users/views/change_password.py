from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.serializers import ChangePasswordSerializer

__all__ = ['ChangePasswordView']


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
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'old_password': 'Wrong password.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        Token.objects.filter(user=user).delete()
        return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)