from django.contrib.auth.models import User
from django.test import TestCase

from board.models import Board
from board.serializers import BoardSerializer
from core.serializers import BaseModelSerializer


class BoardSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.board = Board.objects.create(
            title='Test Board',
            description='A description',
            color='#FF0000',
            user=self.user,
        )

    # --- meta ---

    def test_meta_model_is_board(self):
        self.assertIs(BoardSerializer.Meta.model, Board)

    def test_is_subclass_of_base_model_serializer(self):
        self.assertTrue(issubclass(BoardSerializer, BaseModelSerializer))

    # --- excluded fields ---

    def test_user_field_excluded(self):
        serializer = BoardSerializer(self.board)
        self.assertNotIn('user', serializer.data)

    def test_is_archived_field_excluded(self):
        serializer = BoardSerializer(self.board)
        self.assertNotIn('is_archived', serializer.data)

    # --- read-only fields (inherited from BaseModelSerializer) ---

    def test_id_is_read_only(self):
        serializer = BoardSerializer(self.board)
        self.assertTrue(serializer.fields['id'].read_only)

    def test_created_at_is_read_only(self):
        serializer = BoardSerializer(self.board)
        self.assertTrue(serializer.fields['created_at'].read_only)

    def test_updated_at_is_read_only(self):
        serializer = BoardSerializer(self.board)
        self.assertTrue(serializer.fields['updated_at'].read_only)

    # --- serialization ---

    def test_serialization_contains_expected_fields(self):
        serializer = BoardSerializer(self.board)
        for field in ('id', 'title', 'description', 'color', 'created_at', 'updated_at'):
            self.assertIn(field, serializer.data)

    def test_serialization_title_value(self):
        serializer = BoardSerializer(self.board)
        self.assertEqual(serializer.data['title'], 'Test Board')

    def test_serialization_description_value(self):
        serializer = BoardSerializer(self.board)
        self.assertEqual(serializer.data['description'], 'A description')

    def test_serialization_color_value(self):
        serializer = BoardSerializer(self.board)
        self.assertEqual(serializer.data['color'], '#FF0000')

    # --- deserialization / validation ---

    def test_valid_data_is_valid(self):
        data = {'title': 'New Board', 'description': 'Desc', 'color': '#000000'}
        serializer = BoardSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_missing_title_is_invalid(self):
        serializer = BoardSerializer(data={'description': 'No title'})
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_description_optional(self):
        serializer = BoardSerializer(data={'title': 'No description board'})
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_color_optional(self):
        serializer = BoardSerializer(data={'title': 'No color board'})
        self.assertTrue(serializer.is_valid(), serializer.errors)
