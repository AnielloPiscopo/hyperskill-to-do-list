from django.db import models

__all__ = ['TaskStatus']

class TaskStatus(models.IntegerChoices):
    IN_PROGRESS = 0, 'In Progress'
    TODO = 1, 'To Do'
    DONE = 2, 'Done'