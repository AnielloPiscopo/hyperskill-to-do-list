from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase


class InfoViewTest(APITestCase):
    client: APIClient

    def setUp(self):
        self.client = APIClient()
        self.url = '/auth/about/'
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_info_authenticated_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_info_returns_username(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['username'], 'testuser')

    def test_info_returns_email(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_info_returns_id(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['id'], self.user.id)

    def test_info_unauthenticated_returns_401(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
