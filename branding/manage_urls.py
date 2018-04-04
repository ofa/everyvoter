"""URLs for Manage app"""
from django.conf.urls import url

from branding import views


# pylint: disable=invalid-name
urlpatterns = [
    url(r'^update/$',
        views.OrgUpdateView.as_view(), name='update_organization'),
]
