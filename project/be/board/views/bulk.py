import logging
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from core.schema.api import responses as core_responses
from core.utils.logs import LogHelper
from core.serializers import BulkIdsSerializer
from board.schema.api import payloads, responses as board_responses
from board.services import delete_boards

__all__ = ['BoardDestroyAllView']

logger = logging.getLogger(__name__)


class BoardDestroyAllView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Delete multiple boards',
        description='Permanently deletes archived boards, or a subset by ids. '
                    'If ids is empty or not provided, deletes all archived boards.',
        tags=['boards'],
        examples=[payloads.BOARD_IDS_REQUEST_EXAMPLE, payloads.BOARD_IDS_ALL_REQUEST_EXAMPLE],
        request=BulkIdsSerializer,
        responses={
            200: board_responses.RESPONSE_200_DELETED_ALL,
            400: core_responses.RESPONSE_400,
            403: core_responses.RESPONSE_403,
        }
    )
    def post(self, request: Request) -> Response:
        logger.info(
            f"{LogHelper.build_prefix('board', 'BoardDestroyAllView', 'POST', LogHelper.Direction.REQUEST)} - received")

        serializer: BulkIdsSerializer = BulkIdsSerializer(data=request.data)
        if not serializer.is_valid():
            response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            logger.info(
                f"{LogHelper.build_prefix('board', 'BoardDestroyAllView', 'POST', LogHelper.Direction.RESPONSE)}"
                f" - status={response.status_code}, reason=invalid_serializer")
            return response

        ids: list[int] | None = serializer.validated_data.get('ids')
        delete_boards(user=request.user, ids=ids if ids else None)
        response: Response = Response({'detail': 'Boards deleted.'}, status=status.HTTP_200_OK)
        logger.info(
            f"{LogHelper.build_prefix('board', 'BoardDestroyAllView', 'POST', LogHelper.Direction.RESPONSE)}"
            f" - status={response.status_code}")
        return response