"""URLs for rendering app"""
from django.conf.urls import url

from rendering import views


# pylint: disable=invalid-name
urlpatterns = [
    url(r'^preview/email/$',
        views.EmailPreviewView.as_view(),
        name='preview_email'),
    url(r'^preview/block/$',
        views.BlockPreviewView.as_view(),
        name='preview_block'),
]
