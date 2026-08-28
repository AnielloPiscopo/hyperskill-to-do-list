import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from board.models import Board
from board.serializers import BoardSerializer, BoardDetailSerializer
from core.serializers import BaseModelSerializer, SlugModelSerializer
from task.models import Task


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

    def test_is_subclass_of_slug_model_serializer(self):
        self.assertTrue(issubclass(BoardSerializer, SlugModelSerializer))

    # --- excluded fields ---

    def test_user_field_excluded(self):
        serializer = BoardSerializer(self.board)
        self.assertNotIn('user', serializer.data)

    # --- read-only fields (inherited from BaseModelSerializer / SlugModelSerializer) ---

    def test_id_is_read_only(self):
        serializer = BoardSerializer(self.board)
        self.assertTrue(serializer.fields['id'].read_only)

    def test_created_at_is_read_only(self):
        serializer = BoardSerializer(self.board)
        self.assertTrue(serializer.fields['created_at'].read_only)

    def test_updated_at_is_read_only(self):
        serializer = BoardSerializer(self.board)
        self.assertTrue(serializer.fields['updated_at'].read_only)

    def test_slug_is_read_only(self):
        serializer = BoardSerializer(self.board)
        self.assertTrue(serializer.fields['slug'].read_only)

    # --- slug serialization ---

    def test_slug_value_matches_board_slug(self):
        serializer = BoardSerializer(self.board)
        self.assertEqual(serializer.data['slug'], self.board.slug)

    # --- serialization ---

    def test_serialization_contains_expected_fields(self):
        serializer = BoardSerializer(self.board)
        for field in ('id', 'title', 'description', 'color', 'slug', 'created_at', 'updated_at'):
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

    # --- validate_color ---

    def test_invalid_hex_color_is_invalid(self):
        serializer = BoardSerializer(data={'title': 'Board', 'color': 'not-a-color'})
        self.assertFalse(serializer.is_valid())
        self.assertIn('color', serializer.errors)

    def test_hex_color_without_hash_is_invalid(self):
        serializer = BoardSerializer(data={'title': 'Board', 'color': 'FF0000'})
        self.assertFalse(serializer.is_valid())
        self.assertIn('color', serializer.errors)

    def test_lowercase_color_is_uppercased(self):
        serializer = BoardSerializer(data={'title': 'Board', 'color': '#ff0000'})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data['color'], '#FF0000')


class BoardDetailSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.board = Board.objects.create(
            title='Test Board',
            description='A description',
            color='#FF0000',
            user=self.user,
        )
        self.active_task = Task.objects.create(
            title='Active Task',
            description='Desc',
            goal_set_date=datetime.date(2024, 1, 1),
            set_to_complete=datetime.date(2024, 1, 31),
            user=self.user,
            board=self.board,
            is_archived=False,
        )
        self.archived_task = Task.objects.create(
            title='Archived Task',
            description='Desc',
            goal_set_date=datetime.date(2024, 1, 1),
            set_to_complete=datetime.date(2024, 1, 31),
            user=self.user,
            board=self.board,
            is_archived=True,
        )

    # --- inheritance ---

    def test_is_subclass_of_board_serializer(self):
        self.assertTrue(issubclass(BoardDetailSerializer, BoardSerializer))

    # --- tasks field ---

    def test_contains_tasks_field(self):
        serializer = BoardDetailSerializer(self.board)
        self.assertIn('tasks', serializer.data)

    def test_tasks_field_contains_active_tasks(self):
        serializer = BoardDetailSerializer(self.board)
        task_titles = [t['title'] for t in serializer.data['tasks']]
        self.assertIn('Active Task', task_titles)

    def test_tasks_field_excludes_archived_tasks(self):
        serializer = BoardDetailSerializer(self.board)
        task_titles = [t['title'] for t in serializer.data['tasks']]
        self.assertNotIn('Archived Task', task_titles)

    def test_tasks_field_is_empty_when_no_active_tasks(self):
        self.active_task.is_archived = True
        self.active_task.save()
        serializer = BoardDetailSerializer(self.board)
        self.assertEqual(len(serializer.data['tasks']), 0)

    # --- inherited fields ---

    def test_user_field_excluded(self):
        serializer = BoardDetailSerializer(self.board)
        self.assertNotIn('user', serializer.data)
