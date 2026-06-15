import datetime
from unittest.mock import MagicMock

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from todo.models import Todo
from todo.permissions import IsAuthorOrReadOnly


class IsAuthorOrReadOnlyTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.permission = IsAuthorOrReadOnly()
        self.view = MagicMock()
        self.author = User.objects.create_user(
            username='author',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='other',
            password='testpass123'
        )
        self.todo = Todo.objects.create(
            task='Test task',
            description='Test description',
            goal_set_date=datetime.date(2024, 1, 1),
            set_to_complete=datetime.date(2024, 1, 31),
            todo_of=self.author
        )

    def _make_request(self, method: str, user: User) -> Request:
        raw = getattr(self.factory, method)('/')
        raw.user = user
        return Request(raw)

    def test_get_allowed_for_non_author(self):
        request = self._make_request('get', self.other_user)
        self.assertTrue(self.permission.has_object_permission(request, self.view, self.todo))

    def test_head_allowed_for_non_author(self):
        request = self._make_request('head', self.other_user)
        self.assertTrue(self.permission.has_object_permission(request, self.view, self.todo))

    def test_options_allowed_for_non_author(self):
        request = self._make_request('options', self.other_user)
        self.assertTrue(self.permission.has_object_permission(request, self.view, self.todo))

    def test_put_allowed_for_author(self):
        request = self._make_request('put', self.author)
        self.assertTrue(self.permission.has_object_permission(request, self.view, self.todo))

    def test_patch_allowed_for_author(self):
        request = self._make_request('patch', self.author)
        self.assertTrue(self.permission.has_object_permission(request, self.view, self.todo))

    def test_delete_allowed_for_author(self):
        request = self._make_request('delete', self.author)
        self.assertTrue(self.permission.has_object_permission(request, self.view, self.todo))

    def test_put_denied_for_non_author(self):
        request = self._make_request('put', self.other_user)
        self.assertFalse(self.permission.has_object_permission(request, self.view, self.todo))

    def test_patch_denied_for_non_author(self):
        request = self._make_request('patch', self.other_user)
        self.assertFalse(self.permission.has_object_permission(request, self.view, self.todo))

    def test_delete_denied_for_non_author(self):
        request = self._make_request('delete', self.other_user)
        self.assertFalse(self.permission.has_object_permission(request, self.view, self.todo))
