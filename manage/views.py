"""Views for EveryVoter Admin"""
from django.contrib.auth.views import (
    LoginView as DjangoLoginView,
    LogoutView as DjangoLogoutView
)
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from manage.forms import AuthenticationForm
from manage.mixins import ManageViewMixin


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
    """Management Homepage"""
    template_name = 'management/manage.html'
