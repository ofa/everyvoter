"""URLs for geodataset app"""
from django.conf.urls import url

from geodataset import views


# pylint: disable=invalid-name
urlpatterns = [
    url(r'^$',
        views.GeoDatasetListView.as_view(), name='list_geodatasets'),
    url(r'^datasets/create/$',
        views.GeoDatasetCreateView.as_view(), name='create_geodataset'),
    url(r'^datasets/(?P<slug>[-\w]+)/$',
        views.GeoDatasetDetailView.as_view(),
        name='view_geodataset'),
    url(r'^datasets/(?P<slug>[-\w]+)/update/$',
        views.GeoDatasetUpdateView.as_view(),
        name='update_geodataset'),
    url(r'^datasets/(?P<slug>[-\w]+)/delete/$',
        views.GeoDatasetDeleteView.as_view(),
        name='delete_geodataset'),
    url(r'^datasets/(?P<slug>[-\w]+)/download/$',
        views.GeoDatasetCSVView.as_view(),
        name='download_geodataset'),

    url(r'^entry/(?P<slug>[-\w]+)/$',
        views.EntryDetailView.as_view(),
        name='view_entry'),

    url(r'^entryvalue/(?P<slug>[-\w]+)/$',
        views.FieldValueUpdateView.as_view(),
        name='update_fieldvalue'),

    url(r'^category/$',
        views.GeoDatasetCategoryListView.as_view(),
        name='list_geodatasetcategories'),
    url(r'^category/create/$',
        views.GeoDatasetCategoryCreateView.as_view(),
        name='create_geodatasetcategory'),
    url(r'^category/(?P<slug>[-\w]+)/update/$',
        views.GeoDatasetCategoryUpdateView.as_view(),
        name='update_geodatasetcategory'),
    url(r'^category/(?P<slug>[-\w]+)/delete/$',
        views.GeoDatasetCategoryDeleteView.as_view(),
        name='delete_geodatasetcategory'),
]
