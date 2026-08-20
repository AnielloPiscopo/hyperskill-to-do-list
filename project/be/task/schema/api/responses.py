from drf_spectacular.utils import OpenApiResponse
from core.serializers import SimpleMessageResponseSerializer

RESPONSE_400_SINGLE_TASK = OpenApiResponse(description='Bad request — invalid data, or task is archived.')
RESPONSE_400_SINGLE_TASK_DELETE = OpenApiResponse(description='Bad request — task must be archived before deletion.')
RESPONSE_404 = OpenApiResponse(description='Task not found.')
RESPONSE_200_ARCHIVED = OpenApiResponse(response=SimpleMessageResponseSerializer,
                                        description='Task archived successfully.')
RESPONSE_200_RESTORED = OpenApiResponse(response=SimpleMessageResponseSerializer,
                                        description='Task restored successfully.')
RESPONSE_200_ARCHIVED_ALL = OpenApiResponse(response=SimpleMessageResponseSerializer,
                                            description='Tasks archived successfully.')
RESPONSE_200_RESTORED_ALL = OpenApiResponse(response=SimpleMessageResponseSerializer,
                                            description='Tasks restored successfully.')
RESPONSE_200_MOVED = OpenApiResponse(response=SimpleMessageResponseSerializer,
                                     description='Tasks moved successfully.')
RESPONSE_204_DELETED = OpenApiResponse(description='Task deleted successfully.')
