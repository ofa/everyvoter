"""Management urls for Targeting App"""
from django.conf.urls import url

from targeting import views


# pylint: disable=invalid-name
urlpatterns = [
    url(r'^target/$',
        views.TargetListView.as_view(), name='list_targets'),
    url(r'^target/create/$',
        views.TargetCreateView.as_view(), name='create_target'),
    url(r'^target/(?P<slug>[-\w]+)/edit/$',
        views.TargetUpdateView.as_view(),
        name='update_target'),
    url(r'^target/(?P<slug>[-\w]+)/delete/$',
        views.TargetDeleteView.as_view(),
        name='delete_target'),

    url(r'^targettag/$',
        views.TargetTagListView.as_view(), name='list_targettags'),
    url(r'^targettag/create/$',
        views.TargetTagCreateView.as_view(), name='create_targettag'),
    url(r'^targettag/(?P<slug>[-\w]+)/edit/$',
        views.TargetTagUpdateView.as_view(),
        name='update_targettag'),
    url(r'^targettag/(?P<slug>[-\w]+)/delete/$',
        views.TargetTagDeleteView.as_view(),
        name='delete_targettag'),
]
