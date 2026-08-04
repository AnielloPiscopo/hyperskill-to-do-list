from enum import Enum


class LogHelper:
    """Helper for building standardized log message prefixes across the project."""

    class Direction(str, Enum):
        """Direction of the logged event, relative to the view/serializer."""
        REQUEST = 'REQUEST'
        RESPONSE = 'RESPONSE'

    @staticmethod
    def build_prefix(app_name: str, view_name: str, method: str, direction: 'LogHelper.Direction') -> str:
        """
        Builds a standardized log message prefix.

        Format: [APP_NAME]-[VIEW_NAME]-[METHOD] - [DIRECTION]

        The caller is responsible for appending any additional context
        (e.g. specific variables or a free-text message) after this prefix.
        """
        return f'[{app_name.upper()}]-[{view_name}]-[{method.upper()}] - [{direction.value}]'