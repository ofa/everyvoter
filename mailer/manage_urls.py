"""URLs for Manage app"""
from django.contrib import admin
from django.conf.urls import url, include

from mailer import views


# pylint: disable=invalid-name
urlpatterns = [
    url(r'^templates/$',
        views.MailingTemplateListView.as_view(),
        name='list_templates'),
    url(r'^templates/create/$',
        views.MailingTemplateFormView.as_view(), name='create_template'),
    url(r'^templates/(?P<slug>[-\w]+)/edit/$',
        views.MailingTemplateUpdateView.as_view(),
        name='update_template'),

    url(r'^wrappers/$',
        views.WrapperListView.as_view(), name='list_wrappers'),
    url(r'^wrappers/create/$',
        views.WrapperCreateView.as_view(), name='create_wrapper'),
    url(r'^wrappers/(?P<pk>[-\w]+)/edit/$',
        views.WrapperUpdateView.as_view(),
        name='update_wrapper'),
]
