"""Forms for account app"""
from django import forms

from blocks.models import Block

class BlockModelForm(forms.ModelForm):
    """Model form for blocks"""
    weight = forms.ChoiceField(choices=[(x, x) for x in range(1, 100)])

    class Meta(object):
        """Meta options for form"""
        model = Block
        fields = ['name', 'weight', 'categories', 'code']
