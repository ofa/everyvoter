"""List filters for accounts"""
import django_filters

from accounts.models import User
from election.choices import STATES


class AccountManageFilter(django_filters.FilterSet):
    """Filter for the user list in the management panel"""
    email = django_filters.CharFilter(
        lookup_expr='icontains', label='Email Address Contains')
    location__state__code = django_filters.ChoiceFilter(
        label='Home State', choices=STATES)

    class Meta(object):
        """Meta options for the filter"""
        model = User
        fields = ['email', 'location__state__code']
