# -*- coding: utf-8 -*-

import celery

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
    def registered(self, request):
        result = self.inspect.registered()
        return Response(result, status=status.HTTP_200_OK)

    @list_route(methods=["get"])
    def active(self, request):
        result = self.inspect.active()
        return Response(result, status=status.HTTP_200_OK)

    @list_route(methods=["get"])
    def scheduled(self, request):
        result = self.inspect.scheduled()
        return Response(result, status=status.HTTP_200_OK)

