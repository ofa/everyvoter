"""Views for Import App"""
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy
from django_filters.views import FilterView
import unicodecsv

from manage.mixins import ManageViewMixin
from branding.mixins import OrganizationViewMixin, OrganizationCreateViewMixin
from everyvoter_common.utils.slug import slugify_header
from everyvoter_common.utils.uuid_slug_mixin import UUIDSlugMixin
from user_import.models import UserImport
from user_import.tasks import ingest_import
from user_import.forms import UserImportForm
from user_import.filters import UserImportFilter


class ImportListView(OrganizationViewMixin, ManageViewMixin, FilterView):
    """List all imports"""
    model = UserImport
    template_name = "user_import/list_imports.html"
    paginate_by = 15
    context_object_name = 'imports'
    filterset_class = UserImportFilter


class ImportCreateView(OrganizationViewMixin, ManageViewMixin,
                       SuccessMessageMixin, OrganizationCreateViewMixin,
                       CreateView):
    """Create a new import"""
    model = UserImport
    form_class = UserImportForm
    template_name = "user_import/create_import.html"
    success_url = reverse_lazy('manage:user_import:list_imports')
    success_message = "Import %(name)s was started"

    def form_valid(self, form):
        """Handle a valid form"""
        form.instance.uploader = self.request.user
        form.instance.status = 'pending'

        response = super(ImportCreateView, self).form_valid(form)

        ingest_import.delay(self.object.pk)

        return response


class ImportErrorCSVView(OrganizationViewMixin, ManageViewMixin,
                         UUIDSlugMixin, DetailView):
    """Download errors from a specific import"""
    model = UserImport
    slug_field = 'uuid'

    def render_to_response(self, context, **response_kwargs):
        """Render to response"""
        response = HttpResponse(content_type='text/csv')
        # pylint: disable=line-too-long
        response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(
            slugify_header(self.object.name))

        import_record_statuses = self.object.importrecordstatus_set.filter(
            status='failed').select_related('import_record')

        field_names = [
            'status',
            'error_type',
            'first_name',
            'last_name',
            'email',
            'address',
            'note'
        ]

        writer = unicodecsv.DictWriter(response, fieldnames=field_names)
        writer.writeheader()
        for import_record_status in import_record_statuses:
            import_record = import_record_status.import_record
            row = {
                'status': import_record_status.status,
                'error_type': import_record_status.error_type,
                'note': import_record_status.note,
                'first_name': import_record.first_name,
                'last_name': import_record.last_name,
                'email': import_record.email,
                'address': import_record.address
            }
            writer.writerow(row)

        return response
