from django.db import models
from django.contrib.auth.models import User

__all__ = ['Todo']

class Todo(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.CharField(max_length=50)
    description = models.TextField(max_length=1024)
    goal_set_date = models.DateField()
    set_to_complete = models.DateField()
    is_completed = models.BooleanField(default=False)
    todo_of = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
