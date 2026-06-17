import datetime

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from todo.enums import TaskStatus
from todo.models import Todo


class TodoListViewTest(APITestCase):
    client: APIClient

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = '/tasks/'
        self.todo_data = {
            'task': 'Test task',
            'description': 'Test description',
            'goal_set_date': '2024-01-01',
            'set_to_complete': '2024-01-31',
            'status': TaskStatus.TODO,
            'todo_of': self.user.pk,
        }

    def test_list_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_unauthenticated_returns_401(self):
        self.client.force_authenticate(user=None)
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_todo(self):
        response = self.client.post(self.url, self.todo_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 1)

    def test_create_sets_todo_of_to_request_user(self):
        self.client.post(self.url, self.todo_data)
        self.assertEqual(Todo.objects.first().todo_of, self.user)

    def test_create_unauthenticated_returns_401(self):
        self.client.force_authenticate(user=None)
        self.client.logout()
        response = self.client.post(self.url, self.todo_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ordering_todo_before_done(self):
        Todo.objects.create(
            task='Done task',
            description='Desc',
            goal_set_date=datetime.date(2024, 1, 1),
            set_to_complete=datetime.date(2024, 1, 31),
            status=TaskStatus.DONE,
            todo_of=self.user
        )
        Todo.objects.create(
            task='Todo task',
            description='Desc',
            goal_set_date=datetime.date(2024, 1, 1),
            set_to_complete=datetime.date(2024, 1, 31),
            status=TaskStatus.TODO,
            todo_of=self.user
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data
        self.assertEqual(results[0]['task'], 'Todo task')
        self.assertEqual(results[1]['task'], 'Done task')


class TodoDetailViewTest(APITestCase):
    client: APIClient

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.todo = Todo.objects.create(
            task='Test task',
            description='Test description',
            goal_set_date=datetime.date(2024, 1, 1),
            set_to_complete=datetime.date(2024, 1, 31),
            todo_of=self.user
        )
        self.url = f'/tasks/{self.todo.pk}/'

    def test_retrieve_todo(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['task'], 'Test task')

    def test_update_todo_as_author(self):
        response = self.client.put(self.url, {
            'task': 'Updated task',
            'description': 'Updated description',
            'goal_set_date': '2024-01-01',
            'set_to_complete': '2024-01-31',
            'status': TaskStatus.TODO,
            'todo_of': self.user.pk,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.task, 'Updated task')

    def test_partial_update_todo_as_author(self):
        response = self.client.patch(self.url, {'status': TaskStatus.DONE})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.status, str(TaskStatus.DONE))

    def test_delete_todo_as_author(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 0)

    def test_update_todo_as_non_author_returns_403(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.put(self.url, {
            'task': 'Hacked task',
            'description': 'Hacked',
            'goal_set_date': '2024-01-01',
            'set_to_complete': '2024-01-31',
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_todo_as_non_author_returns_403(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_nonexistent_todo_returns_404(self):
        response = self.client.get('/tasks/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_unauthenticated_returns_401(self):
        self.client.force_authenticate(user=None)
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
