"""Account-related Views"""
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, ListView, DetailView

from accounts.forms import UserForm
from accounts.utils_user import create_user
from accounts.models import User
from branding.mixins import OrganizationViewMixin
from manage.mixins import ManageViewMixin


class CreateUserView(FormView):
    """View of the Homepage"""
    template_name = "accounts/create_user.html"
    form_class = UserForm
    success_url = reverse_lazy('accounts:create_user_success')

    def form_valid(self, form):
        """Process a form that passed basic form-based validation"""
        try:
            create_user(
                organization=self.request.organization,
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'])
        except ValidationError as error:
            form.add_error(None, error)
            form.data = form.data.copy()
            form.data['address'] = ''
            return super(CreateUserView, self).form_invalid(form)
        return super(CreateUserView, self).form_valid(form)


class UserCreatedView(TemplateView):
    """Page to show after user is successfully created"""
    template_name = "accounts/user_created.html"


class UserManageListView(OrganizationViewMixin, ManageViewMixin, ListView):
    """List all users"""
    model = User
    template_name = "accounts/manage/list_users.html"
    paginate_by = 10
    context_object_name = 'accounts'


class UserManageDetailView(OrganizationViewMixin, ManageViewMixin, DetailView):
    """View a single user"""
    model = User
    template_name = "accounts/manage/view_user.html"
    context_object_name = 'account'
    slug_field = 'username'
