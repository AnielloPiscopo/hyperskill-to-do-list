from django.contrib.auth.models import User
from django.test import TestCase

from users.serializers import RegisterSerializer


class RegisterSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'securepassword123',
            'confirm_password': 'securepassword123',
        }

    def test_valid_data_is_valid(self):
        serializer = RegisterSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_passwords_mismatch_is_invalid(self):
        data = self.valid_data.copy()
        data['confirm_password'] = 'differentpassword'
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)

    def test_create_returns_user_instance(self):
        serializer = RegisterSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertIsInstance(user, User)

    def test_create_sets_correct_username_and_email(self):
        serializer = RegisterSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'newuser@example.com')

    def test_password_is_hashed(self):
        serializer = RegisterSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertTrue(user.check_password('securepassword123'))

    def test_missing_username_is_invalid(self):
        data = self.valid_data.copy()
        data.pop('username')
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

    def test_missing_password_is_invalid(self):
        data = self.valid_data.copy()
        data.pop('password')
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_email_is_required(self):
        data = self.valid_data.copy()
        data.pop('email')
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_email_is_normalized_to_lowercase(self):
        data = self.valid_data.copy()
        data['email'] = 'NewUser@Example.COM'
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.email, 'newuser@example.com')

    def test_duplicate_email_is_invalid(self):
        serializer = RegisterSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        data = self.valid_data.copy()
        data['username'] = 'anotheruser'
        serializer2 = RegisterSerializer(data=data)
        self.assertFalse(serializer2.is_valid())
        self.assertIn('email', serializer2.errors)

    def test_duplicate_email_case_insensitive_is_invalid(self):
        serializer = RegisterSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        data = self.valid_data.copy()
        data['username'] = 'anotheruser'
        data['email'] = self.valid_data['email'].upper()
        serializer2 = RegisterSerializer(data=data)
        self.assertFalse(serializer2.is_valid())
        self.assertIn('email', serializer2.errors)

    def test_password_and_confirm_password_are_write_only(self):
        serializer = RegisterSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        output = RegisterSerializer(user)
        self.assertNotIn('password', output.data)
        self.assertNotIn('confirm_password', output.data)
