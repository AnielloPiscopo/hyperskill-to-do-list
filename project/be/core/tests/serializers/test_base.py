from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import serializers

from core.serializers import BaseModelSerializer


class BaseModelSerializerTest(TestCase):
    def test_is_subclass_of_model_serializer(self):
        self.assertTrue(issubclass(BaseModelSerializer, serializers.ModelSerializer))

    def test_read_only_fields_contains_id(self):
        self.assertIn('id', BaseModelSerializer.Meta.read_only_fields)

    def test_read_only_fields_contains_created_at(self):
        self.assertIn('created_at', BaseModelSerializer.Meta.read_only_fields)

    def test_read_only_fields_contains_updated_at(self):
        self.assertIn('updated_at', BaseModelSerializer.Meta.read_only_fields)

    def test_validate_strips_whitespace_from_string_fields(self):
        class DummySerializer(BaseModelSerializer):
            name = serializers.CharField()

            class Meta(BaseModelSerializer.Meta):
                model = User
                fields = ['name']

        serializer = DummySerializer()
        result = serializer.validate({'name': '  hello  '})
        self.assertEqual(result['name'], 'hello')

    def test_validate_does_not_strip_non_string_fields(self):
        class DummySerializer(BaseModelSerializer):
            age = serializers.IntegerField()

            class Meta(BaseModelSerializer.Meta):
                model = User
                fields = ['age']

        serializer = DummySerializer()
        result = serializer.validate({'age': 42})
        self.assertEqual(result['age'], 42)
