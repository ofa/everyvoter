"""Account URLs for Manage app"""
from django.contrib import admin
from django.conf.urls import url, include

from accounts import views


# pylint: disable=invalid-name
urlpatterns = [
    url(r'^$',
        views.UserManageListView.as_view(), name='list_users'),
    url(r'^(?P<slug>[-\w]+)/$',
        views.UserManageDetailView.as_view(),
        name='view_user'),
]
