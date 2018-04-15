"""Validators for fields in django"""
from django.core.exceptions import ValidationError
from django.template import Template, TemplateSyntaxError


def validate_template(data):
    """Validate a django template"""
    try:
        Template(data)
    except TemplateSyntaxError as error:
        raise ValidationError(unicode(error))
