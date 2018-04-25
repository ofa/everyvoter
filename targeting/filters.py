"""List filters for targeting"""
import django_filters

from targeting.models import Target


class TargetFilter(django_filters.FilterSet):
    """Filter for the target list in the management panel"""
    name = django_filters.CharFilter(
        lookup_expr='icontains', label='Name Contains')

    class Meta(object):
        """Meta options for the filter"""
        model = Target
        fields = ['name', 'district__district_type', 'district__state', 'tags']
