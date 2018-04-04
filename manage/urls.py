"""URLs for Manage app"""
from django.conf.urls import url, include

from manage import views


# pylint: disable=invalid-name
urlpatterns = [
    url(r'^user_import/',
        include('user_import.manage_urls', namespace='user_import')),
    url(r'^users/',
        include('accounts.manage_urls', namespace='accounts')),
    url(r'^organization/',
        include('branding.manage_urls', namespace='branding')),
    url(r'^login/$',
        views.LoginView.as_view(), name='manage_login'),
    url(r'^logout/$',
        views.LogoutView.as_view(), name='manage_logout'),
    url(r'^$',
        views.ManageView.as_view(), name='manage'),
]
