# -*- coding: utf-8 -*-

from django.conf import settings

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

# TODO: Find a way to start workers so we can improve testing


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

    def test_200_celery_inspect_active(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(reverse('celery_inspect:active'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_404_celery_inspect_active_status(self):
        if "djcelery" in settings.INSTALLED_APPS:
            from djcelery.models import WorkerState
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
            WorkerState.objects.create(hostname='worker1@localhot:8000')
            response = self.client.get(reverse('celery_inspect:active_status'))
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_501_celery_inspect_active_status(self):
        if "djcelery" not in settings.INSTALLED_APPS:
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
            response = self.client.get(reverse('celery_inspect:active_status'))
            self.assertEqual(response.status_code, status.HTTP_501_NOT_IMPLEMENTED)

    def test_200_celery_inspect_registered(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(reverse('celery_inspect:registered'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_200_celery_inspect_scheduled(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(reverse('celery_inspect:scheduled'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
