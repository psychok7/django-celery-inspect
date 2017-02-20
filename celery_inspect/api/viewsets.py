# -*- coding: utf-8 -*-

import celery

from django.conf import settings

from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.settings import api_settings


class CeleryInspectViewSet(viewsets.ViewSet):
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES
    inspect = celery.current_app.control.inspect()

    @list_route(methods=["get"])
    def ping(self, request):
        result = self.inspect.ping()
        return Response(result, status=status.HTTP_200_OK)

    @list_route(methods=["get"])
    def active(self, request):
        result = self.inspect.active()
        return Response(result, status=status.HTTP_200_OK)

    @list_route(methods=["get"])
    def active_status(self, request):
        """
        This will only work if you have django-celery installed (for now).
        In case you only need to work with status codes to find out if the
        workers are up or not.
        This will only work if we assume our db only contains "active workers".
        To use this feature, you must ensure you use only named workers,
        For example: "-n worker1@localhost:8000".
        http://docs.celeryproject.org/en/latest/userguide/workers.html#starting-the-worker
        """

        app_installed = "djcelery" in settings.INSTALLED_APPS
        if not app_installed:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

        from djcelery.models import WorkerState

        count_workers = WorkerState.objects.all().count()
        result = self.inspect.active()

        if count_workers == len(result):
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @list_route(methods=["get"])
    def registered(self, request):
        result = self.inspect.registered()
        return Response(result, status=status.HTTP_200_OK)

    @list_route(methods=["get"])
    def scheduled(self, request):
        result = self.inspect.scheduled()
        return Response(result, status=status.HTTP_200_OK)

