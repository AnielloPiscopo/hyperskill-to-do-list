import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from task.models import Task
from task.services.soft_delete import archive_task, restore_task, archive_tasks, restore_tasks


def _make_task(user, is_archived=False):
    return Task.objects.create(
        title='Task',
        description='Desc',
        goal_set_date=datetime.date(2024, 1, 1),
        set_to_complete=datetime.date(2024, 1, 31),
        user=user,
        is_archived=is_archived,
    )


class ArchiveTaskTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.task = _make_task(self.user)

    def test_archive_task_sets_is_archived_true(self):
        archive_task(self.task)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_archived)


class RestoreTaskTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.task = _make_task(self.user, is_archived=True)

    def test_restore_task_sets_is_archived_false(self):
        restore_task(self.task)
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_archived)


class ArchiveTasksTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.task1 = _make_task(self.user)
        self.task2 = _make_task(self.user)

    def test_archive_tasks_archives_all_user_tasks(self):
        archive_tasks(self.user)
        self.task1.refresh_from_db()
        self.task2.refresh_from_db()
        self.assertTrue(self.task1.is_archived)
        self.assertTrue(self.task2.is_archived)

    def test_archive_tasks_archives_specific_ids(self):
        archive_tasks(self.user, ids=[self.task1.pk])
        self.task1.refresh_from_db()
        self.task2.refresh_from_db()
        self.assertTrue(self.task1.is_archived)
        self.assertFalse(self.task2.is_archived)

    def test_archive_tasks_skips_already_archived(self):
        self.task1.is_archived = True
        self.task1.save()
        archive_tasks(self.user)
        self.task2.refresh_from_db()
        self.assertTrue(self.task2.is_archived)
        self.assertEqual(Task.objects.filter(is_archived=True).count(), 2)

    def test_archive_tasks_does_not_affect_other_users(self):
        other_user = User.objects.create_user(username='other', password='pass')
        other_task = _make_task(other_user)
        archive_tasks(self.user)
        other_task.refresh_from_db()
        self.assertFalse(other_task.is_archived)

    def test_archive_tasks_with_none_ids_archives_all(self):
        archive_tasks(self.user, ids=None)
        self.task1.refresh_from_db()
        self.task2.refresh_from_db()
        self.assertTrue(self.task1.is_archived)
        self.assertTrue(self.task2.is_archived)


class RestoreTasksTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.task1 = _make_task(self.user, is_archived=True)
        self.task2 = _make_task(self.user, is_archived=True)

    def test_restore_tasks_restores_all_archived(self):
        restore_tasks(self.user)
        self.task1.refresh_from_db()
        self.task2.refresh_from_db()
        self.assertFalse(self.task1.is_archived)
        self.assertFalse(self.task2.is_archived)

    def test_restore_tasks_restores_specific_ids(self):
        restore_tasks(self.user, ids=[self.task1.pk])
        self.task1.refresh_from_db()
        self.task2.refresh_from_db()
        self.assertFalse(self.task1.is_archived)
        self.assertTrue(self.task2.is_archived)

    def test_restore_tasks_skips_active_tasks(self):
        active_task = _make_task(self.user, is_archived=False)
        restore_tasks(self.user)
        active_task.refresh_from_db()
        self.assertFalse(active_task.is_archived)

    def test_restore_tasks_does_not_affect_other_users(self):
        other_user = User.objects.create_user(username='other', password='pass')
        other_task = _make_task(other_user, is_archived=True)
        restore_tasks(self.user)
        other_task.refresh_from_db()
        self.assertTrue(other_task.is_archived)

    def test_restore_tasks_with_none_ids_restores_all(self):
        restore_tasks(self.user, ids=None)
        self.task1.refresh_from_db()
        self.task2.refresh_from_db()
        self.assertFalse(self.task1.is_archived)
        self.assertFalse(self.task2.is_archived)
