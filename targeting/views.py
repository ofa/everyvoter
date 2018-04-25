"""Views for targeting"""
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.urls import reverse_lazy
from django_filters.views import FilterView

from manage.mixins import ManageViewMixin
from branding.mixins import OrganizationViewMixin, OrganizationCreateViewMixin
from targeting.models import Target, TargetTag
from targeting.filters import TargetFilter


class TargetListView(OrganizationViewMixin, ManageViewMixin, FilterView):
    """List all targets"""
    model = Target
    queryset = Target.objects.select_related(
        'election', 'district', 'district__state')
    paginate_by = 10
    context_object_name = 'targets'
    filterset_class = TargetFilter
    template_name_suffix = '_list'


class TargetCreateModifyObjectViewMixin(object):
    """Mixin for views that crea modify targets"""
    def get_form(self):
        """Get the form, but with tags scoped to that user's organization"""
        form = super(TargetCreateModifyObjectViewMixin, self).get_form()
        form.fields['tags'].queryset = form.fields['tags'].queryset.filter(
            organization=self.request.organization)
        # pylint: disable=line-too-long
        form.fields['district'].queryset = form.fields['district'].queryset.filter(
            district_type__in=['cd', 'state'])
        form.fields['blocks'].queryset = form.fields['blocks'].queryset.filter(
            organization=self.request.organization)
        return form


class TargetCreateView(ManageViewMixin, SuccessMessageMixin,
                       OrganizationCreateViewMixin,
                       TargetCreateModifyObjectViewMixin, CreateView):
    """Create a Target"""
    model = Target
    fields = ['name', 'target_type', 'election', 'district', 'blocks', 'tags']
    success_url = reverse_lazy('manage:targeting:list_targets')
    success_message = "Target %(name)s was created"


class TargetUpdateView(ManageViewMixin, SuccessMessageMixin,
                       OrganizationViewMixin,
                       TargetCreateModifyObjectViewMixin, UpdateView):
    """Edit a Target"""
    model = Target
    slug_field = 'uuid'
    fields = ['name', 'target_type', 'election', 'district', 'blocks', 'tags']
    context_object_name = 'target'
    success_url = reverse_lazy('manage:targeting:list_targets')
    success_message = "Target %(name)s was edited"


class TargetDeleteView(ManageViewMixin, SuccessMessageMixin,
                       OrganizationViewMixin, DeleteView):
    """Delete a Target"""
    model = Target
    slug_field = 'uuid'
    context_object_name = 'target'
    success_url = reverse_lazy('manage:targeting:list_targets')
    success_message = "Target %(name)s was deleted"


class TargetTagListView(OrganizationViewMixin, ManageViewMixin, ListView):
    """List all target tags"""
    model = TargetTag
    paginate_by = 10
    context_object_name = 'targettags'


class TargetTagCreateView(ManageViewMixin, SuccessMessageMixin,
                          OrganizationCreateViewMixin, CreateView):
    """Create a target tag"""
    model = TargetTag
    fields = ['name']
    success_url = reverse_lazy('manage:targeting:list_targettags')
    success_message = "Target Tag %(name)s was created"


class TargetTagUpdateView(ManageViewMixin, SuccessMessageMixin,
                          OrganizationViewMixin, UpdateView):
    """Edit a target tag"""
    model = TargetTag
    slug_field = 'uuid'
    fields = ['name']
    context_object_name = 'targettag'
    success_url = reverse_lazy('manage:targeting:list_targettags')
    success_message = "Target Tag %(name)s was edited"


class TargetTagDeleteView(ManageViewMixin, SuccessMessageMixin,
                          OrganizationViewMixin, DeleteView):
    """Delete a target tag"""
    model = TargetTag
    slug_field = 'uuid'
    context_object_name = 'targettag'
    success_url = reverse_lazy('manage:targeting:list_targettags')
    success_message = "Target Tag %(name)s was deleted"
