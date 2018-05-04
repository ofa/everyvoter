"""Filters for geodatasets"""
import django_filters

from geodataset.models import GeoDataset


class GeoDatasetFilter(django_filters.FilterSet):
    """Filter for the dataset list in the management panel"""
    name = django_filters.CharFilter(
        lookup_expr='icontains', label='Name Contains')

    class Meta(object):
        """Meta options for the filter"""
        model = GeoDataset
        fields = ['name', 'categories']
