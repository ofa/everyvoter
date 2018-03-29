"""Test utils.py in the location app"""
import json
import os

from django.core.exceptions import ValidationError
from django.test import TestCase
from mock import Mock, patch
from geocodio.exceptions import GeocodioDataError

from location import utils
from location.models import GeoLookup


class GeocodeAddressTest(TestCase):
    """Test for the address geocoder"""
    def setUp(self):
        """Setup the test"""
        self.geocoder_patch = patch('location.utils.GeocodioClient')
        self.addCleanup(self.geocoder_patch.stop)
        self.mock_geocode_client = self.geocoder_patch.start()

        path = os.path.dirname(os.path.abspath(__file__))

        canada_file = os.path.join(
            path, 'json/geocodio_canada.json')
        with open(canada_file) as json_file:
            self.canada = json.loads(json_file.read())

        illinois_file = os.path.join(
            path, 'json/geocodio_illinois.json')
        with open(illinois_file) as json_file:
            self.illinois = json.loads(json_file.read())

        no_results_file = os.path.join(
            path, 'json/geocodio_noresults.json')
        with open(no_results_file) as json_file:
            self.no_results = json.loads(json_file.read())

        puerto_rico_file = os.path.join(
            path, 'json/geocodio_puerto_rico.json')
        with open(puerto_rico_file) as json_file:
            self.puerto_rico = json.loads(json_file.read())

    def test_previously_tested(self):
        """Test an address previously geocoded"""
        new_lookup = GeoLookup(
            lookup='Test Address', response=self.illinois)
        new_lookup.save()

        created, lookup_object = utils.geocode_address('Test Address')

        self.assertEqual(lookup_object, new_lookup)
        self.assertFalse(created)

        self.assertFalse(self.mock_geocode_client.called)

    def test_valid(self):
        """Test a fully valid address that does not already exist"""
        test_address = '1060 W Addison St, Chicago, IL 60613'

        mock_geocoder = Mock()
        mock_geocoder.geocode.return_value = self.illinois

        self.mock_geocode_client.return_value = mock_geocoder

        created, lookup_object = utils.geocode_address(test_address)

        mock_geocoder.geocode.assert_called_once_with(
            test_address,
            fields=['cd116', 'stateleg', 'timezone'])

        self.assertTrue(created)

        self.assertEqual(
            lookup_object.lookup, test_address)
        self.assertEqual(
            lookup_object.response, self.illinois)

    def text_exception(self):
        """Test where Geocodio returns a data exception"""
        test_address = ''

        mock_geocoder = Mock()
        mock_geocoder.geocode.side_effect = GeocodioDataError(
            u'Could not geocode address. When using address components, '
            'postal_code or city has to be present.')

        self.mock_geocode_client.return_value = mock_geocoder

        with self.assertRaises(ValidationError) as context:
            utils.geocode_address(test_address)

        self.assertEqual(
            context.exception.message,
            u'Could not geocode address. When using address components, '
            'postal_code or city has to be present.')
        self.assertEqual(type(context.exception), ValidationError)

    def test_no_result(self):
        """Test a a request with no address"""
        test_address = '00009'

        mock_geocoder = Mock()
        mock_geocoder.geocode.return_value = self.no_results

        self.mock_geocode_client.return_value = mock_geocoder

        with self.assertRaises(ValidationError) as context:
            utils.geocode_address(test_address)

        self.assertEqual(
            context.exception.message,
            'Address could not be found. Try a valid zipcode or state.')
        self.assertEqual(type(context.exception), ValidationError)

        mock_geocoder.geocode.assert_called_once_with(
            test_address,
            fields=['cd116', 'stateleg', 'timezone'])

        self.assertTrue(GeoLookup.objects.filter(
            lookup=test_address, response=self.no_results).exists())

    def test_non_us(self):
        """Test an address outside the USA"""
        test_address = '100 Queen St W, Toronto, ON'

        mock_geocoder = Mock()
        mock_geocoder.geocode.return_value = self.canada

        self.mock_geocode_client.return_value = mock_geocoder

        with self.assertRaises(ValidationError) as context:
            utils.geocode_address(test_address)

        self.assertEqual(context.exception.message, 'Not a US Address')
        self.assertEqual(type(context.exception), ValidationError)

        mock_geocoder.geocode.assert_called_once_with(
            test_address,
            fields=['cd116', 'stateleg', 'timezone'])

        self.assertTrue(GeoLookup.objects.filter(
            lookup=test_address, response=self.canada).exists())

    def test_non_state(self):
        """Test a US address from a territory"""
        test_address = '605 Cll Cuevillas, San Juan, PR 00907'

        mock_geocoder = Mock()
        mock_geocoder.geocode.return_value = self.puerto_rico

        self.mock_geocode_client.return_value = mock_geocoder

        with self.assertRaises(ValidationError) as context:
            utils.geocode_address(test_address)

        self.assertEqual(
            context.exception.message, 'Not a supported US state (or DC)')
        self.assertEqual(type(context.exception), ValidationError)

        mock_geocoder.geocode.assert_called_once_with(
            test_address,
            fields=['cd116', 'stateleg', 'timezone'])

        self.assertTrue(GeoLookup.objects.filter(
            lookup=test_address, response=self.puerto_rico).exists())


class GetLocationTest(TestCase):
    """Test for the address geocoder"""
    def setUp(self):
        """Setup the test"""
        self.geocode_patch = patch('location.utils.geocode_address')
        self.addCleanup(self.geocode_patch.stop)
        self.mock_geocode = self.geocode_patch.start()

        path = os.path.dirname(os.path.abspath(__file__))

        illinois_file = os.path.join(
            path, 'json/geocodio_illinois.json')
        with open(illinois_file) as json_file:
            self.illinois = json.loads(json_file.read())

    def test_valid(self):
        """Test a valid request"""
        geolookup = GeoLookup.objects.create(
            lookup='1060 W Addison St, Chicago, IL 60613',
            response=self.illinois)

        self.mock_geocode.return_value = (True, geolookup)

        location = utils.get_location(
            '1060 W Addison St, Chicago, IL 60613')

        self.assertIn(location, geolookup.location_set.all())
        self.assertIn(geolookup, location.lookups.all())
