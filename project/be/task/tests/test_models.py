import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from task.enums import TaskStatus, TaskPriority
from task.models import Task


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.task = Task.objects.create(
            title='Test task',
            description='Test description',
            goal_set_date=datetime.date(2024, 1, 1),
            set_to_complete=datetime.date(2024, 1, 31),
            user=self.user
        )

    def test_todo_creation(self):
        self.assertIsInstance(self.task, Task)

    def test_default_status_is_todo(self):
        self.assertEqual(self.task.status, TaskStatus.TODO)

    def test_default_priority_is_zero(self):
        self.assertEqual(self.task.priority, TaskPriority.ZERO)

    def test_todo_fields(self):
        self.assertEqual(self.task.title, 'Test task')
        self.assertEqual(self.task.description, 'Test description')
        self.assertEqual(self.task.goal_set_date, datetime.date(2024, 1, 1))
        self.assertEqual(self.task.set_to_complete, datetime.date(2024, 1, 31))

    def test_todo_of_relation(self):
        self.assertEqual(self.task.user, self.user)

    def test_cascade_delete_on_user_deletion(self):
        self.user.delete()
        self.assertEqual(Task.objects.count(), 0)

    def test_task_max_length(self):
        max_length = Task._meta.get_field('title').max_length
        self.assertEqual(max_length, 50)

    def test_description_max_length(self):
        max_length = Task._meta.get_field('description').max_length
        self.assertEqual(max_length, 1024)

    def test_str_returns_task_name(self):
        self.assertEqual(str(self.task), 'Test task')

    def test_repr_contains_id_task_and_status(self):
        expected = (f'Task(id={self.task.id!r}, title={self.task.title!r}, description={self.task.description!r}, '
                    f'status={self.task.status!r}), priority={self.task.priority!r}')
        self.assertEqual(repr(self.task), expected)