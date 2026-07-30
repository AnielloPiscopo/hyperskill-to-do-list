import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from board.models import Board
from board.services.soft_delete import archive_board, restore_board, archive_boards, restore_boards
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


class ArchiveBoardTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.board = Board.objects.create(title='Board', user=self.user)
        self.task = _make_task(self.user, board=self.board)

    def test_archive_board_sets_is_archived_true(self):
        archive_board(self.board)
        self.board.refresh_from_db()
        self.assertTrue(self.board.is_archived)

    def test_archive_board_archives_all_tasks(self):
        archive_board(self.board)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_archived)

    def test_archive_board_with_no_tasks(self):
        empty_board = Board.objects.create(title='Empty', user=self.user)
        archive_board(empty_board)
        empty_board.refresh_from_db()
        self.assertTrue(empty_board.is_archived)


class RestoreBoardTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.board = Board.objects.create(title='Board', user=self.user, is_archived=True)
        self.task = _make_task(self.user, board=self.board, is_archived=True)

    def test_restore_board_sets_is_archived_false(self):
        restore_board(self.board)
        self.board.refresh_from_db()
        self.assertFalse(self.board.is_archived)

    def test_restore_board_does_not_restore_tasks_by_default(self):
        restore_board(self.board)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_archived)

    def test_restore_board_restores_tasks_when_flag_is_true(self):
        restore_board(self.board, restore_tasks=True)
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_archived)

    def test_restore_board_with_restore_tasks_false_leaves_tasks_archived(self):
        restore_board(self.board, restore_tasks=False)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_archived)


class ArchiveBoardsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.board1 = Board.objects.create(title='Board 1', user=self.user)
        self.board2 = Board.objects.create(title='Board 2', user=self.user)
        self.task1 = _make_task(self.user, board=self.board1)

    def test_archive_boards_archives_all_user_boards(self):
        archive_boards(self.user)
        self.board1.refresh_from_db()
        self.board2.refresh_from_db()
        self.assertTrue(self.board1.is_archived)
        self.assertTrue(self.board2.is_archived)

    def test_archive_boards_archives_specific_ids(self):
        archive_boards(self.user, ids=[self.board1.pk])
        self.board1.refresh_from_db()
        self.board2.refresh_from_db()
        self.assertTrue(self.board1.is_archived)
        self.assertFalse(self.board2.is_archived)

    def test_archive_boards_skips_already_archived(self):
        self.board1.is_archived = True
        self.board1.save()
        archive_boards(self.user)
        self.board2.refresh_from_db()
        self.assertTrue(self.board2.is_archived)
        # board1 was already archived, not re-processed
        self.assertEqual(Board.objects.filter(is_archived=True).count(), 2)

    def test_archive_boards_does_not_archive_other_users_boards(self):
        other_user = User.objects.create_user(username='other', password='pass')
        other_board = Board.objects.create(title='Other Board', user=other_user)
        archive_boards(self.user)
        other_board.refresh_from_db()
        self.assertFalse(other_board.is_archived)

    def test_archive_boards_with_empty_ids_archives_all(self):
        # ids=None means archive all
        archive_boards(self.user, ids=None)
        self.board1.refresh_from_db()
        self.board2.refresh_from_db()
        self.assertTrue(self.board1.is_archived)
        self.assertTrue(self.board2.is_archived)


class RestoreBoardsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.board1 = Board.objects.create(title='Board 1', user=self.user, is_archived=True)
        self.board2 = Board.objects.create(title='Board 2', user=self.user, is_archived=True)
        self.task1 = _make_task(self.user, board=self.board1, is_archived=True)

    def test_restore_boards_restores_all_archived_boards(self):
        restore_boards(self.user)
        self.board1.refresh_from_db()
        self.board2.refresh_from_db()
        self.assertFalse(self.board1.is_archived)
        self.assertFalse(self.board2.is_archived)

    def test_restore_boards_restores_specific_ids(self):
        restore_boards(self.user, ids=[self.board1.pk])
        self.board1.refresh_from_db()
        self.board2.refresh_from_db()
        self.assertFalse(self.board1.is_archived)
        self.assertTrue(self.board2.is_archived)

    def test_restore_boards_with_restore_tasks_true(self):
        restore_boards(self.user, restore_tasks=True)
        self.task1.refresh_from_db()
        self.assertFalse(self.task1.is_archived)

    def test_restore_boards_without_restore_tasks(self):
        restore_boards(self.user, restore_tasks=False)
        self.task1.refresh_from_db()
        self.assertTrue(self.task1.is_archived)

    def test_restore_boards_skips_non_archived(self):
        active_board = Board.objects.create(title='Active', user=self.user)
        restore_boards(self.user)
        active_board.refresh_from_db()
        self.assertFalse(active_board.is_archived)

    def test_restore_boards_does_not_restore_other_users_boards(self):
        other_user = User.objects.create_user(username='other', password='pass')
        other_board = Board.objects.create(title='Other', user=other_user, is_archived=True)
        restore_boards(self.user)
        other_board.refresh_from_db()
        self.assertTrue(other_board.is_archived)
