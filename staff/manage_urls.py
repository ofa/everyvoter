"""Management URLs for staff/admin app"""
from django.conf.urls import url

from staff import views


# pylint: disable=invalid-name
urlpatterns = [
    url(r'^$',
        views.StaffListView.as_view(), name='list_staff'),
]
