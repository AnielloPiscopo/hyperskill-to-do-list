import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from todo.models import Todo
from todo.serializers import TodoSerializer


class TodoSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.valid_data = {
            'task': 'Test task',
            'description': 'Test description',
            'goal_set_date': datetime.date(2024, 1, 1),
            'set_to_complete': datetime.date(2024, 1, 31),
            'is_completed': False,
            'todo_of': self.user.pk,
        }

    def test_valid_data_is_valid(self):
        serializer = TodoSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_serializer_expected_fields(self):
        todo = Todo.objects.create(
            task='Test task',
            description='Test description',
            goal_set_date=datetime.date(2024, 1, 1),
            set_to_complete=datetime.date(2024, 1, 31),
            todo_of=self.user
        )
        serializer = TodoSerializer(todo)
        expected_fields = {'id', 'task', 'description', 'goal_set_date', 'set_to_complete', 'is_completed', 'todo_of'}
        self.assertEqual(set(serializer.data.keys()), expected_fields)

    def test_missing_task_is_invalid(self):
        data = self.valid_data.copy()
        data.pop('task')
        serializer = TodoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('task', serializer.errors)

    def test_missing_description_is_invalid(self):
        data = self.valid_data.copy()
        data.pop('description')
        serializer = TodoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('description', serializer.errors)

    def test_create_saves_todo_instance(self):
        serializer = TodoSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        todo = serializer.save()
        self.assertIsInstance(todo, Todo)
        self.assertEqual(todo.task, 'Test task')
        self.assertEqual(todo.todo_of, self.user)
