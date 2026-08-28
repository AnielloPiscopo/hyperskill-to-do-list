from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from board.models import Board, BoardSlugHistory


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

    def test_list_archived_boards_with_filter(self):
        self.board.is_archived = True
        self.board.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/boards/', {'is_archived': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Board 1')

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

    def test_create_response_contains_slug(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/boards/', {'title': 'New Board'})
        self.assertIn('slug', response.data)
        self.assertEqual(response.data['slug'], 'new-board')

    def test_slug_is_ignored_when_provided_in_create(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/boards/', {'title': 'New Board', 'slug': 'custom-slug'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['slug'], 'new-board')

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

    def _url(self, slug=None):
        return f'/boards/{slug or self.board.slug}/'

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

    def test_retrieve_archived_board_returns_200(self):
        self.board.is_archived = True
        self.board.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self._url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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

    def test_delete_active_board_returns_400(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self._url())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_archived_board_returns_204(self):
        self.board.is_archived = True
        self.board.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self._url())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_archived_board_removes_it(self):
        self.board.is_archived = True
        self.board.save()
        self.client.force_authenticate(user=self.user)
        self.client.delete(self._url())
        self.assertFalse(Board.objects.filter(pk=self.board.pk).exists())

    def test_delete_non_author_returns_404(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self._url())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_archived_board_returns_400(self):
        self.board.is_archived = True
        self.board.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self._url(), {'title': 'Updated'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_archived_board_returns_400(self):
        self.board.is_archived = True
        self.board.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self._url(), {'title': 'Patched'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- slug routing ---

    def test_retrieve_uses_slug_in_url(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self._url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], self.board.slug)

    def test_get_unknown_slug_returns_404(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self._url(slug='nonexistent-slug'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_old_slug_returns_moved_to(self):
        old_slug = 'old-board-slug'
        BoardSlugHistory.objects.create(board=self.board, slug=old_slug)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self._url(slug=old_slug))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['moved_to'], self.board.slug)

    def test_get_old_slug_of_other_user_board_returns_404(self):
        other_board = Board.objects.create(title='Other Board', user=self.other_user)
        old_slug = 'old-other-slug'
        BoardSlugHistory.objects.create(board=other_board, slug=old_slug)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self._url(slug=old_slug))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_changes_slug(self):
        self.client.force_authenticate(user=self.user)
        self.client.put(self._url(), {'title': 'New Title'})
        self.board.refresh_from_db()
        self.assertEqual(self.board.slug, 'new-title')
