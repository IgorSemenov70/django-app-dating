from clients.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class ClientListAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create_user(
            email='test@mail.ru',
            first_name='test1',
            last_name='testuser1',
            password='123456test',
            gender='female',
            longitude=53.8,
            latitude=54.1,
        )
        cls.user_2 = cls.user_1 = User.objects.create_user(
            email='test2@mail.ru',
            first_name='test1',
            last_name='testuser1',
            password='123456test',
            gender='female',
            longitude=53.9,
            latitude=54.1,
        )

    def test_list_of_clients_is_displayed(self):
        self.client.force_authenticate(user=self.user_1)
        response = self.client.get(reverse('clients_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
