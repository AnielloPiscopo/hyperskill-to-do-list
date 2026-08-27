from typing import cast

from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey
from django.test import TestCase

from board.models import Board, BoardSlugHistory
from core.models import BaseModel
from core.models.slugs import SluggedModel, SlugHistory


class BoardModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.board = Board.objects.create(
            title='My Board',
            description='Board description',
            color='#123456',
            user=self.user,
        )

    # --- inheritance ---

    def test_inherits_from_base_model(self):
        self.assertTrue(issubclass(Board, BaseModel))

    def test_inherits_from_slugged_model(self):
        self.assertTrue(issubclass(Board, SluggedModel))

    # --- field types ---

    def test_id_field_type(self):
        field = Board._meta.get_field('id')
        self.assertIsInstance(field, models.AutoField)

    def test_title_field_type(self):
        field = Board._meta.get_field('title')
        self.assertIsInstance(field, models.CharField)

    def test_description_field_type(self):
        field = Board._meta.get_field('description')
        self.assertIsInstance(field, models.TextField)

    def test_color_field_type(self):
        field = Board._meta.get_field('color')
        self.assertIsInstance(field, models.CharField)

    def test_user_field_type(self):
        field = Board._meta.get_field('user')
        self.assertIsInstance(field, models.ForeignKey)

    # --- field options ---

    def test_title_max_length(self):
        field = Board._meta.get_field('title')
        self.assertEqual(field.max_length, 100)

    def test_description_max_length(self):
        field = Board._meta.get_field('description')
        self.assertEqual(field.max_length, 2048)

    def test_description_blank(self):
        field = Board._meta.get_field('description')
        self.assertTrue(field.blank)

    def test_description_default(self):
        field = Board._meta.get_field('description')
        self.assertEqual(field.default, '')

    def test_color_max_length(self):
        field = Board._meta.get_field('color')
        self.assertEqual(field.max_length, 7)

    def test_color_blank(self):
        field = Board._meta.get_field('color')
        self.assertTrue(field.blank)

    def test_color_default(self):
        field = Board._meta.get_field('color')
        self.assertEqual(field.default, '#FFFFFF')

    def test_user_on_delete_cascade(self):
        field = cast(ForeignKey, Board._meta.get_field('user'))
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)

    def test_user_related_name(self):
        field = cast(ForeignKey, Board._meta.get_field('user'))
        self.assertEqual(field.remote_field.related_name, 'boards')

    # --- defaults ---

    def test_description_defaults_to_empty_string(self):
        board = Board.objects.create(title='Minimal', user=self.user)
        self.assertEqual(board.description, '')

    def test_color_defaults_to_white(self):
        board = Board.objects.create(title='Minimal', user=self.user)
        self.assertEqual(board.color, '#FFFFFF')

    def test_is_archived_defaults_to_false(self):
        board = Board.objects.create(title='Minimal', user=self.user)
        self.assertFalse(board.is_archived)

    # --- cascade delete ---

    def test_board_deleted_when_user_deleted(self):
        board_pk = self.board.pk
        self.user.delete()
        self.assertFalse(Board.objects.filter(pk=board_pk).exists())

    # --- str / repr ---

    def test_str_representation(self):
        self.assertEqual(str(self.board), f'[{self.user.username}] My Board')

    def test_repr_representation(self):
        expected = f"Board(id={self.board.id}, title='My Board', user='testuser')"
        self.assertEqual(repr(self.board), expected)

    # --- slug field ---

    def test_slug_field_type(self):
        field = Board._meta.get_field('slug')
        self.assertIsInstance(field, models.SlugField)

    def test_slug_max_length(self):
        field = Board._meta.get_field('slug')
        self.assertEqual(field.max_length, 100)

    def test_slug_blank(self):
        field = Board._meta.get_field('slug')
        self.assertTrue(field.blank)

    def test_unique_together_user_slug(self):
        self.assertIn(('user', 'slug'), Board._meta.unique_together)

    # --- slug behaviour ---

    def test_slug_auto_generated_on_create(self):
        self.assertNotEqual(self.board.slug, '')

    def test_slug_derived_from_title(self):
        self.assertEqual(self.board.slug, 'my-board')

    def test_slug_regenerated_on_title_change(self):
        self.board.title = 'New Title'
        self.board.save()
        self.board.refresh_from_db()
        self.assertEqual(self.board.slug, 'new-title')

    def test_old_slug_saved_to_slug_history_on_title_change(self):
        old_slug = self.board.slug
        self.board.title = 'New Title'
        self.board.save()
        self.assertTrue(SlugHistory.objects.filter(slug=old_slug).exists())

    def test_no_slug_history_when_title_unchanged(self):
        self.board.description = 'New description'
        self.board.save()
        self.assertFalse(SlugHistory.objects.exists())

    def test_duplicate_title_gets_numbered_slug(self):
        board2 = Board.objects.create(title='My Board', user=self.user)
        self.assertEqual(board2.slug, 'my-board-2')

    def test_slug_scoped_per_user(self):
        other_user = User.objects.create_user(username='other', password='pass123')
        board2 = Board.objects.create(title='My Board', user=other_user)
        self.assertEqual(board2.slug, 'my-board')


class BoardSlugHistoryTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.board = Board.objects.create(title='My Board', user=self.user)

    # --- field types ---

    def test_board_field_type(self):
        field = BoardSlugHistory._meta.get_field('board')
        self.assertIsInstance(field, models.ForeignKey)

    def test_board_on_delete_cascade(self):
        field = cast(ForeignKey, BoardSlugHistory._meta.get_field('board'))
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)

    def test_board_related_name(self):
        field = cast(ForeignKey, BoardSlugHistory._meta.get_field('board'))
        self.assertEqual(field.remote_field.related_name, 'old_slugs')

    def test_slug_field_type(self):
        field = BoardSlugHistory._meta.get_field('slug')
        self.assertIsInstance(field, models.SlugField)

    def test_created_at_field_type(self):
        field = BoardSlugHistory._meta.get_field('created_at')
        self.assertIsInstance(field, models.DateTimeField)

    def test_created_at_auto_now_add(self):
        field = BoardSlugHistory._meta.get_field('created_at')
        self.assertTrue(field.auto_now_add)

    # --- meta ---

    def test_unique_together(self):
        self.assertIn(('board', 'slug'), BoardSlugHistory._meta.unique_together)

    # --- behaviour ---

    def test_deleted_when_board_deleted(self):
        history = BoardSlugHistory.objects.create(board=self.board, slug='old-slug')
        self.board.delete()
        self.assertFalse(BoardSlugHistory.objects.filter(pk=history.pk).exists())
