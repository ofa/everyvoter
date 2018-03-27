"""URLs for Accounts app"""
from django.conf.urls import url

from accounts.views import CreateUserView, UserCreatedView

# pylint: disable=invalid-name
urlpatterns = [
    url(r'^create/$',
        CreateUserView.as_view(), name='create_user'),
    url(r'^create/success/$',
        UserCreatedView.as_view(), name='create_user_success'),
]
