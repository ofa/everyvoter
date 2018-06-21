"""Views for branding"""
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

from manage.mixins import ManageViewMixin
from branding.models import Organization


class OrgUpdateView(ManageViewMixin, SuccessMessageMixin, UpdateView):
    """Create a new import"""
    model = Organization
    fields = ['name', 'platform_name', 'homepage', 'privacy_url', 'terms_url',
              'main_unsubscribe_url', 'from_address', 'online_vr',
              'disable_vr_sameday', 'disable_vr_eday']
    template_name = "branding/update_organization.html"
    success_url = reverse_lazy('manage:branding:update_organization')
    success_message = "%(name)s updated"

    def get_object(self, queryset=None):
        """Get the object"""
        return self.request.organization

    def get_form(self):
        """Get the form"""
        form = super(OrgUpdateView, self).get_form()

        # pylint: disable=line-too-long
        form.fields['from_address'].queryset = form.fields['from_address'].queryset.filter(
            Q(organization=self.request.organization) | Q(
                organization__isnull=True))
        return form
