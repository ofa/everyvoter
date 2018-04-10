"""Unsubscription-related URLs"""
from django.conf.urls import url

from mailer.views import UnsubscribeCreateView, UnsubscribeCompleteView


# pylint: disable=invalid-name
urlpatterns = [
    url(r'^$',
        UnsubscribeCreateView.as_view(), name='unsubscribe'),
    url(r'^complete/$',
        UnsubscribeCompleteView.as_view(), name='unsubscribe_complete'),
]
