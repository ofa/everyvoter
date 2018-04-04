"""Views for Import App"""
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from manage.mixins import ManageViewMixin
from branding.mixins import OrganizationViewMixin
from user_import.models import UserImport
from user_import.tasks import ingest_import
from user_import.forms import UserImportForm


class ImportListView(OrganizationViewMixin, ManageViewMixin, ListView):
    """List all imports"""
    model = UserImport
    template_name = "user_import/list_imports.html"
    paginate_by = 10
    context_object_name = 'imports'


class ImportCreateView(OrganizationViewMixin, ManageViewMixin,
                       SuccessMessageMixin, CreateView):
    """Create a new import"""
    model = UserImport
    form_class = UserImportForm
    template_name = "user_import/create_import.html"
    success_url = reverse_lazy('manage:user_import:list_imports')
    success_message = "Import %(name)s was started"

    def form_valid(self, form):
        """Handle a valid form"""
        form.instance.uploader = self.request.user
        form.instance.organization = self.request.organization
        form.instance.status = 'pending'

        response = super(ImportCreateView, self).form_valid(form)

        ingest_import.delay(self.object.pk)

        return response
