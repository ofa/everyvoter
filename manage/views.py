"""Views for EveryVoter Admin"""
from django.contrib.auth.views import (
    LoginView as DjangoLoginView,
    LogoutView as DjangoLogoutView
)
from django.urls import reverse_lazy
from django.views.generic import ListView
from rawpaginator.paginator import Paginator

from manage.forms import AuthenticationForm
from manage.mixins import ManageViewMixin
from mailer.send_calendar import mailing_calendar
from mailer.models import MailingTemplate


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


class ManageView(ManageViewMixin, ListView):
    """Management Homepage"""
    template_name = 'management/manage.html'
    context_object_name = 'sends'
    paginator_class = Paginator
    model = MailingTemplate
    paginate_by = 20

    def get_queryset(self):
        """Get the queryset"""
        return mailing_calendar(
            organization=self.request.organization, upcoming=True)

    def get_paginator(self, queryset, per_page, orphans=0,
                      allow_first_empty_page=True, **kwargs):
        """Get the paginator (in our case a RawQuerySet paginator)"""
        return Paginator(queryset, per_page)
