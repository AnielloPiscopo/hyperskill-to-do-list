from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel
from task.enums import TaskStatus, TaskPriority

__all__ = ['Task']


class Task(BaseModel):
    """A single to-do item owned by a user and optionally associated with a board.

    Supports soft-delete via the inherited `is_archived` flag.
    Deleting a User cascades and removes all their tasks; deleting a Board
    sets the task's `board` FK to NULL (tasks are kept).
    """

    id = models.AutoField(primary_key=True)
    title = models.CharField(
        max_length=50,
        help_text='Title of the task (max 50 characters)'
    )
    description = models.TextField(
        max_length=1024,
        blank=True,
        default='',
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
    priority = models.CharField(
        max_length=20,
        choices=TaskPriority.choices,
        default=TaskPriority.ZERO,
        help_text='Priority of the task'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text='User who created the task'
    )
    board = models.ForeignKey(
        "board.Board",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks"
    )

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return (f'Task(id={self.id!r}, title={self.title!r}, description={self.description!r}, '
                f'status={self.status!r}), priority={self.priority!r}')