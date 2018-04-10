"""Views for mailer"""
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy

from accounts.models import User
from branding.mixins import OrganizationViewMixin
from mailer.models import Unsubscribe, Mailing
from mailer.forms import UnsubscribeForm


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
