"""Views for staff app"""
from django.views.generic import ListView

from accounts.models import User
from branding.mixins import OrganizationViewMixin
from manage.mixins import ManageViewMixin


class StaffListView(OrganizationViewMixin, ManageViewMixin, ListView):
    """List all users"""
    model = User
    queryset = User.objects.filter(is_staff=True).select_related()
    template_name = "staff/staff_list.html"
    paginate_by = 50
    context_object_name = 'users'
