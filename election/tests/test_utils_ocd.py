"""Test Open Civic Data utils"""
import json
import os

from django.test import TestCase

from election import utils


class GeocodioOCDIDTest(TestCase):
    def setUp(self):
        """Setup test"""
        path = os.path.dirname(os.path.abspath(__file__))

        illinois_full_file = os.path.join(
            path, 'json/geocodio_full_illinois.json')
        with open(illinois_full_file) as json_file:
            self.full_illinois = json.loads(json_file.read())

        massachusetts_full_file = os.path.join(
            path, 'json/geocodio_full_massachusetts.json')
        with open(massachusetts_full_file) as json_file:
            self.full_massachusetts = json.loads(json_file.read())

        dc_full_file = os.path.join(
            path, 'json/geocodio_full_dc.json')
        with open(dc_full_file) as json_file:
            self.full_dc = json.loads(json_file.read())

        illinois_multi_zip_file = os.path.join(
            path, 'json/geocodio_zip_multi_illinois.json')
        with open(illinois_multi_zip_file) as json_file:
            self.zip_multi_illinois = json.loads(json_file.read())

        illinois_single_zip_file = os.path.join(
            path, 'json/geocodio_zip_single_illinois.json')
        with open(illinois_single_zip_file) as json_file:
            self.zip_single_illinois = json.loads(json_file.read())


    def test_full_address(self):
        """Test requests that are full addresses"""

        # Illinois (which has a really straightforward)
        self.assertEqual(
            utils.geocodio_ocd_ids(self.full_illinois),
            ['ocd-division/country:us/state:il',
             'ocd-division/country:us/state:il/cd:5',
             'ocd-division/country:us/state:il/sldl:12',
             'ocd-division/country:us/state:il/sldu:6'])

        # Massachusetts (which has weird legislative districts)
        self.assertEqual(
            utils.geocodio_ocd_ids(self.full_massachusetts),
            ['ocd-division/country:us/state:ma',
             'ocd-division/country:us/state:ma/cd:4',
             'ocd-division/country:us/state:ma/sldl:1st_bristol',
             'ocd-division/country:us/state:ma/sldu:bristol_and_norfolk'])

        # DC (which has a non-standard state OCD ID)
        self.assertEqual(
            utils.geocodio_ocd_ids(self.full_dc),
            ['ocd-division/country:us/district:dc',
             'ocd-division/country:us/district:dc/ward:2'])

    def test_zip(self):
        """Test where all is provided is a zipcode"""

        # Zipcode 60657 has multiple congressional districts, it should only
        # have the state.
        self.assertEqual(
            utils.geocodio_ocd_ids(self.zip_multi_illinois),
            ['ocd-division/country:us/state:il'])

        # Zipcode 60602 is based entirely in IL-7, it should have the CD but no
        # state leg data
        self.assertEqual(
            utils.geocodio_ocd_ids(self.zip_single_illinois),
            ['ocd-division/country:us/state:il',
             'ocd-division/country:us/state:il/cd:7'])
