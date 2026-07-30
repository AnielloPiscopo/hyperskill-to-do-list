from typing import cast

from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey
from django.test import TestCase

from board.models import Board
from core.models import BaseModel


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
