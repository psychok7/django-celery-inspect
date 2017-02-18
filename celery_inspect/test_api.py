# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class CeleryInspectAPITests(TestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.user = get_user_model().objects.create_user(
            name='test', email='test@example.com', password='safe#passw0rd!'
        )
        self.token = Token.objects.get(user=self.user)

    def test_200_celery_inspect_ping(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(reverse('celery_inspect:ping'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_200_celery_inspect_registered(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(reverse('celery_inspect:registered'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_200_celery_inspect_active(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(reverse('celery_inspect:active'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_200_celery_inspect_scheduled(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(reverse('celery_inspect:scheduled'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
