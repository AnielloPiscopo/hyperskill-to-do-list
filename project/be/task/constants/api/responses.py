from drf_spectacular.utils import OpenApiResponse

RESPONSE_404 = OpenApiResponse(description='Task not found.')
RESPONSE_200_ARCHIVED = OpenApiResponse(description='Task archived successfully.')
RESPONSE_200_RESTORED = OpenApiResponse(description='Task restored successfully.')
RESPONSE_200_ARCHIVED_ALL = OpenApiResponse(description='Tasks archived successfully.')
RESPONSE_200_RESTORED_ALL = OpenApiResponse(description='Tasks restored successfully.')
RESPONSE_204_DELETED = OpenApiResponse(description='Task deleted successfully.')