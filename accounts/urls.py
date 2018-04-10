"""URLs for Accounts app"""
from django.conf.urls import url

from accounts import views

# pylint: disable=invalid-name
urlpatterns = [
    url(r'^create/$',
        views.CreateUserView.as_view(), name='create_user'),
    url(r'^create/success/$',
        views.UserCreatedView.as_view(), name='create_user_success'),
    url(r'^(?P<slug>[-\w]+)/$',
        views.SelfUpdateUserView.as_view(),
        name='self_update_user'),
    url(r'^update/success/$',
        views.UserUpdatedView.as_view(), name='update_user_success'),
]
