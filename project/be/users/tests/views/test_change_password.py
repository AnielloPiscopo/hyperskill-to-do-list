from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase


class ChangePasswordViewTest(APITestCase):
    client: APIClient

    def setUp(self):
        self.client = APIClient()
        self.url = '/auth/change-password/'
        self.user = User.objects.create_user(username='testuser', password='oldpass123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.valid_data = {
            'old_password': 'oldpass123',
            'new_password': 'newpass456',
            'confirm_new_password': 'newpass456',
        }

    # --- valid data ---

    def test_change_password_valid_returns_200(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password_valid_returns_detail(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Password changed successfully.')

    def test_change_password_updates_password(self):
        self.client.post(self.url, self.valid_data)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass456'))

    def test_change_password_deletes_token(self):
        self.client.post(self.url, self.valid_data)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    # --- wrong old password ---

    def test_change_password_wrong_old_password_returns_400(self):
        data = self.valid_data.copy()
        data['old_password'] = 'wrongpass'
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_wrong_old_password_returns_error(self):
        data = self.valid_data.copy()
        data['old_password'] = 'wrongpass'
        response = self.client.post(self.url, data)
        self.assertIn('old_password', response.data)
        self.assertEqual(response.data['old_password'], ['Wrong password.'])

    # --- invalid serializer data ---

    def test_change_password_missing_fields_returns_400(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- unauthenticated ---

    def test_change_password_unauthenticated_returns_401(self):
        self.client.credentials()
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
