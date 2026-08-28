import datetime

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from board.models import Board
from task.models import Task


def _make_task(user, board=None, is_archived=False):
    return Task.objects.create(
        title='Task',
        description='Desc',
        goal_set_date=datetime.date(2024, 1, 1),
        set_to_complete=datetime.date(2024, 1, 31),
        user=user,
        board=board,
        is_archived=is_archived,
    )


class TaskMoveViewTest(APITestCase):
    client: APIClient

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.other_user = User.objects.create_user(username='other', password='pass')
        self.board = Board.objects.create(title='Board', user=self.user)
        self.task = _make_task(self.user)
        self.url = '/tasks/move/'

    # --- authentication ---

    def test_unauthenticated_returns_401(self):
        response = self.client.post(self.url, {'ids': [self.task.pk], 'board': self.board.pk}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- 400 paths ---

    def test_nonexistent_board_returns_400(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {'ids': [self.task.pk], 'board': 9999}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_board_not_owned_returns_400(self):
        self.client.force_authenticate(user=self.user)
        other_board = Board.objects.create(title='Other', user=self.other_user)
        response = self.client.post(self.url, {'ids': [self.task.pk], 'board': other_board.pk}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- 200 paths ---

    def test_valid_board_returns_200(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {'ids': [self.task.pk], 'board': self.board.pk}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_null_board_returns_200(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {'ids': [self.task.pk], 'board': None}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_detail_message_on_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {'ids': [self.task.pk], 'board': self.board.pk}, format='json')
        self.assertEqual(response.data['detail'], 'Tasks moved.')

    def test_task_board_is_updated_on_success(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(self.url, {'ids': [self.task.pk], 'board': self.board.pk}, format='json')
        self.task.refresh_from_db()
        self.assertEqual(self.task.board, self.board)


class TaskDestroyAllViewTest(APITestCase):
    client: APIClient

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.other_user = User.objects.create_user(username='user2', password='pass123')
        self.task1 = _make_task(self.user, is_archived=True)
        self.task2 = _make_task(self.user, is_archived=True)
        self.active_task = _make_task(self.user)
        self.other_task = _make_task(self.other_user, is_archived=True)

    # --- authentication ---

    def test_unauthenticated_returns_401(self):
        response = self.client.post('/tasks/delete-all/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- 400 paths ---

    def test_non_integer_ids_returns_400(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/tasks/delete-all/', {'ids': ['abc', 'def']}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ids_not_a_list_returns_400(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/tasks/delete-all/', {'ids': 'not-a-list'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- 200 paths ---

    def test_no_body_returns_200(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/tasks/delete-all/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_without_ids_deletes_all_archived_tasks(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/tasks/delete-all/', {}, format='json')
        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())
        self.assertFalse(Task.objects.filter(pk=self.task2.pk).exists())

    def test_with_ids_deletes_specific_tasks(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/tasks/delete-all/', {'ids': [self.task1.pk]}, format='json')
        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())
        self.assertTrue(Task.objects.filter(pk=self.task2.pk).exists())

    def test_with_empty_ids_deletes_all_archived(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/tasks/delete-all/', {'ids': []}, format='json')
        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())
        self.assertFalse(Task.objects.filter(pk=self.task2.pk).exists())

    def test_does_not_delete_active_tasks(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/tasks/delete-all/', {}, format='json')
        self.assertTrue(Task.objects.filter(pk=self.active_task.pk).exists())

    def test_does_not_affect_other_users_tasks(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/tasks/delete-all/', {}, format='json')
        self.assertTrue(Task.objects.filter(pk=self.other_task.pk).exists())

    def test_returns_detail_message(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/tasks/delete-all/', {}, format='json')
        self.assertEqual(response.data['detail'], 'Tasks deleted.')
