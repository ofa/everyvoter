"""List filters for accounts"""
import django_filters

from election.models import LegislativeDistrict


class LegislativeDistrictFilter(django_filters.FilterSet):
    """Filter for the user list in the management panel"""
    name = django_filters.CharFilter(
        lookup_expr='icontains', label='Name Contains')

    class Meta(object):
        """Meta options for the filter"""
        model = LegislativeDistrict
        fields = ['state', 'district_type', 'name', 'ocd_id']
