from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase


class LogoutViewTest(APITestCase):
    client: APIClient

    def setUp(self):
        self.client = APIClient()
        self.url = '/auth/logout/'
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_logout_authenticated_returns_200(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_returns_detail_message(self):
        response = self.client.post(self.url)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Logged out successfully.')

    def test_logout_deletes_token(self):
        self.client.post(self.url)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_logout_unauthenticated_returns_401(self):
        self.client.credentials()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
