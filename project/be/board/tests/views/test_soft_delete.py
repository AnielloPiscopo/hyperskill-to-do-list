import datetime

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from board.models import Board
from task.models import Task


class BoardArchiveViewTest(APITestCase):
    client: APIClient

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.other_user = User.objects.create_user(username='user2', password='pass123')
        self.board = Board.objects.create(title='Board 1', user=self.user)
        self.task = _make_task(self.user, board=self.board)

    def _url(self, slug=None):
        return f'/boards/{slug or self.board.slug}/archive/'

    def test_archive_unauthenticated_returns_401(self):
        response = self.client.post(self._url())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_archive_board_returns_200(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self._url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_archive_board_sets_is_archived(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(self._url())
        self.board.refresh_from_db()
        self.assertTrue(self.board.is_archived)

    def test_archive_board_archives_tasks(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(self._url())
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_archived)

    def test_archive_already_archived_board_returns_404(self):
        self.board.is_archived = True
        self.board.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self._url())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_archive_nonexistent_board_returns_404(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self._url(slug='nonexistent-slug'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_archive_other_user_board_returns_404(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(self._url())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_archive_returns_detail_message(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self._url())
        self.assertEqual(response.data['detail'], 'Board archived.')


class BoardRestoreViewTest(APITestCase):
    client: APIClient

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.other_user = User.objects.create_user(username='user2', password='pass123')
        self.board = Board.objects.create(title='Board 1', user=self.user, is_archived=True)
        self.task = _make_task(self.user, board=self.board, is_archived=True)

    def _url(self, slug=None):
        return f'/boards/{slug or self.board.slug}/restore/'

    def test_restore_unauthenticated_returns_401(self):
        response = self.client.post(self._url())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_restore_board_returns_200(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self._url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restore_board_sets_is_archived_false(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(self._url())
        self.board.refresh_from_db()
        self.assertFalse(self.board.is_archived)

    def test_restore_non_archived_board_returns_404(self):
        self.board.is_archived = False
        self.board.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self._url())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_restore_nonexistent_board_returns_404(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self._url(slug='nonexistent-slug'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_restore_other_user_board_returns_404(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(self._url())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_restore_with_restore_tasks_true(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(self._url() + '?restore_tasks=true')
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_archived)

    def test_restore_without_restore_tasks_leaves_tasks_archived(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(self._url())
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_archived)

    def test_restore_returns_detail_message(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self._url())
        self.assertEqual(response.data['detail'], 'Board restored.')


class BoardArchiveAllViewTest(APITestCase):
    client: APIClient

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.other_user = User.objects.create_user(username='user2', password='pass123')
        self.board1 = Board.objects.create(title='Board 1', user=self.user)
        self.board2 = Board.objects.create(title='Board 2', user=self.user)
        self.other_board = Board.objects.create(title='Other Board', user=self.other_user)

    def test_archive_all_unauthenticated_returns_401(self):
        response = self.client.post('/boards/archive-all/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_archive_all_returns_200(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/boards/archive-all/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_archive_all_without_ids_archives_all_boards(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/boards/archive-all/', {}, format='json')
        self.board1.refresh_from_db()
        self.board2.refresh_from_db()
        self.assertTrue(self.board1.is_archived)
        self.assertTrue(self.board2.is_archived)

    def test_archive_all_with_ids_archives_specific_boards(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/boards/archive-all/', {'ids': [self.board1.pk]}, format='json')
        self.board1.refresh_from_db()
        self.board2.refresh_from_db()
        self.assertTrue(self.board1.is_archived)
        self.assertFalse(self.board2.is_archived)

    def test_archive_all_with_empty_ids_archives_all(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/boards/archive-all/', {'ids': []}, format='json')
        self.board1.refresh_from_db()
        self.board2.refresh_from_db()
        self.assertTrue(self.board1.is_archived)
        self.assertTrue(self.board2.is_archived)

    def test_archive_all_does_not_affect_other_users_boards(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/boards/archive-all/', {}, format='json')
        self.other_board.refresh_from_db()
        self.assertFalse(self.other_board.is_archived)

    def test_archive_all_returns_detail_message(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/boards/archive-all/', {}, format='json')
        self.assertEqual(response.data['detail'], 'Boards archived.')

    def test_archive_all_with_non_integer_ids_returns_400(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/boards/archive-all/', {'ids': ['abc', 'def']}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_archive_all_with_ids_not_a_list_returns_400(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/boards/archive-all/', {'ids': 'not-a-list'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_archive_all_with_invalid_ids_does_not_archive_anything(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/boards/archive-all/', {'ids': ['abc']}, format='json')
        self.board1.refresh_from_db()
        self.board2.refresh_from_db()
        self.assertFalse(self.board1.is_archived)
        self.assertFalse(self.board2.is_archived)


class BoardRestoreAllViewTest(APITestCase):
    client: APIClient

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.other_user = User.objects.create_user(username='user2', password='pass123')
        self.board1 = Board.objects.create(title='Board 1', user=self.user, is_archived=True)
        self.board2 = Board.objects.create(title='Board 2', user=self.user, is_archived=True)
        self.other_board = Board.objects.create(title='Other Board', user=self.other_user, is_archived=True)
        self.task1 = _make_task(self.user, board=self.board1, is_archived=True)

    def test_restore_all_unauthenticated_returns_401(self):
        response = self.client.post('/boards/restore-all/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_restore_all_returns_200(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/boards/restore-all/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restore_all_without_ids_restores_all_boards(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/boards/restore-all/', {}, format='json')
        self.board1.refresh_from_db()
        self.board2.refresh_from_db()
        self.assertFalse(self.board1.is_archived)
        self.assertFalse(self.board2.is_archived)

    def test_restore_all_with_ids_restores_specific_boards(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/boards/restore-all/', {'ids': [self.board1.pk]}, format='json')
        self.board1.refresh_from_db()
        self.board2.refresh_from_db()
        self.assertFalse(self.board1.is_archived)
        self.assertTrue(self.board2.is_archived)

    def test_restore_all_with_empty_ids_restores_all(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/boards/restore-all/', {'ids': []}, format='json')
        self.board1.refresh_from_db()
        self.board2.refresh_from_db()
        self.assertFalse(self.board1.is_archived)
        self.assertFalse(self.board2.is_archived)

    def test_restore_all_with_restore_tasks_true(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/boards/restore-all/?restore_tasks=true', {}, format='json')
        self.task1.refresh_from_db()
        self.assertFalse(self.task1.is_archived)

    def test_restore_all_without_restore_tasks_leaves_tasks_archived(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/boards/restore-all/', {}, format='json')
        self.task1.refresh_from_db()
        self.assertTrue(self.task1.is_archived)

    def test_restore_all_does_not_affect_other_users_boards(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/boards/restore-all/', {}, format='json')
        self.other_board.refresh_from_db()
        self.assertTrue(self.other_board.is_archived)

    def test_restore_all_returns_detail_message(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/boards/restore-all/', {}, format='json')
        self.assertEqual(response.data['detail'], 'Boards restored.')

    def test_restore_all_with_non_integer_ids_returns_400(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/boards/restore-all/', {'ids': ['abc', 'def']}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_restore_all_with_ids_not_a_list_returns_400(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/boards/restore-all/', {'ids': 'not-a-list'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_restore_all_with_invalid_ids_does_not_restore_anything(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/boards/restore-all/', {'ids': ['abc']}, format='json')
        self.board1.refresh_from_db()
        self.board2.refresh_from_db()
        self.assertTrue(self.board1.is_archived)
        self.assertTrue(self.board2.is_archived)

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