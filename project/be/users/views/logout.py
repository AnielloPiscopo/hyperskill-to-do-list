from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

__all__ = ['LogoutView']


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Logout',
        description='Invalidates the current token.',
        tags=['auth'],
        request=None,
        responses={
            200: OpenApiResponse(description='Logged out successfully.'),
            401: OpenApiResponse(description='Authentication credentials were not provided.'),
        }
    )
    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)