"""Slugify-related utilties"""
from slugify import slugify


def slugify_header(header_field):
    """Take a header field and return the clean ASCII slugified field"""
    return slugify(header_field, separator='_', max_length=250)
