"""Views for mailer"""
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    CreateView, UpdateView, ListView, TemplateView, FormView
)
from django.views.generic.detail import SingleObjectMixin, BaseDetailView
from django.urls import reverse_lazy, reverse
from django_filters.views import FilterView

from accounts.models import User
from manage.mixins import ManageViewMixin
from branding.mixins import OrganizationViewMixin, OrganizationCreateViewMixin
from blocks.models import Block, EmailBlocks
from everyvoter_common.utils.multi_form_view import MultipleFormsView
from mailer.models import (
    EmailWrapper, Unsubscribe, Mailing, MailingTemplate, Email
)
from mailer.forms import (
    UnsubscribeForm, MailingTemplateForm, EmailForm, EmailPreviewForm
)
from mailer.filters import MailingTemplateFilter



class EmailOrganizationViewMixin(object):
    """Mixin for listviews that list objects with email one-to-one fields"""

    def get_queryset(self):
        """Get the Mailing/MailingTemplate queryset filtered by organization"""
        queryset = super(EmailOrganizationViewMixin, self).get_queryset()
        return queryset.filter(email__organization=self.request.organization)


class MailingTemplateListView(EmailOrganizationViewMixin, ManageViewMixin,
                              FilterView):
    """List all mailing templates"""
    model = MailingTemplate
    queryset = MailingTemplate.objects.select_related('email')
    paginate_by = 10
    context_object_name = 'mailing_templates'
    filterset_class = MailingTemplateFilter
    template_name_suffix = '_list'


class MailingTemplateFormView(ManageViewMixin, MultipleFormsView):
    """View to create or update a MailingTemplateForm"""
    form_classes = {
        'email_form': EmailForm,
        'mailing_template_form': MailingTemplateForm
    }
    template_name = 'mailer/mailingtemplate_form.html'
    success_url = reverse_lazy('manage:mailer:list_templates')

    def get_forms(self, form_classes):
        """Get the forms"""
        forms = super(MailingTemplateFormView, self).get_forms(form_classes)

        forms['email_form'].fields['blocks'].queryset = Block.objects.filter(
            organization=self.request.organization)

        return forms

    def form_valid(self, forms, all_cleaned_data):
        """Handle a valid form"""
        email = forms['email_form'].instance
        mailing_template = forms['mailing_template_form'].instance

        if email.pk:
            success_message = u'Template {name} Edited'.format(
                name=mailing_template.name)
        else:
            success_message = u'Template {name} Created'.format(
                name=mailing_template.name)

        if not hasattr(email, 'organization'):
            email.organization = self.request.organization

        email.save()

        if not hasattr(mailing_template, 'email'):
            mailing_template.email = email

        mailing_template.save()


        EmailBlocks.objects.filter(email=email).delete()
        new_blocks = []
        for block in forms['email_form'].cleaned_data['blocks']:
            new_blocks.append(EmailBlocks(email=email, block=block))
        EmailBlocks.objects.bulk_create(new_blocks)

        messages.success(self.request, success_message)

        return super(MailingTemplateFormView, self).form_valid(
            forms, all_cleaned_data)

    def get_success_url(self):
        """Get the success URL"""
        if 'save_preview' in self.request.POST:
            return reverse(
                'manage:mailer:preview_email', args=[self.object.email.uuid])
        return super(MailingTemplateFormView, self).get_success_url()


class MailingTemplateUpdateView(EmailOrganizationViewMixin,
                                SingleObjectMixin,
                                MailingTemplateFormView):
    """View to update a mailing template"""
    model = MailingTemplate
    queryset = MailingTemplate.objects.select_related('email')
    context_object_name = 'mailing_template'

    def dispatch(self, request, *args, **kwargs):
        """Dispatch the MailingTemplateUpdateView View"""
        # pylint: disable=attribute-defined-outside-init
        self.object = self.get_queryset().get(email__uuid=kwargs['slug'])

        return super(MailingTemplateUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self, form_class_name):
        """Get kwargs for the forms."""
        kwargs = super(MailingTemplateUpdateView, self).get_form_kwargs(
            form_class_name)
        if form_class_name == 'email_form':
            kwargs['instance'] = self.object.email
        elif form_class_name == 'mailing_template_form':
            kwargs['instance'] = self.object
        return kwargs


class EmailPreviewView(ManageViewMixin, OrganizationViewMixin, BaseDetailView,
                       FormView):
    """Preview an email"""
    model = Email
    slug_field = 'uuid'
    form_class = EmailPreviewForm
    template_name = 'mailer/email_preview.html'
    context_object_name = 'email'

    def get_form(self):
        """Get the form"""
        form = super(EmailPreviewView, self).get_form()
        form.fields['email'].initial = self.object.id
        return form


class WrapperListView(OrganizationViewMixin, ManageViewMixin, ListView):
    """List all imports"""
    model = EmailWrapper
    paginate_by = 10
    context_object_name = 'wrappers'


class WrapperCreateView(ManageViewMixin, SuccessMessageMixin,
                        OrganizationCreateViewMixin, CreateView):
    """Create a wrapper"""
    model = EmailWrapper
    fields = ['name', 'header', 'footer', 'default']
    success_url = reverse_lazy('manage:mailer:list_wrappers')
    success_message = "Wrapper %(name)s was created"


class WrapperUpdateView(ManageViewMixin, SuccessMessageMixin, UpdateView):
    """Create a wrapper"""
    model = EmailWrapper
    fields = ['name', 'header', 'footer', 'default']
    context_object_name = 'wrapper'
    success_url = reverse_lazy('manage:mailer:list_wrappers')
    success_message = "Wrapper %(name)s was edited"


    def get_form(self):
        """Get the form"""
        form = super(WrapperUpdateView, self).get_form()

        if self.object and self.object.default:
            del form.fields['default']

        return form


class UnsubscribeCreateView(OrganizationViewMixin,
                            OrganizationCreateViewMixin, CreateView):
    """List all imports"""
    model = Unsubscribe
    template_name = "mailer/unsubscribe.html"
    form_class = UnsubscribeForm
    success_url = reverse_lazy('unsubscribe:unsubscribe_complete')

    def form_valid(self, form):
        """Handle a valid form"""
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
