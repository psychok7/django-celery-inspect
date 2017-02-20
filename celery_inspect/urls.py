from django.conf.urls import url

from celery_inspect.api.viewsets import CeleryInspectViewSet


ping = CeleryInspectViewSet.as_view({'get': 'ping'})
active = CeleryInspectViewSet.as_view({'get': 'active'})
active_status = CeleryInspectViewSet.as_view({'get': 'active_status'})
registered = CeleryInspectViewSet.as_view({'get': 'registered'})
scheduled = CeleryInspectViewSet.as_view({'get': 'scheduled'})


# Register Viewsets explicitly because we do not have a router in the app.
# Not sure if there is a better way of doing this
# http://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/#binding-viewsets-to-urls-explicitly
urlpatterns = [
    url(r'^ping/$', ping, name='ping'),
    url(r'^active/$', active, name='active'),
    url(r'^active-status/$', active_status, name='active_status'),
    url(r'^registered/$', registered, name='registered'),
    url(r'^scheduled/$', scheduled, name='scheduled'),
]

