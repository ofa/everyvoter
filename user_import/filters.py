"""List filters for user imports"""
import django_filters

from user_import.models import UserImport


class UserImportFilter(django_filters.FilterSet):
    """Filter for the user import list in the management panel"""

    class Meta(object):
        """Meta options for the filter"""
        model = UserImport
        fields = ['status']
