"""URLs for User Import app"""
from django.conf.urls import url

from user_import import views


# pylint: disable=invalid-name
urlpatterns = [
    url(r'^$',
        views.ImportListView.as_view(), name='list_imports'),
    url(r'^new/$',
        views.ImportCreateView.as_view(), name='create_import'),
]
