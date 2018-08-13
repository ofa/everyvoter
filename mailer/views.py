"""Views for mailer"""
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView, UpdateView, ListView, TemplateView, FormView
)
from django.views.generic.detail import SingleObjectMixin, BaseDetailView
from django.urls import reverse_lazy, reverse
from django_filters.views import FilterView
from rawpaginator.paginator import Paginator

from accounts.models import User
from manage.mixins import ManageViewMixin
from branding.mixins import OrganizationViewMixin, OrganizationCreateViewMixin
from blocks.models import Block
from everyvoter_common.utils.multi_form_view import MultipleFormsView
from everyvoter_common.utils.soft_delete import SoftDeleteView
from everyvoter_common.utils.uuid_slug_mixin import UUIDSlugMixin
from mailer.models import (
    EmailWrapper, Unsubscribe, Mailing, MailingTemplate, Email
)
from mailer.forms import (
    UnsubscribeForm, MailingTemplateForm, EmailForm, EmailPreviewForm
)
from mailer.filters import MailingTemplateFilter
from mailer.send_calendar import mailing_calendar



class EmailOrganizationViewMixin(object):
    """Mixin for listviews that list objects with email one-to-one fields"""

    def get_queryset(self):
        """Get the Mailing/MailingTemplate queryset filtered by organization"""
        queryset = super(EmailOrganizationViewMixin, self).get_queryset()
        return queryset.filter(email__organization=self.request.organization)


class SentMailingListView(EmailOrganizationViewMixin, ManageViewMixin,
                          ListView):
    """List all sent mailings"""
    model = Mailing
    queryset = Mailing.objects.select_related().order_by('-created_at')
    paginate_by = 30
    context_object_name = 'mailings'
    template_name_suffix = '_list'


class MailingTemplateListView(EmailOrganizationViewMixin, ManageViewMixin,
                              FilterView):
    """List all mailing templates"""
    model = MailingTemplate
    queryset = MailingTemplate.objects.select_related('email').filter(
        active=True)
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
            organization=self.request.organization).select_related('geodataset')

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

        email.blocks.clear()
        for block in forms['email_form'].cleaned_data['blocks']:
            email.blocks.add(block)

        if not hasattr(self, 'object'):
            self.object = mailing_template

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
    queryset = MailingTemplate.objects.select_related('email').order_by('pk')
    context_object_name = 'mailing_template'

    def dispatch(self, request, *args, **kwargs):
        """Dispatch the MailingTemplateUpdateView View"""
        # pylint: disable=attribute-defined-outside-init
        self.object = get_object_or_404(self.get_queryset(),
                                        email__uuid=kwargs['slug'])

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


class MailingTemplateDeleteView(EmailOrganizationViewMixin, SoftDeleteView):
    """Allow deletion of email"""
    model = MailingTemplate
    context_object_name = 'mailing_template'
    slug_field = 'email__uuid'
    success_url = reverse_lazy('manage:mailer:list_templates')


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


class UpcomingMailingsView(ManageViewMixin, ListView):
    """Management Homepage"""
    template_name = 'mailer/upcoming_list.html'
    context_object_name = 'sends'
    paginator_class = Paginator
    model = MailingTemplate
    paginate_by = 20

    def get_queryset(self):
        """Get the queryset"""
        return mailing_calendar(
            organization=self.request.organization, upcoming=True)

    def get_paginator(self, queryset, per_page, orphans=0,
                      allow_first_empty_page=True, **kwargs):
        """Get the paginator (in our case a RawQuerySet paginator)"""
        return Paginator(queryset, per_page)


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


class WrapperUpdateView(OrganizationViewMixin, ManageViewMixin,
                        SuccessMessageMixin, UUIDSlugMixin, UpdateView):
    """Create a wrapper"""
    model = EmailWrapper
    slug_field = 'uuid'
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

    def dispatch(self, request, *args, **kwargs):
        """Dispatch the view"""
        # pylint: disable=attribute-defined-outside-init
        user_uuid = request.GET.get('user')

        try:
            self.unsub_user = User.objects.filter(
                username=user_uuid, organization=request.organization).first()
        except ValueError:
            self.unsub_user = None

        return super(UnsubscribeCreateView, self).dispatch(
            request, *args, **kwargs)

    def get_form(self):
        """Get the form"""
        form = super(UnsubscribeCreateView, self).get_form()

        if self.unsub_user:
            form.fields['address'].initial = self.unsub_user.email

        return form

    def form_valid(self, form):
        """Handle a valid form"""
        form.instance.origin = 'user'

        try:
            email = Email.objects.filter(
                uuid=self.request.GET.get('email'),
                organization=self.request.organization).first()
        except ValueError:
            email = None

        if email:
            form.instance.email = email

        if self.unsub_user:
            form.instance.user = self.unsub_user
            User.objects.filter(Q(id=self.unsub_user.id) |
                                Q(email__iexact=form.cleaned_data['address'])
                               ).update(unsubscribed=True)
        else:
            User.objects.filter(
                email__iexact=form.cleaned_data['address']).update(
                    unsubscribed=True)

        return super(UnsubscribeCreateView, self).form_valid(form)


class UnsubscribeCompleteView(TemplateView):
    """Page to show after unsubscription is successful"""
    template_name = "mailer/unsubscribe_complete.html"
