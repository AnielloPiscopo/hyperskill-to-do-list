from django.test import TestCase
from rest_framework import generics

from core.mixins import UserScopedQuerysetMixin
from task.models import Task


class DummyView(UserScopedQuerysetMixin, generics.GenericAPIView):
    queryset = Task.objects.all()


class UserScopedQuerysetMixinTest(TestCase):

    def test_returns_empty_queryset_during_schema_generation(self):
        view = DummyView()
        view.swagger_fake_view = True
        self.assertEqual(view.get_queryset().count(), 0)

    def test_raises_not_implemented_without_get_user_queryset_override(self):
        view = DummyView()
        view.swagger_fake_view = False
        with self.assertRaises(NotImplementedError):
            view.get_queryset()