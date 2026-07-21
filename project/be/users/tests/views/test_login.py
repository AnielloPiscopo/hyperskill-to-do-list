from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from django.conf import settings
from django.test import override_settings


class LoginViewTest(APITestCase):
    client: APIClient

    def setUp(self):
        self.client = APIClient()
        self.url = '/auth/login/'
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    # --- valid credentials ---

    def test_login_valid_credentials_returns_200(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'testpass123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_returns_token_key(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'testpass123'})
        self.assertIn('token', response.data)

    def test_login_creates_token_in_db(self):
        self.client.post(self.url, {'username': 'testuser', 'password': 'testpass123'})
        self.assertTrue(Token.objects.filter(user=self.user).exists())

    def test_login_reuses_existing_token(self):
        existing_token = Token.objects.create(user=self.user)
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'testpass123'})
        self.assertEqual(response.data['token'], existing_token.key)

    # --- invalid credentials ---

    def test_login_wrong_password_returns_400(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_unknown_username_returns_400(self):
        response = self.client.post(self.url, {'username': 'nouser', 'password': 'testpass123'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_invalid_credentials_returns_detail(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'wrong'})
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Invalid credentials.')

    @override_settings(REST_FRAMEWORK={
        **settings.REST_FRAMEWORK,
        'DEFAULT_THROTTLE_RATES': {'login': '2/minute'}
    })
    def test_login_rate_limit_returns_429(self):
        for _ in range(2):
            self.client.post(self.url, {'username': 'testuser', 'password': 'testpass123'})
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'testpass123'})
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
