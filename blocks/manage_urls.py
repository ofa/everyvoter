"""URLs for blocks app"""
from django.conf.urls import url

from blocks import views


# pylint: disable=invalid-name
urlpatterns = [
    url(r'^block/$',
        views.BlockListView.as_view(), name='list_blocks'),
    url(r'^block/create/$',
        views.BlockCreateView.as_view(), name='create_block'),
    url(r'^block/(?P<slug>[-\w]+)/edit/$',
        views.BlockUpdateView.as_view(),
        name='update_block'),
    url(r'^block/(?P<slug>[-\w]+)/delete/$',
        views.BlockDeleteView.as_view(),
        name='delete_block'),
    url(r'^block/(?P<slug>[-\w]+)/preview/$',
        views.BlockPreviewView.as_view(),
        name='preview_block'),

    url(r'^categories/$',
        views.BlockCategoryListView.as_view(), name='list_blockcategories'),
    url(r'^categories/create/$',
        views.BlockCategoryCreateView.as_view(), name='create_blockcategory'),
    url(r'^categories/(?P<slug>[-\w]+)/edit/$',
        views.BlockCategoryUpdateView.as_view(),
        name='update_blockcategory'),
    url(r'^categories/(?P<slug>[-\w]+)/delete/$',
        views.BlockCategoryDeleteView.as_view(),
        name='delete_blockcategory'),
]
