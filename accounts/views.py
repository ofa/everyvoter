"""Account-related Views"""
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from accounts.forms import UserForm
from accounts.utils_user import create_user


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


