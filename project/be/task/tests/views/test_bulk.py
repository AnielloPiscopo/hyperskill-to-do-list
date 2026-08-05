import datetime

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from board.models import Board
from task.models import Task


def _make_task(user, board=None):
    return Task.objects.create(
        title='Task',
        description='Desc',
        goal_set_date=datetime.date(2024, 1, 1),
        set_to_complete=datetime.date(2024, 1, 31),
        user=user,
        board=board,
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
