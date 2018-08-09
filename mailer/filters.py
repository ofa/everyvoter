"""List filters for mailer"""
import django_filters

from mailer.models import MailingTemplate
from election.choices import DEADLINES, ELECTION_TYPES


class MailingTemplateFilter(django_filters.FilterSet):
    """Filter for the user list in the management panel"""
    name = django_filters.CharFilter(
        lookup_expr='icontains', label='Name Contains')
    election_type = django_filters.ChoiceFilter(
        label='Election Type', choices=ELECTION_TYPES)
    deadline_type = django_filters.ChoiceFilter(
        label='Deadline', choices=DEADLINES)

    class Meta(object):
        """Meta options for the filter"""
        model = MailingTemplate
        fields = ['name', 'election_type', 'deadline_type']
