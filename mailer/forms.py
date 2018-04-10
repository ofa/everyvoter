"""Forms for mailer app"""
from django import forms

from mailer.models import Unsubscribe


class UnsubscribeForm(forms.ModelForm):
    """Unsubscribe form"""
    mailing_uuid = forms.CharField(widget=forms.HiddenInput(), required=False)
    user_uuid = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta(object):
        """Meta options for form"""
        model = Unsubscribe
        fields = ['email', 'mailing_uuid', 'user_uuid']
