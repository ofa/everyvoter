"""URLs for Manage app"""
from django.conf.urls import url, include

from manage import views


# pylint: disable=invalid-name
urlpatterns = [
    url(r'^login/$',
        views.LoginView.as_view(), name='manage_login'),
    url(r'^logout/$',
        views.LogoutView.as_view(), name='manage_logout'),
    url(r'^$',
        views.ManageView.as_view(), name='manage'),
]
