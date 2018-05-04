"""Test for geodataset models"""
from django.test import TestCase
from model_mommy import mommy

from geodataset import models

class TestEntry(TestCase):
    """Test the Entry Model"""
    def test_data(self):
        """Test the data method of the Entry model"""
        entry = mommy.make('geodataset.Entry', district_id=1)
        cool_field = mommy.make(
            models.Field, geodataset=entry.geodataset, name='cool')
        nifty_field = mommy.make(
            models.Field, geodataset=entry.geodataset, name='nifty')

        mommy.make(models.FieldValue, field=cool_field, entry=entry,
                   value='Cool Value!')
        mommy.make(models.FieldValue, field=nifty_field, entry=entry,
                   value='Nifty Value!')

        self.assertDictEqual(
            entry.data, {'cool': 'Cool Value!', 'nifty': 'Nifty Value!'})
