from django.db import models

__all__ = ['TaskStatus', 'TaskPriority']

class TaskStatus(models.IntegerChoices):
    IN_PROGRESS = 0, 'In Progress'
    TODO = 1, 'To Do'
    DONE = 2, 'Done'

class TaskPriority(models.IntegerChoices):
    HIGH = 0, 'High'
    MEDIUM = 1, 'Medium'
    LOW = 2, 'Low'
    ZERO = 3, 'Zero'