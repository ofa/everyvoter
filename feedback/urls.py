"""URLs for Accounts app"""
from django.conf.urls import url

from feedback import views


# pylint: disable=invalid-name
urlpatterns = [
    url(r'^email/$',
        views.EmailFeedbackView.as_view(), name='process_email_feedback'),
]
