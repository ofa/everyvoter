"""Views for branding"""
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

from manage.mixins import ManageViewMixin
from branding.models import Organization


class OrgUpdateView(ManageViewMixin, SuccessMessageMixin, UpdateView):
    """Create a new import"""
    model = Organization
    fields = ['name', 'platform_name', 'homepage', 'privacy_url', 'terms_url']
    template_name = "branding/update_organization.html"
    success_url = reverse_lazy('manage:branding:update_organization')
    success_message = "%(name)s updated"

    def get_object(self, queryset=None):
        """Get the object"""
        return self.request.organization
