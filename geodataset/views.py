"""Views for geodataset"""
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView, DetailView, UpdateView, ListView, DeleteView
)
from django_filters.views import FilterView
import unicodecsv

from branding.mixins import OrganizationViewMixin, OrganizationCreateViewMixin
from everyvoter_common.utils.soft_delete import SoftDeleteView
from everyvoter_common.utils.slug import slugify_header
from manage.mixins import ManageViewMixin
from geodataset.forms import GeoDatasetUploadForm
from geodataset.models import GeoDataset, GeoDatasetCategory, Entry, FieldValue
from geodataset.utils import (
    process_geodataset_file, generate_csv_data
)
from geodataset.filters import GeoDatasetFilter


class GeoDatasetListView(OrganizationViewMixin, ManageViewMixin, FilterView):
    """List of all GeoDatasets"""
    model = GeoDataset
    paginate_by = 10
    context_object_name = 'geodatasets'
    filterset_class = GeoDatasetFilter
    template_name_suffix = '_list'

    def get_context_data(self, *args, **kwargs):
        """Get the context for the page"""
        response = super(GeoDatasetListView, self).get_context_data(
            *args, **kwargs)

        # Only allow filtering of categories contained in its own organization
        response['filter'].filters['categories'].queryset = response[
            'filter'].filters['categories'].queryset.filter(
                organization=self.request.organization)

        return response


class CommonGeoDatasetEditView(OrganizationViewMixin, ManageViewMixin,
                               OrganizationCreateViewMixin, CreateView):
    """Create or edit a geodataset"""
    model = GeoDataset
    form_class = GeoDatasetUploadForm
    success_url = reverse_lazy('manage:dataset:list_geodatasets')

    def get_form(self):
        """Get the form"""
        form = super(CommonGeoDatasetEditView, self).get_form()

        # pylint: disable=line-too-long
        form.fields['categories'].queryset = form.fields['categories'].queryset.filter(
            organization=self.request.organization)

        return form


    def form_valid(self, form):
        """Handle a valid form"""

        if form.instance.pk:
            created = False
        else:
            created = True

        # Assign an organization and save the geodataset itself
        response = super(CommonGeoDatasetEditView, self).form_valid(form)

        if form.cleaned_data['file']:
            process_geodataset_file(
                form.cleaned_data['file'], self.object, created)

        return response


class GeoDatasetCreateView(CommonGeoDatasetEditView, CreateView):
    """Create a Geodataset"""


class GeoDatasetUpdateView(CommonGeoDatasetEditView, UpdateView):
    """Update a Geodataset"""
    slug_field = 'uuid'
    context_object_name = 'geodataset'

    def get_form(self):
        """Get the form"""
        form = super(GeoDatasetUpdateView, self).get_form()

        form.fields['file'].required = False

        return form


class GeoDatasetDetailView(OrganizationViewMixin, ManageViewMixin, DetailView):
    """Detail view for an individual GeoDataset"""
    model = GeoDataset
    slug_field = 'uuid'
    context_object_name = 'geodataset'


    def get_context_data(self, *args, **kwargs):
        """Get the context for the view"""
        context = super(GeoDatasetDetailView, self).get_context_data(
            *args, **kwargs)

        context['entries'] = self.object.entry_set.select_related(
            ).order_by('district__ocd_id')

        return context


class GeoDatasetDeleteView(OrganizationViewMixin, ManageViewMixin,
                           SoftDeleteView):
    """Delete a geodataset"""
    model = GeoDataset
    slug_field = 'uuid'
    context_object_name = 'geodataset'
    success_url = reverse_lazy('manage:dataset:list_geodatasets')


class GeoDatasetCSVView(OrganizationViewMixin, ManageViewMixin, DetailView):
    """Download a CSV of an individual GeoDataset"""
    model = GeoDataset
    slug_field = 'uuid'

    def render_to_response(self, context, **response_kwargs):
        """Render to response"""
        response = HttpResponse(content_type='text/csv')
        # pylint: disable=line-too-long
        response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(
            slugify_header(self.object.name))

        data, field_names = generate_csv_data(self.object)

        writer = unicodecsv.DictWriter(response, fieldnames=field_names)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

        return response


class EntryDetailView(ManageViewMixin, DetailView):
    """Detail view of an entry"""
    model = Entry
    slug_field = 'uuid'
    queryset = Entry.objects.select_related('district', 'geodataset')
    context_object_name = 'entry'

    def get_queryset(self):
        """Get the queryset filtered by organization"""
        queryset = super(EntryDetailView, self).get_queryset()
        return queryset.filter(
            geodataset__organization=self.request.organization)


class FieldValueUpdateView(ManageViewMixin, UpdateView):
    """Update a FieldValue"""
    model = FieldValue
    slug_field = 'uuid'
    fields = ['value']
    context_object_name = 'fieldvalue'
    queryset = FieldValue.objects.select_related(
        'entry', 'field', 'entry__geodataset', 'entry__district')

    def get_queryset(self):
        """Get the queryset filtered by organization"""
        queryset = super(FieldValueUpdateView, self).get_queryset()
        return queryset.filter(
            entry__geodataset__organization=self.request.organization)

    def get_success_url(self):
        """Get the URL to redirect to on a successful update"""
        return reverse('manage:dataset:view_entry',
                       kwargs={'slug': self.object.entry.uuid})


class GeoDatasetCategoryListView(OrganizationViewMixin, ManageViewMixin,
                                 ListView):
    """List all geodataset categories"""
    model = GeoDatasetCategory
    paginate_by = 10
    context_object_name = 'geodatasetcategories'


class GeoDatasetCategoryCreateView(ManageViewMixin, SuccessMessageMixin,
                                   OrganizationCreateViewMixin, CreateView):
    """Create a geodataset category"""
    model = GeoDatasetCategory
    fields = ['name']
    success_url = reverse_lazy('manage:dataset:list_geodatasetcategories')
    success_message = "Dataset Category %(name)s was created"


class GeoDatasetCategoryUpdateView(ManageViewMixin, SuccessMessageMixin,
                                   OrganizationViewMixin, UpdateView):
    """Edit a geodataset category"""
    model = GeoDatasetCategory
    slug_field = 'uuid'
    fields = ['name']
    context_object_name = 'geodatasetcategory'
    success_url = reverse_lazy('manage:dataset:list_geodatasetcategories')
    success_message = "Dataset Category %(name)s was edited"


class GeoDatasetCategoryDeleteView(ManageViewMixin, SuccessMessageMixin,
                                   OrganizationViewMixin, DeleteView):
    """Delete a geodataset category"""
    model = GeoDatasetCategory
    slug_field = 'uuid'
    context_object_name = 'geodatasetcategory'
    success_url = reverse_lazy('manage:dataset:list_geodatasetcategories')
    success_message = "Dataset Category %(name)s was deleted"
