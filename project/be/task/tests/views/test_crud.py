import datetime

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from task.enums import TaskStatus
from task.models import Task

from board.models import Board


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
            'title': 'Test task',
            'description': 'Test description',
            'goal_set_date': '2024-01-01',
            'set_to_complete': '2024-01-31',
            'status': TaskStatus.TODO,
            'user': self.user.pk,
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
        self.assertEqual(Task.objects.count(), 1)

    def test_create_sets_todo_of_to_request_user(self):
        self.client.post(self.url, self.todo_data)
        self.assertEqual(Task.objects.first().user, self.user)

    def test_create_unauthenticated_returns_401(self):
        self.client.force_authenticate(user=None)
        self.client.logout()
        response = self.client.post(self.url, self.todo_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ordering_todo_before_done(self):
        Task.objects.create(
            title='Done task',
            description='Desc',
            goal_set_date=datetime.date(2024, 1, 1),
            set_to_complete=datetime.date(2024, 1, 31),
            status=TaskStatus.DONE,
            user=self.user
        )
        Task.objects.create(
            title='Todo task',
            description='Desc',
            goal_set_date=datetime.date(2024, 1, 1),
            set_to_complete=datetime.date(2024, 1, 31),
            status=TaskStatus.TODO,
            user=self.user
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(results[0]['title'], 'Todo task')
        self.assertEqual(results[1]['title'], 'Done task')

    def test_list_excludes_archived_tasks(self):
        Task.objects.create(
            title='Archived task',
            description='Desc',
            goal_set_date=datetime.date(2024, 1, 1),
            set_to_complete=datetime.date(2024, 1, 31),
            user=self.user,
            is_archived=True
        )
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 0)

    def test_list_excludes_other_user_tasks(self):
        other_user = User.objects.create_user(username='other', password='pass')
        Task.objects.create(
            title='Other task',
            description='Desc',
            goal_set_date=datetime.date(2024, 1, 1),
            set_to_complete=datetime.date(2024, 1, 31),
            user=other_user
        )
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 0)

    def test_filter_by_status(self):
        Task.objects.create(
            title='Todo task',
            description='Desc',
            goal_set_date=datetime.date(2024, 1, 1),
            set_to_complete=datetime.date(2024, 1, 31),
            status=TaskStatus.TODO,
            user=self.user
        )
        Task.objects.create(
            title='Done task',
            description='Desc',
            goal_set_date=datetime.date(2024, 1, 1),
            set_to_complete=datetime.date(2024, 1, 31),
            status=TaskStatus.DONE,
            user=self.user
        )
        response = self.client.get(self.url, {'status': TaskStatus.TODO})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Todo task')

    def test_filter_by_board(self):
        board = Board.objects.create(title='Board 1', user=self.user)
        Task.objects.create(
            title='Task with board',
            description='Desc',
            goal_set_date=datetime.date(2024, 1, 1),
            set_to_complete=datetime.date(2024, 1, 31),
            user=self.user,
            board=board
        )
        Task.objects.create(
            title='Task without board',
            description='Desc',
            goal_set_date=datetime.date(2024, 1, 1),
            set_to_complete=datetime.date(2024, 1, 31),
            user=self.user
        )
        response = self.client.get(self.url, {'board': board.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Task with board')

    def test_search_by_title(self):
        Task.objects.create(
            title='Meeting task',
            description='Desc',
            goal_set_date=datetime.date(2024, 1, 1),
            set_to_complete=datetime.date(2024, 1, 31),
            user=self.user
        )
        Task.objects.create(
            title='Other task',
            description='Desc',
            goal_set_date=datetime.date(2024, 1, 1),
            set_to_complete=datetime.date(2024, 1, 31),
            user=self.user
        )
        response = self.client.get(self.url, {'search': 'Meeting'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Meeting task')

    def test_search_by_description(self):
        Task.objects.create(
            title='Task 1',
            description='Contains meeting notes',
            goal_set_date=datetime.date(2024, 1, 1),
            set_to_complete=datetime.date(2024, 1, 31),
            user=self.user
        )
        Task.objects.create(
            title='Task 2',
            description='Other description',
            goal_set_date=datetime.date(2024, 1, 1),
            set_to_complete=datetime.date(2024, 1, 31),
            user=self.user
        )
        response = self.client.get(self.url, {'search': 'meeting'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Task 1')

    def test_ordering_by_set_to_complete(self):
        Task.objects.create(
            title='Later task',
            description='Desc',
            goal_set_date=datetime.date(2024, 1, 1),
            set_to_complete=datetime.date(2024, 2, 28),
            user=self.user
        )
        Task.objects.create(
            title='Earlier task',
            description='Desc',
            goal_set_date=datetime.date(2024, 1, 1),
            set_to_complete=datetime.date(2024, 1, 15),
            user=self.user
        )
        response = self.client.get(self.url, {'ordering': 'set_to_complete'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'Earlier task')
        self.assertEqual(response.data['results'][1]['title'], 'Later task')


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
        self.todo = Task.objects.create(
            title='Test task',
            description='Test description',
            goal_set_date=datetime.date(2024, 1, 1),
            set_to_complete=datetime.date(2024, 1, 31),
            user=self.user
        )
        self.url = f'/tasks/{self.todo.pk}/'

    def test_retrieve_todo(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test task')

    def test_update_todo_as_author(self):
        response = self.client.put(self.url, {
            'title': 'Updated task',
            'description': 'Updated description',
            'goal_set_date': '2024-01-01',
            'set_to_complete': '2024-01-31',
            'status': TaskStatus.TODO,
            'user': self.user.pk,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated task')

    def test_partial_update_todo_as_author(self):
        response = self.client.patch(self.url, {'status': TaskStatus.DONE})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.status, str(TaskStatus.DONE))

    def test_delete_todo_as_author(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_update_todo_as_non_author_returns_404(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.put(self.url, {
            'title': 'Hacked task',
            'description': 'Hacked',
            'goal_set_date': '2024-01-01',
            'set_to_complete': '2024-01-31',
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_todo_as_non_author_returns_404(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_nonexistent_todo_returns_404(self):
        response = self.client.get('/tasks/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_unauthenticated_returns_401(self):
        self.client.force_authenticate(user=None)
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_other_user_task_returns_404(self):
        other_user = User.objects.create_user(username='other', password='pass')
        task = Task.objects.create(
            title='Other task',
            description='Desc',
            goal_set_date=datetime.date(2024, 1, 1),
            set_to_complete=datetime.date(2024, 1, 31),
            user=other_user
        )
        response = self.client.get(f'/tasks/{task.pk}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


def _make_task(user, is_archived=False):
    return Task.objects.create(
        title='Task',
        description='Desc',
        goal_set_date=datetime.date(2024, 1, 1),
        set_to_complete=datetime.date(2024, 1, 31),
        user=user,
        is_archived=is_archived,
    )


class TaskArchiveViewTest(APITestCase):
    client: APIClient

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.other_user = User.objects.create_user(username='user2', password='pass123')
        self.task = _make_task(self.user)

    def _url(self, pk=None):
        return f'/tasks/{pk or self.task.pk}/archive/'

    def test_archive_unauthenticated_returns_401(self):
        response = self.client.post(self._url())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_archive_task_returns_200(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self._url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_archive_task_sets_is_archived(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(self._url())
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_archived)

    def test_archive_already_archived_task_returns_404(self):
        self.task.is_archived = True
        self.task.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self._url())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_archive_nonexistent_task_returns_404(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self._url(pk=9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_archive_other_user_task_returns_404(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(self._url())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_archive_returns_detail_message(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self._url())
        self.assertEqual(response.data['detail'], 'Task archived.')


class TaskRestoreViewTest(APITestCase):
    client: APIClient

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.other_user = User.objects.create_user(username='user2', password='pass123')
        self.task = _make_task(self.user, is_archived=True)

    def _url(self, pk=None):
        return f'/tasks/{pk or self.task.pk}/restore/'

    def test_restore_unauthenticated_returns_401(self):
        response = self.client.post(self._url())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_restore_task_returns_200(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self._url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restore_task_sets_is_archived_false(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(self._url())
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_archived)

    def test_restore_non_archived_task_returns_404(self):
        self.task.is_archived = False
        self.task.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self._url())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_restore_nonexistent_task_returns_404(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self._url(pk=9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_restore_other_user_task_returns_404(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(self._url())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_restore_returns_detail_message(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self._url())
        self.assertEqual(response.data['detail'], 'Task restored.')


class TaskArchiveAllViewTest(APITestCase):
    client: APIClient

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.other_user = User.objects.create_user(username='user2', password='pass123')
        self.task1 = _make_task(self.user)
        self.task2 = _make_task(self.user)
        self.other_task = _make_task(self.other_user)

    def test_archive_all_unauthenticated_returns_401(self):
        response = self.client.post('/tasks/archive-all/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_archive_all_returns_200(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/tasks/archive-all/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_archive_all_without_ids_archives_all_tasks(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/tasks/archive-all/', {}, format='json')
        self.task1.refresh_from_db()
        self.task2.refresh_from_db()
        self.assertTrue(self.task1.is_archived)
        self.assertTrue(self.task2.is_archived)

    def test_archive_all_with_ids_archives_specific_tasks(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/tasks/archive-all/', {'ids': [self.task1.pk]}, format='json')
        self.task1.refresh_from_db()
        self.task2.refresh_from_db()
        self.assertTrue(self.task1.is_archived)
        self.assertFalse(self.task2.is_archived)

    def test_archive_all_with_empty_ids_archives_all(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/tasks/archive-all/', {'ids': []}, format='json')
        self.task1.refresh_from_db()
        self.task2.refresh_from_db()
        self.assertTrue(self.task1.is_archived)
        self.assertTrue(self.task2.is_archived)

    def test_archive_all_does_not_affect_other_users_tasks(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/tasks/archive-all/', {}, format='json')
        self.other_task.refresh_from_db()
        self.assertFalse(self.other_task.is_archived)

    def test_archive_all_returns_detail_message(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/tasks/archive-all/', {}, format='json')
        self.assertEqual(response.data['detail'], 'Tasks archived.')


class TaskRestoreAllViewTest(APITestCase):
    client: APIClient

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.other_user = User.objects.create_user(username='user2', password='pass123')
        self.task1 = _make_task(self.user, is_archived=True)
        self.task2 = _make_task(self.user, is_archived=True)
        self.other_task = _make_task(self.other_user, is_archived=True)

    def test_restore_all_unauthenticated_returns_401(self):
        response = self.client.post('/tasks/restore-all/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_restore_all_returns_200(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/tasks/restore-all/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restore_all_without_ids_restores_all_tasks(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/tasks/restore-all/', {}, format='json')
        self.task1.refresh_from_db()
        self.task2.refresh_from_db()
        self.assertFalse(self.task1.is_archived)
        self.assertFalse(self.task2.is_archived)

    def test_restore_all_with_ids_restores_specific_tasks(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/tasks/restore-all/', {'ids': [self.task1.pk]}, format='json')
        self.task1.refresh_from_db()
        self.task2.refresh_from_db()
        self.assertFalse(self.task1.is_archived)
        self.assertTrue(self.task2.is_archived)

    def test_restore_all_with_empty_ids_restores_all(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/tasks/restore-all/', {'ids': []}, format='json')
        self.task1.refresh_from_db()
        self.task2.refresh_from_db()
        self.assertFalse(self.task1.is_archived)
        self.assertFalse(self.task2.is_archived)

    def test_restore_all_does_not_affect_other_users_tasks(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/tasks/restore-all/', {}, format='json')
        self.other_task.refresh_from_db()
        self.assertTrue(self.other_task.is_archived)

    def test_restore_all_returns_detail_message(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/tasks/restore-all/', {}, format='json')
        self.assertEqual(response.data['detail'], 'Tasks restored.')
