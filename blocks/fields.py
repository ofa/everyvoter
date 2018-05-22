"""Block-related Form Fields"""
from django import forms
from django.forms.models import ModelChoiceIterator
from django.utils.safestring import SafeText

from blocks.models import Block
from blocks.widgets import BlockSelectWidget



class BlockChoiceIterator(ModelChoiceIterator):
    def choice(self, obj):
        return (self.field.prepare_value(obj), obj)


class BlockSelectField(forms.ModelMultipleChoiceField):
    """Field to select blocks"""
    widget = BlockSelectWidget
    iterator = BlockChoiceIterator

    def __init__(self, queryset=None, **kwargs):
        """Initialize the field"""
        if not queryset:
            queryset = Block.objects.all()
        super(BlockSelectField, self).__init__(
            queryset, **kwargs)
