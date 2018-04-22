"""Mailing-related field validators"""
from django.core.exceptions import ValidationError
from django.template import Template, TemplateSyntaxError


def validate_template(template):
    """Validate a template passed to a field

    Django's built-in template engine has pretty-good debug functionality,
    throwing a TemplateSyntaxError whenever there is any issue with a template.
    If we just catch that error and pass it along as a ValidationError we have
    ourselves a pretty easy template validator.

    Args:
        template: django template copy
    """
    try:
        Template(template)
    except TemplateSyntaxError as error:
        raise ValidationError(
            'Template Syntax Error: {}'.format(unicode(error)))
