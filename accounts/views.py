"""Account-related Views"""
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.views.generic import (
    FormView, TemplateView, DetailView, UpdateView
)
from django_filters.views import FilterView

from accounts.filters import AccountManageFilter
from accounts.forms import UserForm, UserEditForm
from accounts.models import User
from accounts.utils_user import create_user, update_user_location
from branding.mixins import OrganizationViewMixin
from everyvoter_common.utils.uuid_slug_mixin import UUIDSlugMixin
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


class SelfUpdateUserView(OrganizationViewMixin, UUIDSlugMixin, UpdateView):
    """Allow a user to update their record"""
    model = User
    form_class = UserEditForm
    template_name = "accounts/update_user.html"
    slug_field = 'username'
    success_url = reverse_lazy('accounts:update_user_success')
    context_object_name = 'account'

    def form_valid(self, form):
        """Process a valid form"""
        if form.cleaned_data['address']:
            try:
                update_user_location(
                    self.object,
                    form.cleaned_data['address'])
            except ValidationError as error:
                form.add_error(None, error)
                form.data = form.data.copy()
                form.data['address'] = ''
                return super(SelfUpdateUserView, self).form_invalid(form)
        return super(SelfUpdateUserView, self).form_valid(form)


class UserUpdatedView(TemplateView):
    """Page to show after user is successfully created"""
    template_name = "accounts/user_updated.html"


class UserCreatedView(TemplateView):
    """Page to show after user is successfully created"""
    template_name = "accounts/user_created.html"


class UserManageListView(OrganizationViewMixin, ManageViewMixin, FilterView):
    """List all users"""
    model = User
    queryset = User.objects.select_related()
    template_name = "accounts/manage/list_users.html"
    paginate_by = 20
    context_object_name = 'accounts'
    filterset_class = AccountManageFilter


class UserManageDetailView(OrganizationViewMixin, UUIDSlugMixin,
                           ManageViewMixin, DetailView):
    """View a single user"""
    model = User
    template_name = "accounts/manage/view_user.html"
    context_object_name = 'account'
    slug_field = 'username'

    def get_context_data(self, object):
        """Get context for view"""
        context = super(UserManageDetailView, self).get_context_data()

        context['email_activity'] = object.emailactivity_set.select_related(
            'email', 'email__mailing', 'email__mailing__template',
            'email__mailing__organization_election',
            'email__mailing__organization_election__election',
            'email__mailing__organization_election__election__state').exclude(
                email__isnull=True)

        return context
