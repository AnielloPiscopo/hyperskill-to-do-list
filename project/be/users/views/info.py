from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers import InfoSerializer

__all__ = ['InfoView']

class InfoView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Get current user',
        description='Returns the profile of the currently authenticated user.',
        tags=['auth'],
        responses={
            200: InfoSerializer,
            401: OpenApiResponse(description='Authentication credentials were not provided.'),
        }
    )
    def get(self, request):
        serializer = InfoSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)