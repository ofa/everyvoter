"""Account URLs for accounts app"""
from django.conf.urls import url

from accounts import views


# pylint: disable=invalid-name
urlpatterns = [
    url(r'^$',
        views.UserManageListView.as_view(), name='list_users'),
    url(r'^(?P<slug>[-\w]+)/$',
        views.UserManageDetailView.as_view(),
        name='view_user'),
]
