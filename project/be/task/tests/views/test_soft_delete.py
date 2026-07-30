import datetime

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from task.models import Task


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

def _make_task(user, is_archived=False):
    return Task.objects.create(
        title='Task',
        description='Desc',
        goal_set_date=datetime.date(2024, 1, 1),
        set_to_complete=datetime.date(2024, 1, 31),
        user=user,
        is_archived=is_archived,
    )