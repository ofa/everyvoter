"""Views for Election"""
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DetailView, UpdateView
from django.urls import reverse
from django_filters.views import FilterView

from branding.mixins import OrganizationViewMixin
from election.models import OrganizationElection
from election.filters import OrganizationElectionFilter
from election.forms import OrgElectionNotificationForm
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
        context['notification_form'] = OrgElectionNotificationForm(
            instance=self.object)
        return context


class OrgElectionNotificationUpdateView(ManageViewMixin, OrganizationViewMixin,
                                        SuccessMessageMixin, UpdateView):
    """Edit an Organization Election notification options"""
    model = OrganizationElection
    slug_field = 'uuid'
    context_object_name = 'orgelection'
    form_class = OrgElectionNotificationForm
    success_message = "Mailing Types updated"

    def get_success_url(self):
        """Get the success URL"""
        return reverse('manage:election:view_election',
                       kwargs={'slug': self.object.uuid})
