from django.db import models

__all__ = ['TaskStatus', 'TaskPriority']

class TaskStatus(models.TextChoices):
    """Valid states a task can be in throughout its lifecycle."""

    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    TODO = 'TODO', 'To Do'
    DONE = 'DONE', 'Done'


class TaskPriority(models.TextChoices):
    """Priority levels for tasks, ordered from highest urgency to none.

    ZERO acts as a sentinel "no priority" value and is the only priority
    allowed when a task has status DONE (see TaskSerializer._check_priority_and_status).
    """

    HIGH = 'HIGH', 'High'
    MEDIUM = 'MEDIUM', 'Medium'
    LOW = 'LOW', 'Low'
    ZERO = 'ZERO', 'Zero'