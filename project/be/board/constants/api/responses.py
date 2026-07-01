from drf_spectacular.utils import OpenApiResponse

RESPONSE_404 = OpenApiResponse(description='Board not found.')
RESPONSE_200_ARCHIVED = OpenApiResponse(description='Board archived successfully.')
RESPONSE_200_RESTORED = OpenApiResponse(description='Board restored successfully.')
RESPONSE_200_ARCHIVED_ALL = OpenApiResponse(description='Boards archived successfully.')
RESPONSE_200_RESTORED_ALL = OpenApiResponse(description='Boards restored successfully.')
RESPONSE_204_DELETED = OpenApiResponse(description='Board deleted successfully.')