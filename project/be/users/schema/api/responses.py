from drf_spectacular.utils import OpenApiResponse
from core.serializers import SimpleMessageResponseSerializer
from users.serializers import InfoSerializer

RESPONSE_200_CHANGE_PASSWORD = OpenApiResponse(response=SimpleMessageResponseSerializer,
                                               description="Password changed successfully.")

RESPONSE_400_CHANGE_PASSWORD = OpenApiResponse(description='Bad request — invalid data or wrong password.')
RESPONSE_400_LOGIN = OpenApiResponse(description='Invalid credentials.')
RESPONSE_200_LOGOUT = OpenApiResponse(response=SimpleMessageResponseSerializer,
                                      description='Logged out successfully.')
RESPONSE_201_REGISTER = OpenApiResponse(response=InfoSerializer,
                                        description='User created successfully.')
RESPONSE_400_REGISTER = OpenApiResponse(description='Bad request — invalid data or passwords do not match.')
