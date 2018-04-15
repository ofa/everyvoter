"""Views for mailer"""
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, ListView, TemplateView
from django.urls import reverse_lazy

from accounts.models import User
from manage.mixins import ManageViewMixin
from branding.mixins import OrganizationViewMixin
from mailer.models import EmailWrapper, Unsubscribe, Mailing
from mailer.forms import UnsubscribeForm


class WrapperListView(OrganizationViewMixin, ManageViewMixin, ListView):
    """List all imports"""
    model = EmailWrapper
    template_name = "mailer/list_wrappers.html"
    paginate_by = 10
    context_object_name = 'wrappers'


class WrapperCreateView(ManageViewMixin, SuccessMessageMixin, CreateView):
    """Create a wrapper"""
    model = EmailWrapper
    template_name = 'mailer/create_wrapper.html'
    fields = ['name', 'header', 'footer', 'default']
    success_url = reverse_lazy('manage:mailer:list_wrappers')
    success_message = "Wrapper %(name)s was created"

    def form_valid(self, form):
        """Handle a valid form"""
        form.instance.organization = self.request.organization

        return super(WrapperCreateView, self).form_valid(form)


class WrapperUpdateView(ManageViewMixin, SuccessMessageMixin, UpdateView):
    """Create a wrapper"""
    model = EmailWrapper
    template_name = 'mailer/edit_wrapper.html'
    fields = ['name', 'header', 'footer', 'default']
    context_object_name = 'wrapper'
    success_url = reverse_lazy('manage:mailer:list_wrappers')
    success_message = "Wrapper %(name)s was edited"


class UnsubscribeCreateView(OrganizationViewMixin, CreateView):
    """List all imports"""
    model = Unsubscribe
    template_name = "mailer/unsubscribe.html"
    form_class = UnsubscribeForm
    success_url = reverse_lazy('unsubscribe:unsubscribe_complete')

    def form_valid(self, form):
        """Handle a valid form"""
        form.instance.organization = self.request.organization
        form.instance.origin = 'user'

        if form.cleaned_data['mailing_uuid']:
            form.instance.mailing = Mailing.objects.filter(
                uuid=form.cleaned_data['mailing_uuid']).first()

        if form.cleaned_data['user_uuid']:
            form.instance.user = User.objects.filter(
                username=form.cleaned_data['user_uuid']).first()

        response = super(UnsubscribeCreateView, self).form_valid(form)

        User.objects.filter(email__iexact=form.cleaned_data['email']).update(
            unsubscribed=True)

        return response


class UnsubscribeCompleteView(TemplateView):
    """Page to show after unsubscription is successful"""
    template_name = "mailer/unsubscribe_complete.html"
