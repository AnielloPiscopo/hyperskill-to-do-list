from django.contrib.auth.models import User
from django.db import models
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models import QuerySet

from core.models import BaseModel
from task.models import Task

__all__ = ["Board"]


class Board(BaseModel):
    if TYPE_CHECKING:
        tasks: "QuerySet[Task]"

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=2048, blank=True, default="")
    color = models.CharField(max_length=7, blank=True, default="#FFFFFF")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="boards")

    def __str__(self):
        return f"[{self.user.username}] {self.title}"

    def __repr__(self):
        return f"Board(id={self.id}, title={self.title!r}, user={self.user.username!r})"