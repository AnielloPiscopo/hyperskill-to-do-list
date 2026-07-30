from django.contrib.auth.models import User
from django.test import TestCase

from users.serializers import InfoSerializer


class InfoSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
        )

    def test_serializer_contains_expected_fields(self):
        serializer = InfoSerializer(self.user)
        self.assertSetEqual(set(serializer.data.keys()), {'id', 'username', 'email'})

    def test_serializer_returns_correct_username(self):
        serializer = InfoSerializer(self.user)
        self.assertEqual(serializer.data['username'], 'testuser')

    def test_serializer_returns_correct_email(self):
        serializer = InfoSerializer(self.user)
        self.assertEqual(serializer.data['email'], 'test@example.com')

    def test_serializer_returns_correct_id(self):
        serializer = InfoSerializer(self.user)
        self.assertEqual(serializer.data['id'], self.user.id)
