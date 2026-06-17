from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel
from task.enums import TaskStatus

__all__ = ['Task']


class Task(BaseModel):
    id = models.AutoField(primary_key=True)
    title = models.CharField(
        max_length=50,
        help_text='Title of the task (max 50 characters)'
    )
    description = models.TextField(
        max_length=1024,
        help_text='Detailed description of the task (max 1024 characters)'
    )
    goal_set_date = models.DateField(
        help_text='Date when the task was created (YYYY-MM-DD)'
    )
    set_to_complete = models.DateField(
        help_text='Deadline for the task (YYYY-MM-DD)'
    )
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.TODO,
        help_text='Status of the task'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text='User who created the task'
    )

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return f'Task(id={self.id!r}, title={self.title!r}, description={self.description!r}, status={self.status!r})'