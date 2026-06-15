from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class RegisterViewTest(APITestCase):
    client: APIClient

    def setUp(self):
        self.client = APIClient()
        self.url = '/register/'
        self.valid_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'securepassword123',
            'confirm_password': 'securepassword123',
        }

    def test_register_valid_user_returns_201(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_creates_user_in_db(self):
        self.client.post(self.url, self.valid_data)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, 'newuser')

    def test_register_passwords_mismatch_returns_400(self):
        data = self.valid_data.copy()
        data['confirm_password'] = 'wrongpassword'
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_missing_username_returns_400(self):
        data = self.valid_data.copy()
        data.pop('username')
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_username_returns_400(self):
        User.objects.create_user(username='newuser', password='testpass123')
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_without_email_returns_201(self):
        data = self.valid_data.copy()
        data.pop('email')
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_response_contains_username_and_email(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)

    def test_register_response_does_not_expose_password(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertNotIn('password', response.data)
        self.assertNotIn('confirm_password', response.data)
