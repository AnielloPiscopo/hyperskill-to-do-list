from drf_spectacular.utils import OpenApiResponse
from core.serializers import SimpleMessageResponseSerializer

RESPONSE_400_SINGLE_BOARD = OpenApiResponse(description='Bad request — invalid data, or board is archived.')
RESPONSE_400_SINGLE_BOARD_DELETE = OpenApiResponse(description='Bad request — board must be archived before deletion.')
RESPONSE_404 = OpenApiResponse(description='Board not found.')
RESPONSE_200_ARCHIVED = OpenApiResponse(response=SimpleMessageResponseSerializer,
                                        description='Board archived successfully.')
RESPONSE_200_RESTORED = OpenApiResponse(response=SimpleMessageResponseSerializer,
                                        description='Board restored successfully.')
RESPONSE_200_ARCHIVED_ALL = OpenApiResponse(response=SimpleMessageResponseSerializer,
                                            description='Boards archived successfully.')
RESPONSE_200_RESTORED_ALL = OpenApiResponse(response=SimpleMessageResponseSerializer,
                                            description='Boards restored successfully.')
RESPONSE_204_DELETED = OpenApiResponse(description='Board deleted successfully.')
