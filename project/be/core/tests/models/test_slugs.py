from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.test import TestCase

from core.models import BaseModel
from core.models.slugs import SluggedModel, SlugHistory


class SluggedModelTest(TestCase):

    # --- meta ---

    def test_is_abstract(self):
        self.assertTrue(SluggedModel._meta.abstract)

    def test_inherits_from_base_model(self):
        self.assertTrue(issubclass(SluggedModel, BaseModel))

    # --- slug field ---

    def test_slug_field_type(self):
        field = SluggedModel._meta.get_field('slug')
        self.assertIsInstance(field, models.SlugField)

    def test_slug_max_length(self):
        field = SluggedModel._meta.get_field('slug')
        self.assertEqual(field.max_length, 100)

    def test_slug_blank(self):
        field = SluggedModel._meta.get_field('slug')
        self.assertTrue(field.blank)


class SlugHistoryTest(TestCase):

    # --- meta ---

    def test_app_label(self):
        self.assertEqual(SlugHistory._meta.app_label, 'core')

    def test_unique_together(self):
        self.assertIn(('content_type', 'object_id', 'slug'), SlugHistory._meta.unique_together)

    # --- field types ---

    def test_content_type_field_type(self):
        field = SlugHistory._meta.get_field('content_type')
        self.assertIsInstance(field, models.ForeignKey)

    def test_content_type_fk_target(self):
        field = SlugHistory._meta.get_field('content_type')
        self.assertIs(field.related_model, ContentType)

    def test_object_id_field_type(self):
        field = SlugHistory._meta.get_field('object_id')
        self.assertIsInstance(field, models.PositiveIntegerField)

    def test_slug_field_type(self):
        field = SlugHistory._meta.get_field('slug')
        self.assertIsInstance(field, models.SlugField)

    def test_created_at_field_type(self):
        field = SlugHistory._meta.get_field('created_at')
        self.assertIsInstance(field, models.DateTimeField)

    def test_created_at_auto_now_add(self):
        field = SlugHistory._meta.get_field('created_at')
        self.assertTrue(field.auto_now_add)
