from django.contrib.auth.models import User
from django.test import TestCase

from board.models import Board
from board.services.bulk import delete_boards


class DeleteBoardsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.other_user = User.objects.create_user(username='other', password='pass')
        self.board1 = Board.objects.create(title='Board 1', user=self.user, is_archived=True)
        self.board2 = Board.objects.create(title='Board 2', user=self.user, is_archived=True)
        self.active_board = Board.objects.create(title='Active Board', user=self.user)

    def test_deletes_all_archived_boards_when_ids_is_none(self):
        delete_boards(self.user, ids=None)
        self.assertFalse(Board.objects.filter(pk=self.board1.pk).exists())
        self.assertFalse(Board.objects.filter(pk=self.board2.pk).exists())

    def test_deletes_specific_boards_when_ids_provided(self):
        delete_boards(self.user, ids=[self.board1.pk])
        self.assertFalse(Board.objects.filter(pk=self.board1.pk).exists())
        self.assertTrue(Board.objects.filter(pk=self.board2.pk).exists())

    def test_empty_ids_list_deletes_all_archived(self):
        delete_boards(self.user, ids=[])
        self.assertFalse(Board.objects.filter(pk=self.board1.pk).exists())
        self.assertFalse(Board.objects.filter(pk=self.board2.pk).exists())

    def test_does_not_delete_active_boards(self):
        delete_boards(self.user, ids=None)
        self.assertTrue(Board.objects.filter(pk=self.active_board.pk).exists())

    def test_does_not_delete_other_users_boards(self):
        other_board = Board.objects.create(title='Other', user=self.other_user, is_archived=True)
        delete_boards(self.user, ids=None)
        self.assertTrue(Board.objects.filter(pk=other_board.pk).exists())
