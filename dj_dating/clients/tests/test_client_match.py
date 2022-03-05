from clients.models import User, Like
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class ClientMatchAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create_user(
            email='test@mail.ru',
            first_name='test1',
            last_name='testuser1',
            password='123456test',
            gender='female',
        )
        cls.user_2 = cls.user_1 = User.objects.create_user(
            email='test2@mail.ru',
            first_name='test1',
            last_name='testuser1',
            password='123456test',
            gender='female',
        )

    def test_liked_by_the_client(self):
        self.client.force_authenticate(user=self.user_1)
        response = self.client.post(reverse('client_match', kwargs={'pk': self.user_2.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user_1.id, Like.objects.get(id=1).user_id)

    def test_clients_likes_matched(self):
        self.client.force_authenticate(user=self.user_1)
        response = self.client.post(reverse('client_match', kwargs={'pk': self.user_2.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.force_authenticate(user=self.user_2)
        response = self.client.post(reverse('client_match', kwargs={'pk': self.user_1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        from django.core.mail import outbox
        self.assertEqual(len(outbox), 4)
        self.assertIn(self.user_2.email, outbox[0].to)
