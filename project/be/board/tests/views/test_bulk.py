from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from board.models import Board


class BoardDestroyAllViewTest(APITestCase):
    client: APIClient

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.other_user = User.objects.create_user(username='user2', password='pass123')
        self.board1 = Board.objects.create(title='Board 1', user=self.user, is_archived=True)
        self.board2 = Board.objects.create(title='Board 2', user=self.user, is_archived=True)
        self.active_board = Board.objects.create(title='Active Board', user=self.user)
        self.other_board = Board.objects.create(title='Other Board', user=self.other_user, is_archived=True)

    # --- authentication ---

    def test_unauthenticated_returns_401(self):
        response = self.client.post('/boards/delete-all/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- 400 paths ---

    def test_non_integer_ids_returns_400(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/boards/delete-all/', {'ids': ['abc', 'def']}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ids_not_a_list_returns_400(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/boards/delete-all/', {'ids': 'not-a-list'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- 200 paths ---

    def test_no_body_returns_200(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/boards/delete-all/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_without_ids_deletes_all_archived_boards(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/boards/delete-all/', {}, format='json')
        self.assertFalse(Board.objects.filter(pk=self.board1.pk).exists())
        self.assertFalse(Board.objects.filter(pk=self.board2.pk).exists())

    def test_with_ids_deletes_specific_boards(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/boards/delete-all/', {'ids': [self.board1.pk]}, format='json')
        self.assertFalse(Board.objects.filter(pk=self.board1.pk).exists())
        self.assertTrue(Board.objects.filter(pk=self.board2.pk).exists())

    def test_with_empty_ids_deletes_all_archived(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/boards/delete-all/', {'ids': []}, format='json')
        self.assertFalse(Board.objects.filter(pk=self.board1.pk).exists())
        self.assertFalse(Board.objects.filter(pk=self.board2.pk).exists())

    def test_does_not_delete_active_boards(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/boards/delete-all/', {}, format='json')
        self.assertTrue(Board.objects.filter(pk=self.active_board.pk).exists())

    def test_does_not_affect_other_users_boards(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/boards/delete-all/', {}, format='json')
        self.assertTrue(Board.objects.filter(pk=self.other_board.pk).exists())

    def test_returns_detail_message(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/boards/delete-all/', {}, format='json')
        self.assertEqual(response.data['detail'], 'Boards deleted.')
