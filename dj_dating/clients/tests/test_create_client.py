from clients.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class CreateClientAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = {
            'email': 'test@mail.ru',
            'first_name': 'test1',
            'last_name': 'testuser1',
            'password': '123456test',
            'gender': 'female',
        }

    def test_create_client(self):
        response = self.client.post(reverse('create_client'), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@mail.ru')

    def test_create_client_fail(self):
        self.data = {
            'email': 'test@mail.ru',
            'first_name': 'test1',
            'last_name': 'testuser1',
            'password': '123456',
            'gender': 'female',
        }
        response = self.client.post(reverse('create_client'), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
