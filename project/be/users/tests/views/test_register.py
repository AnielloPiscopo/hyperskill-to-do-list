from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.core.cache import cache


class RegisterViewTest(APITestCase):
    client: APIClient

    def setUp(self):
        self.client = APIClient()
        self.url = '/auth/register/'
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

    def test_register_rate_limit_returns_429(self):
        from core.throttling import LoginRateThrottle
        LoginRateThrottle.THROTTLE_RATES = {'login': '2/minute'}
        cache.clear()
        try:
            for _ in range(2):
                self.client.post(self.url, {
                    'username': f'user{_}',
                    'email': f'user{_}@example.com',
                    'password': 'securepassword123',
                    'confirm_password': 'securepassword123',
                })
            response = self.client.post(self.url, {
                'username': 'user3',
                'email': 'user3@example.com',
                'password': 'securepassword123',
                'confirm_password': 'securepassword123',
            })
            self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        finally:
            del LoginRateThrottle.THROTTLE_RATES
            cache.clear()
