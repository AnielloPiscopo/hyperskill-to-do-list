from drf_spectacular.utils import OpenApiExample

TASK_REQUEST_EXAMPLE = OpenApiExample(
    'Example request',
    value={
        'title': 'My Task',
        'description': 'A task description',
        'goal_set_date': '2024-01-01',
        'set_to_complete': '2024-01-31',
        'status': 'TODO',
        'priority': 'ZERO',
        'board': 1,
    },
    request_only=True,
)

TASK_RESPONSE_EXAMPLE = OpenApiExample(
    'Example response',
    value={
        'id': 1,
        'title': 'My Task',
        'description': 'A task description',
        'goal_set_date': '2024-01-01',
        'set_to_complete': '2024-01-31',
        'status': 'TODO',
        'priority': 'ZERO',
        'board': 1,
        'created_at': '2024-01-01T00:00:00Z',
        'updated_at': '2024-01-01T00:00:00Z',
    },
    response_only=True,
)

TASK_IDS_REQUEST_EXAMPLE = OpenApiExample(
    'Example request',
    value={'ids': [1, 2, 3]},
    request_only=True,
)

TASK_IDS_ALL_REQUEST_EXAMPLE = OpenApiExample(
    'Example request — all',
    value={},
    request_only=True,
)