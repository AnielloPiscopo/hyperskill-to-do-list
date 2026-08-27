from django.test import TestCase

from core.serializers import BaseModelSerializer, SlugModelSerializer


class SlugModelSerializerTest(TestCase):

    # --- inheritance ---

    def test_is_subclass_of_base_model_serializer(self):
        self.assertTrue(issubclass(SlugModelSerializer, BaseModelSerializer))

    # --- read-only fields ---

    def test_read_only_fields_contains_slug(self):
        self.assertIn('slug', SlugModelSerializer.Meta.read_only_fields)

    def test_read_only_fields_contains_id(self):
        self.assertIn('id', SlugModelSerializer.Meta.read_only_fields)

    def test_read_only_fields_contains_created_at(self):
        self.assertIn('created_at', SlugModelSerializer.Meta.read_only_fields)

    def test_read_only_fields_contains_updated_at(self):
        self.assertIn('updated_at', SlugModelSerializer.Meta.read_only_fields)
