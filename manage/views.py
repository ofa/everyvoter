"""Views for EveryVoter Admin"""
from django.contrib.auth.views import (
    LoginView as DjangoLoginView,
    LogoutView as DjangoLogoutView
)
from django.urls import reverse_lazy
from django.utils.timezone import localdate
from django.views.generic import TemplateView


from manage.forms import AuthenticationForm
from manage.mixins import ManageViewMixin
from mailer.send_calendar import mailing_calendar
from mailer.models import Mailing
from election.models import OrganizationElection


class LoginView(DjangoLoginView):
    """Login view for the app"""
    form_class = AuthenticationForm
    template_name = 'management/auth/login.html'
    next_page = reverse_lazy('manage:manage')
    redirect_authenticated_user = True

    def get_success_url(self):
        """Get the URL to redirect the user in"""
        url = self.get_redirect_url()
        return url or self.next_page


class LogoutView(DjangoLogoutView):
    """Logout view for the app"""
    template_name = 'management/auth/logout.html'


class ManageView(ManageViewMixin, TemplateView):
    """Handle Management View"""
    template_name = 'management/manage.html'

    def get_context_data(self, *args, **kwargs):
        """Get the context of the page"""
        context = super(ManageView, self).get_context_data(*args, **kwargs)

        context['elections'] = OrganizationElection.objects.filter(
            election__election_date__gte=localdate(),
            organization=self.request.organization,
            ).order_by('election__election_date')[:10]

        context['sends'] = mailing_calendar(
            organization=self.request.organization, upcoming=True, limit=10)

        context['mailings'] = Mailing.objects.filter(
            email__organization=self.request.organization,
            ).select_related(
                'organization_election',
                'organization_election__election',
                'organization_election__election__state',
                'template').order_by('-created_at')[:10]

        return context
