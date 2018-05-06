"""Validators for geodataset app"""
import csv
import os

from django.core.exceptions import ValidationError
from unicodecsv import DictReader

from election.models import LegislativeDistrict
from geodataset.utils import slugify_header


def validate_geodataset_upload(uploaded_file):
    """Validate an uploaded file containing geodataset data

    Because we're using exclusively `TemporaryFileUploadHandler`s we'll always
    have a local file we can open and inspect.
    """

    # Check the extension. We do this instead of calling the
    # FileExtensionValidator because we don't want a bad extension to go any
    # further in this validator.
    extension = os.path.splitext(uploaded_file.name)[-1].lower()
    if extension != '.csv':
        raise ValidationError(
            'Improper file extension "{}". You must upload a CSV'.format(
                extension))

    # Validate the file by opening and inspecting it.
    with open(uploaded_file.temporary_file_path(), 'rb') as file_obj:
        # Start the reader. Handle bad CSVs
        try:
            reader = DictReader(file_obj, encoding='utf-8-sig')
        except csv.Error:
            raise ValidationError(
                'Error processing file. File may not be a valid CSV.')

        if reader.fieldnames[0] != 'ocd_id':
            raise ValidationError('First column must be named \'ocd_id\'')

        seen = []
        for i, fieldname in enumerate(reader.fieldnames):
            clean_field = slugify_header(fieldname)
            if clean_field == '':
                raise ValidationError(
                    u'Column {} header is empty or decodes to empty'.format(i))
            if clean_field in seen:
                raise ValidationError(
                    u'One or more duplicate headers. {}'.format(clean_field))
            seen.append(clean_field)

        ocd_ids = []
        for row in reader:
            ocd_ids.append(row['ocd_id'])

    if not ocd_ids:
        raise ValidationError('File must have at least one entry.')

    # Get all the OCD IDs that match in the database, turn it into a list
    # we can compare to.
    db_ocd_ids = LegislativeDistrict.objects.filter(
        ocd_id__in=list(set(ocd_ids))).values_list('ocd_id', flat=True)

    # Iterate through user-provided OCD IDs and see if they're in the list
    # that came from the database. If they're not, return an error on the
    # first instance.
    for i, ocd_id in enumerate(ocd_ids):
        if ocd_id not in db_ocd_ids:
            raise ValidationError(u'One or more OCD IDs not found. First '
                                  'found: Row: {row} ID: {id}'.format(
                                      row=(i + 2), id=ocd_id))
