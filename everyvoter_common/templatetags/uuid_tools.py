"""Turn a UUID into SmallUUID"""
from django import template
from django.template.defaultfilters import stringfilter
import smalluuid

# pylint: disable=invalid-name
register = template.Library()

@register.filter
@stringfilter
def translate_uuid(value):
    """Templatetag to handle GET arguments on links"""
    return smalluuid.SmallUUID(hex=value)
