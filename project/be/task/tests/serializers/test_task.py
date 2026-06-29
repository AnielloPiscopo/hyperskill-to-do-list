import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from task.enums import TaskStatus
from task.models import Task
from task.serializers import TaskSerializer


class TaskSerializerTest(TestCase):
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
        # TaskSerializer excludes 'user' and 'is_archived'
        self.valid_data = {
            'title': 'New task',
            'description': 'New description',
            'goal_set_date': '2024-01-01',
            'set_to_complete': '2024-01-31',
            'status': TaskStatus.TODO,
        }

    # --- fields ---

    def test_contains_expected_fields(self):
        serializer = TaskSerializer(self.task)
        self.assertSetEqual(
            set(serializer.data.keys()),
            {'id', 'title', 'description', 'goal_set_date', 'set_to_complete',
             'status', 'board', 'updated_at', 'created_at'}
        )

    def test_user_field_excluded(self):
        serializer = TaskSerializer(self.task)
        self.assertNotIn('user', serializer.data)

    def test_is_archived_field_excluded(self):
        serializer = TaskSerializer(self.task)
        self.assertNotIn('is_archived', serializer.data)

    # --- serialization ---

    def test_serializes_task_fields_correctly(self):
        serializer = TaskSerializer(self.task)
        data = serializer.data
        self.assertEqual(data['title'], 'Test task')
        self.assertEqual(data['description'], 'Test description')
        self.assertEqual(data['goal_set_date'], '2024-01-01')
        self.assertEqual(data['set_to_complete'], '2024-01-31')

    def test_default_status_is_todo(self):
        serializer = TaskSerializer(self.task)
        self.assertEqual(serializer.data['status'], TaskStatus.TODO)

    # --- validation ---

    def test_valid_data_is_valid(self):
        serializer = TaskSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_missing_title_is_invalid(self):
        data = {**self.valid_data}
        del data['title']
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_missing_description_is_invalid(self):
        data = {**self.valid_data}
        del data['description']
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('description', serializer.errors)

    def test_missing_goal_set_date_is_invalid(self):
        data = {**self.valid_data}
        del data['goal_set_date']
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('goal_set_date', serializer.errors)

    def test_missing_set_to_complete_is_invalid(self):
        data = {**self.valid_data}
        del data['set_to_complete']
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('set_to_complete', serializer.errors)

    def test_title_exceeding_max_length_is_invalid(self):
        data = {**self.valid_data, 'title': 'x' * 51}
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_description_exceeding_max_length_is_invalid(self):
        data = {**self.valid_data, 'description': 'x' * 1025}
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('description', serializer.errors)

    def test_invalid_status_is_invalid(self):
        data = {**self.valid_data, 'status': 99}
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('status', serializer.errors)

    def test_invalid_date_format_is_invalid(self):
        data = {**self.valid_data, 'goal_set_date': 'not-a-date'}
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('goal_set_date', serializer.errors)

    # --- save ---

    def test_save_creates_task(self):
        serializer = TaskSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        task = serializer.save(user=self.user)
        self.assertIsInstance(task, Task)
        self.assertEqual(Task.objects.count(), 2)

    def test_update_task(self):
        serializer = TaskSerializer(self.task, data={**self.valid_data, 'title': 'Updated'})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        task = serializer.save()
        self.assertEqual(task.title, 'Updated')
