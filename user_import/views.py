"""Views for Import App"""
from django.views.generic.list import ListView

from manage.mixins import ManageViewMixin
from branding.mixins import OrganizationViewMixin
from user_import.models import UserImport


class ImportListView(OrganizationViewMixin, ManageViewMixin, ListView):
    """List all imports"""
    model = UserImport
    template_name = "user_import/list_imports.html"
