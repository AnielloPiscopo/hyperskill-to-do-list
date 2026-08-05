from django.db import models

__all__ = ['TaskStatus', 'TaskPriority']

class TaskStatus(models.TextChoices):
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    TODO = 'TODO', 'To Do'
    DONE = 'DONE', 'Done'


class TaskPriority(models.TextChoices):
    HIGH = 'HIGH', 'High'
    MEDIUM = 'MEDIUM', 'Medium'
    LOW = 'LOW', 'Low'
    ZERO = 'ZERO', 'Zero'