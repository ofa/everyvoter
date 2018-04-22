"""Forms for mailer app"""
from django import forms

from mailer.models import Unsubscribe, MailingTemplate


class UnsubscribeForm(forms.ModelForm):
    """Unsubscribe form"""
    mailing_uuid = forms.CharField(widget=forms.HiddenInput(), required=False)
    user_uuid = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta(object):
        """Meta options for form"""
        model = Unsubscribe
        fields = ['email', 'mailing_uuid', 'user_uuid']


class MailingTemplateForm(forms.ModelForm):
    """Main template form"""
    class Meta(object):
        """Meta options for form"""
        model = MailingTemplate
        fields = ['name', 'deadline_type', 'days_to_deadline', 'from_name',
                  'tags', 'subject', 'pre_header', 'body_above', 'blocks',
                  'body_below']

    def save(self, commit=True):
        """Save the form

        We need to override the parent save() because that method will try to
        create the blocks, which causes all sorts of havok.
        """
        self.instance.save()
        return self.instance
