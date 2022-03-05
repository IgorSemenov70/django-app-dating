from clients.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class LoginClientAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='test@mail.ru',
            first_name='test1',
            last_name='testuser1',
            password='123456test',
            gender='female',
        )

        cls.token = Token.objects.get(user__email='test@mail.ru')

    def test_client_login(self):
        self.data = {
            'email': 'test@mail.ru',
            'password': '123456test',
            'token': f'{self.token}',
        }
        response = self.client.post(reverse('client_login'), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_login_fail(self):
        self.data = {
            'email': 'test@mail.ru',
            'password': '123456',
            'token': f'{self.token}',
        }
        response = self.client.post(reverse('client_login'), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
