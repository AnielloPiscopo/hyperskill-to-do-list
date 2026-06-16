from rest_framework import serializers
from todo.models import Todo

__all__ = ['TodoSerializer']


class TodoSerializer(serializers.ModelSerializer):
    task = serializers.CharField(
        max_length=50,
        help_text='Title of the task (max 50 characters)'
    )
    description = serializers.CharField(
        max_length=1024,
        help_text='Description of the task (max 1024 characters)'
    )
    goal_set_date = serializers.DateField(
        help_text='Date when the task was created (YYYY-MM-DD)'
    )
    set_to_complete = serializers.BooleanField(
        help_text='Whether the task was completed (True or False)'
    )

    class Meta:
        model = Todo
        fields = '__all__'
