"""Views for Election"""
from django.views.generic import DetailView
from django_filters.views import FilterView

from branding.mixins import OrganizationViewMixin
from election.models import OrganizationElection
from election.filters import OrganizationElectionFilter
from manage.mixins import ManageViewMixin
from mailer.send_calendar import mailing_calendar


class OrgElectionListView(OrganizationViewMixin, ManageViewMixin, FilterView):
    """List all blocks"""
    queryset = OrganizationElection.objects.select_related(
        'election', 'election__state').order_by(
            '-election__election_type', 'election__election_date',
            'election__state')
    model = OrganizationElection
    paginate_by = 120
    context_object_name = 'elections'
    filterset_class = OrganizationElectionFilter
    template_name_suffix = '_list'


class OrgElectionDetailView(OrganizationViewMixin, ManageViewMixin, DetailView):
    """View details about an Organization Election"""
    model = OrganizationElection
    slug_field = 'uuid'
    context_object_name = 'orgelection'

    def get_context_data(self, *args, **kwargs):
        """Get context data"""
        context = super(
            OrgElectionDetailView, self).get_context_data(*args, **kwargs)
        context['election'] = context['orgelection'].election
        return context
