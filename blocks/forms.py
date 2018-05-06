"""Forms for account app"""
from django import forms

from blocks.models import Block
from election.models import Election, LegislativeDistrict

class BlockModelForm(forms.ModelForm):
    """Model form for blocks"""
    weight = forms.ChoiceField(choices=[(x, x) for x in range(1, 100)])

    class Meta(object):
        """Meta options for form"""
        model = Block
        fields = ['name', 'geodataset', 'weight', 'categories', 'code']


class BlockPreviewForm(forms.Form):
    """Preview form"""
    election = forms.ModelChoiceField(queryset=Election.objects.all())
    district = forms.ModelChoiceField(
        queryset=LegislativeDistrict.objects.all())
    block = forms.CharField(widget=forms.HiddenInput())
