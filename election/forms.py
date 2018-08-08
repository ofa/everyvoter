"""Forms for election app"""
from django import forms

from election.models import OrganizationElection


class OrgElectionNotificationForm(forms.ModelForm):
    """Update notification preferences of org election"""

    class Meta(object):
        """Meta options for form"""
        model = OrganizationElection
        fields = ['vbm_active', 'evip_active', 'vr_active', 'eday_active']
