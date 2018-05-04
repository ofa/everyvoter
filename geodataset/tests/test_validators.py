"""Test geodataset forms"""
import os

from django.core.exceptions import ValidationError
from django.test import TestCase
from mock import Mock

from geodataset.validators import validate_geodataset_upload


def generate_filefield(filename):
    """Generate a mock filefield"""
    path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(
        path, 'data/{}'.format(filename))

    mock_filefield = Mock()
    mock_filefield.name = filename
    mock_filefield.temporary_file_path.return_value = filepath

    return mock_filefield


class TestCSVValdiator(TestCase):
    """Test the geodataset validator"""

    def test_valid(self):
        """Test a fully valid file raises no exception and returns nothing"""
        mock_filefield = generate_filefield('valid_csv.csv')

        self.assertIsNone(validate_geodataset_upload(mock_filefield))

    def test_not_csv_sniffer_pass(self):
        """Test uploading a non-CSV file that passes python's sniffer

        It seems like some excel docs will pass python's CSV sniffer. This
        """
        mock_filefield = generate_filefield('binary_file.xlsx.csv')

        with self.assertRaisesRegexp(
            ValidationError,
            'Error processing file. File may not be a valid CSV.'):
            validate_geodataset_upload(mock_filefield)

    def test_bad_extension(self):
        """Test a file with an improper extension"""
        mock_filefield = generate_filefield('wrong_extension.zip')

        with self.assertRaisesRegexp(
            ValidationError,
            'Improper file extension ".zip". You must upload a CSV'):
            validate_geodataset_upload(mock_filefield)

    def test_no_rows(self):
        """Test a csv file with a valid header but no rows"""
        mock_filefield = generate_filefield('no_rows.csv')

        with self.assertRaisesRegexp(
            ValidationError,
            'File must have at least one entry.'):
            validate_geodataset_upload(mock_filefield)

    def test_bad_header(self):
        """Test a file without an ocd_id header"""
        mock_filefield = generate_filefield('bad_ocdid_header_csv.csv')

        with self.assertRaisesRegexp(
            ValidationError, 'First column must be named \'ocd_id\''):
            validate_geodataset_upload(mock_filefield)

    def test_empty_header(self):
        """Test a file with an empty header"""
        mock_filefield = generate_filefield('empty_header_csv.csv')

        with self.assertRaisesRegexp(
            ValidationError, 'Column 3 header is empty or decodes to empty'):
            validate_geodataset_upload(mock_filefield)

    def test_duplicate_header(self):
        """Test a file with a header having duplicate values"""
        mock_filefield = generate_filefield('duplicate_header_csv.csv')

        with self.assertRaisesRegexp(
            ValidationError, 'One or more duplicate headers. field1'):
            validate_geodataset_upload(mock_filefield)

    def test_bad_row(self):
        """Test a file where one of the rows does not have a valid OCD ID"""
        mock_filefield = generate_filefield('bad_row_csv.csv')

        with self.assertRaisesRegexp(
            ValidationError, 'One or more OCD IDs not found. First found: Row: '
                             '3 ID: BAD ROW NON OCD ID'):
            validate_geodataset_upload(mock_filefield)
