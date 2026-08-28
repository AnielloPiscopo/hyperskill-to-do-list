import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from board.models import Board
from task.models import Task
from task.services.bulk import move_tasks, delete_tasks


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


class MoveTasksTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.other_user = User.objects.create_user(username='other', password='pass')
        self.board = Board.objects.create(title='Board', user=self.user)
        self.task1 = _make_task(self.user)
        self.task2 = _make_task(self.user)

    def test_moves_task_to_board(self):
        move_tasks(self.user, [self.task1.pk], self.board)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.board, self.board)

    def test_moves_multiple_tasks_to_board(self):
        move_tasks(self.user, [self.task1.pk, self.task2.pk], self.board)
        self.task1.refresh_from_db()
        self.task2.refresh_from_db()
        self.assertEqual(self.task1.board, self.board)
        self.assertEqual(self.task2.board, self.board)

    def test_clears_board_when_board_is_none(self):
        self.task1.board = self.board
        self.task1.save()
        move_tasks(self.user, [self.task1.pk], None)
        self.task1.refresh_from_db()
        self.assertIsNone(self.task1.board)

    def test_does_not_affect_other_users_tasks(self):
        other_task = _make_task(self.other_user)
        move_tasks(self.user, [other_task.pk], self.board)
        other_task.refresh_from_db()
        self.assertIsNone(other_task.board)

    def test_only_moves_tasks_with_matching_ids(self):
        move_tasks(self.user, [self.task1.pk], self.board)
        self.task2.refresh_from_db()
        self.assertIsNone(self.task2.board)

    def test_empty_ids_list_moves_nothing(self):
        move_tasks(self.user, [], self.board)
        self.task1.refresh_from_db()
        self.assertIsNone(self.task1.board)


class DeleteTasksTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.other_user = User.objects.create_user(username='other', password='pass')
        self.task1 = _make_task(self.user, is_archived=True)
        self.task2 = _make_task(self.user, is_archived=True)
        self.active_task = _make_task(self.user)

    def test_deletes_all_archived_tasks_when_ids_is_none(self):
        delete_tasks(self.user, ids=None)
        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())
        self.assertFalse(Task.objects.filter(pk=self.task2.pk).exists())

    def test_deletes_specific_tasks_when_ids_provided(self):
        delete_tasks(self.user, ids=[self.task1.pk])
        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())
        self.assertTrue(Task.objects.filter(pk=self.task2.pk).exists())

    def test_empty_ids_list_deletes_all_archived(self):
        delete_tasks(self.user, ids=[])
        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())
        self.assertFalse(Task.objects.filter(pk=self.task2.pk).exists())

    def test_does_not_delete_active_tasks(self):
        delete_tasks(self.user, ids=None)
        self.assertTrue(Task.objects.filter(pk=self.active_task.pk).exists())

    def test_does_not_delete_other_users_tasks(self):
        other_task = _make_task(self.other_user, is_archived=True)
        delete_tasks(self.user, ids=None)
        self.assertTrue(Task.objects.filter(pk=other_task.pk).exists())
