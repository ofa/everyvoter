"""Forms for mailer app"""
from django import forms

from election.models import Election
from mailer.models import Unsubscribe, Email, MailingTemplate


class UnsubscribeForm(forms.ModelForm):
    """Unsubscribe form"""
    email_uuid = forms.CharField(widget=forms.HiddenInput(), required=False)
    user_uuid = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta(object):
        """Meta options for form"""
        model = Unsubscribe
        fields = ['address', 'email_uuid', 'user_uuid']


class MailingTemplateForm(forms.ModelForm):
    """Main template form"""
    class Meta(object):
        """Meta options for form"""
        model = MailingTemplate
        fields = ['name', 'deadline_type', 'days_to_deadline', 'election_type']


class EmailForm(forms.ModelForm):
    """Email form"""

    class Meta(object):
        """Meta options for form"""
        model = Email
        fields = ['from_name', 'subject', 'pre_header', 'body_above',
                  'body_below', 'blocks']


class EmailPreviewForm(forms.Form):
    """Preview form"""
    election = forms.ModelChoiceField(queryset=Election.objects.all())
    ocd_ids = forms.CharField(
        help_text='Comma separated list of OCD IDs', required=False)
    sample_address = forms.EmailField(
        label='Sample Email',
        help_text='Optional address to send email sample to',
        required=False)
    email = forms.CharField(widget=forms.HiddenInput())
