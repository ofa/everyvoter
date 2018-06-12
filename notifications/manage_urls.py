"""URLs for blocks app"""
from django.conf.urls import url

from notifications import views


# pylint: disable=invalid-name
urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/$',
        views.NotificationSettingUpdateView.as_view(),
        name='update_notificationsettings'),
]
