import datetime

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from board.models import Board
from task.models import Task


class BoardListViewTest(APITestCase):
    client: APIClient

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.other_user = User.objects.create_user(username='user2', password='pass123')
        self.board = Board.objects.create(title='Board 1', user=self.user)

    # --- authentication ---

    def test_list_unauthenticated_returns_401(self):
        response = self.client.get('/boards/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_unauthenticated_returns_401(self):
        response = self.client.post('/boards/', {'title': 'New'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- GET ---

    def test_list_returns_200(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/boards/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_returns_only_current_user_boards(self):
        Board.objects.create(title='Other Board', user=self.other_user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/boards/')
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Board 1')

    def test_list_excludes_archived_boards(self):
        self.board.is_archived = True
        self.board.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/boards/')
        self.assertEqual(response.data['count'], 0)

    def test_list_ordered_by_title(self):
        Board.objects.create(title='Alpha', user=self.user)
        Board.objects.create(title='Zeta', user=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/boards/')
        titles = [b['title'] for b in response.data['results']]
        self.assertEqual(titles, sorted(titles))

    # --- POST ---

    def test_create_returns_201(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/boards/', {'title': 'New Board'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_sets_user_to_current_user(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/boards/', {'title': 'New Board'})
        board = Board.objects.get(title='New Board')
        self.assertEqual(board.user, self.user)

    def test_create_missing_title_returns_400(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/boards/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- search ---

    def test_search_by_title(self):
        Board.objects.create(title='Meeting board', user=self.user)
        Board.objects.create(title='Other board', user=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/boards/', {'search': 'Meeting'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Meeting board')

    def test_search_by_description(self):
        Board.objects.create(title='Board 1', description='Contains meeting notes', user=self.user)
        Board.objects.create(title='Board 2', description='Other description', user=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/boards/', {'search': 'meeting'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Board 1')

    # --- ordering ---

    def test_ordering_by_title(self):
        Board.objects.create(title='Zeta', user=self.user)
        Board.objects.create(title='Alpha', user=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/boards/', {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [b['title'] for b in response.data['results']]
        self.assertEqual(titles, sorted(titles))

    def test_ordering_by_created_at_desc(self):
        Board.objects.create(title='Second board', user=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/boards/', {'ordering': '-created_at'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'Second board')


class BoardDetailViewTest(APITestCase):
    client: APIClient

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.other_user = User.objects.create_user(username='user2', password='pass123')
        self.board = Board.objects.create(title='Board 1', user=self.user)

    def _url(self):
        return f'/boards/{self.board.pk}/'

    # --- authentication ---

    def test_retrieve_unauthenticated_returns_401(self):
        response = self.client.get(self._url())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- GET ---

    def test_retrieve_author_returns_200(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self._url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_non_author_returns_404(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self._url())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_archived_board_returns_404(self):
        self.board.is_archived = True
        self.board.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self._url())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # --- PUT ---

    def test_update_author_returns_200(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self._url(), {'title': 'Updated'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_non_author_returns_404(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.put(self._url(), {'title': 'Updated'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_persists_changes(self):
        self.client.force_authenticate(user=self.user)
        self.client.put(self._url(), {'title': 'Updated Title'})
        self.board.refresh_from_db()
        self.assertEqual(self.board.title, 'Updated Title')

    # --- PATCH ---

    def test_partial_update_author_returns_200(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self._url(), {'title': 'Patched'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_non_author_returns_404(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.patch(self._url(), {'title': 'Patched'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # --- DELETE ---

    def test_delete_author_returns_204(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self._url())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_removes_board(self):
        self.client.force_authenticate(user=self.user)
        self.client.delete(self._url())
        self.assertFalse(Board.objects.filter(pk=self.board.pk).exists())

    def test_delete_non_author_returns_404(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self._url())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


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


class BoardArchiveViewTest(APITestCase):
    client: APIClient

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.other_user = User.objects.create_user(username='user2', password='pass123')
        self.board = Board.objects.create(title='Board 1', user=self.user)
        self.task = _make_task(self.user, board=self.board)

    def _url(self, pk=None):
        return f'/boards/{pk or self.board.pk}/archive/'

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
        response = self.client.post(self._url(pk=9999))
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

    def _url(self, pk=None):
        return f'/boards/{pk or self.board.pk}/restore/'

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
        response = self.client.post(self._url(pk=9999))
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
