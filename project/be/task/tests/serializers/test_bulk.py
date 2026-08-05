from unittest.mock import Mock

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import serializers

from board.models import Board
from task.serializers.bulk import TaskMoveSerializer


class TaskMoveSerializerValidateBoardTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.other_user = User.objects.create_user(username='other', password='pass')
        self.board = Board.objects.create(title='Board', user=self.user)

    def _request(self, user=None):
        request = Mock()
        request.user = user or self.user
        return request

    # --- validate_board ---

    def test_validate_board_returns_none_when_board_is_none(self):
        serializer = TaskMoveSerializer()
        result = serializer.validate_board(None)
        self.assertIsNone(result)

    def test_validate_board_returns_board_when_owner_matches(self):
        serializer = TaskMoveSerializer(context={'request': self._request()})
        result = serializer.validate_board(self.board)
        self.assertEqual(result, self.board)

    def test_validate_board_raises_when_board_belongs_to_another_user(self):
        other_board = Board.objects.create(title='Other Board', user=self.other_user)
        serializer = TaskMoveSerializer(context={'request': self._request()})
        with self.assertRaises(serializers.ValidationError):
            serializer.validate_board(other_board)

    # --- is_valid integration ---

    def test_valid_board_id_is_valid(self):
        serializer = TaskMoveSerializer(
            data={'ids': [], 'board': self.board.pk},
            context={'request': self._request()},
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_null_board_is_valid(self):
        serializer = TaskMoveSerializer(
            data={'ids': [], 'board': None},
            context={'request': self._request()},
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_nonexistent_board_id_is_invalid(self):
        serializer = TaskMoveSerializer(
            data={'ids': [], 'board': 9999},
            context={'request': self._request()},
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('board', serializer.errors)

    def test_board_not_owned_is_invalid(self):
        other_board = Board.objects.create(title='Other Board', user=self.other_user)
        serializer = TaskMoveSerializer(
            data={'ids': [], 'board': other_board.pk},
            context={'request': self._request()},
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('board', serializer.errors)
