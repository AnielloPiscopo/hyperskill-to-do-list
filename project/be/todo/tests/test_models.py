import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from todo.models import Todo


class TodoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.todo = Todo.objects.create(
            task='Test task',
            description='Test description',
            goal_set_date=datetime.date(2024, 1, 1),
            set_to_complete=datetime.date(2024, 1, 31),
            todo_of=self.user
        )

    def test_todo_creation(self):
        self.assertIsInstance(self.todo, Todo)

    def test_default_is_completed_is_false(self):
        self.assertFalse(self.todo.is_completed)

    def test_todo_fields(self):
        self.assertEqual(self.todo.task, 'Test task')
        self.assertEqual(self.todo.description, 'Test description')
        self.assertEqual(self.todo.goal_set_date, datetime.date(2024, 1, 1))
        self.assertEqual(self.todo.set_to_complete, datetime.date(2024, 1, 31))

    def test_todo_of_relation(self):
        self.assertEqual(self.todo.todo_of, self.user)

    def test_cascade_delete_on_user_deletion(self):
        self.user.delete()
        self.assertEqual(Todo.objects.count(), 0)

    def test_task_max_length(self):
        max_length = Todo._meta.get_field('task').max_length
        self.assertEqual(max_length, 50)

    def test_description_max_length(self):
        max_length = Todo._meta.get_field('description').max_length
        self.assertEqual(max_length, 1024)