"""Block-related Widgets"""
import json

from django import forms


class BlockSelectWidget(forms.SelectMultiple):
    """Widget to select blocks"""
    template_name = 'blocks/widgets/block_select_widget.html'

    def get_options(self, value):
        """Get the possible blocks"""
        options = []

        for (option_value, instance) in self.choices:
            if value:
                selected = bool(option_value in value)
            else:
                selected = False

            options.append({
                'block_name': instance.name,
                'block_key': option_value,
                'geodataset_name': instance.geodataset.name,
                'selected': selected
            })

        return options

    def get_context(self, name, value, attrs):
        """Get the context for the widget"""
        context = {}
        context['widget'] = {
            'name': name,
            'is_hidden': False,
            'required': False,
            'value': self.format_value(value),
            'attrs': self.build_attrs(self.attrs, attrs),
            'template_name': self.template_name,
            'options_json': json.dumps(self.get_options(value))
        }
        return context
