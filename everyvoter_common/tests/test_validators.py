"""Test kennedy-common field validators"""
from django.core.exceptions import ValidationError
from django.test import TestCase

from everyvoter_common.validators import validate_template


class TestValidateTemplate(TestCase):
    """Test the template valdiator"""
    def test_success(self):
        """Test that a valid template raises no exception"""
        validate_template(
            '{% load static %}{% if x %}{{ yay|default:"hello" }}{% endif %}')

    def test_failure(self):
        """Test a few failures"""
        with self.assertRaises(ValidationError):
            validate_template('{{ hey.first() }}')

        with self.assertRaises(ValidationError):
            validate_template('{% if x %}')

        with self.assertRaises(ValidationError):
            validate_template('{{ hey|defaultcool }}')
