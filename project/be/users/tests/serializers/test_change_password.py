from django.test import TestCase
from rest_framework import serializers

from users.serializers import ChangePasswordSerializer


class ChangePasswordSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'old_password': 'oldpass123',
            'new_password': 'newpass456',
            'confirm_new_password': 'newpass456',
        }

    def test_valid_data_is_valid(self):
        serializer = ChangePasswordSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_missing_old_password_is_invalid(self):
        data = self.valid_data.copy()
        data.pop('old_password')
        serializer = ChangePasswordSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('old_password', serializer.errors)

    def test_missing_new_password_is_invalid(self):
        data = self.valid_data.copy()
        data.pop('new_password')
        serializer = ChangePasswordSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('new_password', serializer.errors)

    def test_missing_confirm_new_password_is_invalid(self):
        data = self.valid_data.copy()
        data.pop('confirm_new_password')
        serializer = ChangePasswordSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('confirm_new_password', serializer.errors)

    def test_fields_are_write_only(self):
        serializer = ChangePasswordSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertNotIn('old_password', serializer.data)
        self.assertNotIn('new_password', serializer.data)
        self.assertNotIn('confirm_new_password', serializer.data)

    def test_mismatching_passwords_is_invalid(self):
        data = self.valid_data.copy()
        data['confirm_new_password'] = 'differentpass'
        serializer = ChangePasswordSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)

    def test_mismatching_passwords_returns_error_message(self):
        data = self.valid_data.copy()
        data['confirm_new_password'] = 'differentpass'
        serializer = ChangePasswordSerializer(data=data)
        serializer.is_valid()
        self.assertIn('Passwords must match.', str(serializer.errors['non_field_errors']))
