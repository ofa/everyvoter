"""URLs for Manage app"""
from django.contrib import admin
from django.conf.urls import url, include

from user_import import views


# pylint: disable=invalid-name
urlpatterns = [
    url(r'^$',
        views.ImportListView.as_view(), name='list_imports'),
]
