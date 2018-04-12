"""URLs for HireFire app"""
from django.conf.urls import url

from hirefire import views

# pylint: disable=invalid-name
urlpatterns = [
    url(r'^(?P<hirefire_token>[0-9a-f-]+)/info$',
        views.HireFireView.as_view(), name='hirefire'),
]
