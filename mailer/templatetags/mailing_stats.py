"""Handle Stats"""
from django import template


# pylint: disable=invalid-name
register = template.Library()


@register.simple_tag()
def generate_percent(mailing_count, total):
    """Templatetag to return a percentage of the count"""
    return "{:.1%}".format(float(total)/float(mailing_count))
