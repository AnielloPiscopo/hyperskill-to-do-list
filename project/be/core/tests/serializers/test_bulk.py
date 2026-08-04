import unittest

from core.serializers import BulkIdsSerializer


class BulkIdsSerializerTest(unittest.TestCase):

    def test_valid_with_ids(self):
        serializer = BulkIdsSerializer(data={'ids': [1, 2, 3]})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['ids'], [1, 2, 3])

    def test_valid_without_ids_field(self):
        serializer = BulkIdsSerializer(data={})
        self.assertTrue(serializer.is_valid())
        self.assertNotIn('ids', serializer.validated_data)

    def test_valid_with_empty_ids_list(self):
        serializer = BulkIdsSerializer(data={'ids': []})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['ids'], [])

    def test_invalid_with_non_integer_ids(self):
        serializer = BulkIdsSerializer(data={'ids': ['abc', 'def']})
        self.assertFalse(serializer.is_valid())
        self.assertIn('ids', serializer.errors)

    def test_invalid_with_ids_not_a_list(self):
        serializer = BulkIdsSerializer(data={'ids': 'not-a-list'})
        self.assertFalse(serializer.is_valid())
        self.assertIn('ids', serializer.errors)

    def test_invalid_with_mixed_valid_and_invalid_ids(self):
        serializer = BulkIdsSerializer(data={'ids': [1, 'abc', 3]})
        self.assertFalse(serializer.is_valid())
        self.assertIn('ids', serializer.errors)

    def test_ignores_unexpected_extra_fields(self):
        serializer = BulkIdsSerializer(data={'ids': [1, 2], 'unexpected_field': 'value'})
        self.assertTrue(serializer.is_valid())
        self.assertNotIn('unexpected_field', serializer.validated_data)