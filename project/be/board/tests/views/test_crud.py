from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from board.models import Board


class BoardListViewTest(APITestCase):
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
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Board 1')

    def test_list_excludes_archived_boards(self):
        self.board.is_archived = True
        self.board.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/boards/')
        self.assertEqual(len(response.data), 0)

    def test_list_ordered_by_title(self):
        Board.objects.create(title='Alpha', user=self.user)
        Board.objects.create(title='Zeta', user=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/boards/')
        titles = [b['title'] for b in response.data]
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


class BoardDetailViewTest(APITestCase):
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
