"""Views for Election"""
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DetailView, UpdateView
from django.urls import reverse
from django_filters.views import FilterView

from branding.mixins import OrganizationViewMixin
from election.models import OrganizationElection
from election.filters import OrganizationElectionFilter
from election.forms import OrgElectionNotificationForm, OrgElectionWrapperForm
from everyvoter_common.utils.uuid_slug_mixin import UUIDSlugMixin
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


class OrgElectionDetailView(OrganizationViewMixin, ManageViewMixin,
                            UUIDSlugMixin, DetailView):
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

        context['wrapper_form'] = OrgElectionWrapperForm(instance=self.object)
        context['wrapper_form'].fields['email_wrapper'].queryset = context[
            'wrapper_form'].fields['email_wrapper'].queryset.filter(
                organization=self.request.organization)

        return context


class GenericOrgElectionUpdateView(ManageViewMixin, OrganizationViewMixin,
                                   SuccessMessageMixin, UUIDSlugMixin,
                                   UpdateView):
    """Generic Organization Election update view"""
    model = OrganizationElection
    slug_field = 'uuid'
    context_object_name = 'orgelection'

    def get_success_url(self):
        """Get the success URL"""
        return reverse('manage:election:view_election',
                       kwargs={'slug': self.object.uuid})


class OrgElectionNotificationUpdateView(GenericOrgElectionUpdateView):
    """Edit an Organization Election notification options"""
    form_class = OrgElectionNotificationForm
    success_message = "Mailing Types updated"


class OrgElectionWrapperUpdateView(GenericOrgElectionUpdateView):
    """Update the wrapper for Organization Election"""
    form_class = OrgElectionWrapperForm
    success_message = "Mailing Wrapper updated"

    def get_context_data(self, *args, **kwargs):
        """Get context data"""
        context = super(
            OrgElectionWrapperUpdateView, self).get_context_data(
                *args, **kwargs)

        context['form'].fields['email_wrapper'].queryset = context[
            'form'].fields['email_wrapper'].queryset.filter(
                organization=self.request.organization)

        return context
