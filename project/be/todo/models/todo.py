from django.db import models
from django.contrib.auth.models import User
from todo.enums import TaskStatus

__all__ = ['Todo']


class Todo(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.CharField(
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
    todo_of = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text='User who created the task'
    )

    def __str__(self) -> str:
        return self.task

    def __repr__(self) -> str:
        return f'Todo(id={self.id!r}, task={self.task!r}, status={self.status!r})'