"""List filters for mailer"""
import django_filters

from mailer.models import MailingTemplate


class MailingTemplateFilter(django_filters.FilterSet):
    """Filter for the user list in the management panel"""
    name = django_filters.CharFilter(
        lookup_expr='icontains', label='Name Contains')

    class Meta(object):
        """Meta options for the filter"""
        model = MailingTemplate
        fields = ['name']
