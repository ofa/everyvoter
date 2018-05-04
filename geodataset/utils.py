"""Utilities for Geodataset"""
from collections import OrderedDict
from slugify import slugify
import unicodecsv

from geodataset.models import Entry, Field, FieldValue
from election.models import LegislativeDistrict


def slugify_header(header_field):
    """Take a header field and return the clean ASCII slugified field"""
    return slugify(header_field, separator='_', max_length=250)


def empty_existing_geodataset(geodataset):
    """Wipe existing Entries, Fields and FieldValues for a GeoDataset

    Since queryset.delete() does a SELECT before deleting in order to support
    signals and cascading deletes (such as the M2M) use _raw_delete()
    to use the DB to bulk delete per recommendation at
    http://www.nickang.com/fastest-delete-django/ and
    https://stackoverflow.com/questions/4867852/
    Much faster!
    """
    # pylint: disable=protected-access
    field_values = FieldValue.objects.filter(
        field__geodataset=geodataset)
    field_values._raw_delete(field_values.db)

    entries = Entry.objects.filter(geodataset=geodataset)
    entries._raw_delete(entries.db)

    fields = Field.objects.filter(geodataset=geodataset)
    fields._raw_delete(fields.db)


def read_geodataset_file(filefield):
    """Read a geodataset file defined in a filefield and return useful data

    Take a filefield (retrieved from cleaned_data) and return data, headers,
    and ocd_ids in a tuple.

    Args:
        filefield: the 'file' field from cleaned_data
    """
    with open(filefield.temporary_file_path(), 'rb') as file_obj:
        reader = unicodecsv.reader(file_obj, encoding='utf-8-sig')

        # Load the file into a dictionary
        data = []
        ocd_ids = []
        for row in reader:
            ocd_ids.append(row[0])
            del row[0]
            data.append(row)

        headers = data[0]
        del data[0]
        del ocd_ids[0]

    return (data, headers, ocd_ids)


def create_entries(ocd_ids, geodataset):
    """Create new entries"""
    # Get a dictionary of primary keys for legislative districts
    district_pks = dict(LegislativeDistrict.objects.filter(
        ocd_id__in=list(set(ocd_ids))).values_list('ocd_id', 'id'))

    new_entries = []
    for ocd_id_row_number in range(0, len(ocd_ids)):
        new_entries.append(
            Entry(district_id=district_pks[ocd_ids[ocd_id_row_number]],
                  geodataset=geodataset))

    return Entry.objects.bulk_create(new_entries)


def create_fields(headers, geodataset):
    """Create new fields"""

    new_fields = []
    for field in headers:
        new_fields.append(
            Field(name=slugify_header(field), geodataset=geodataset))

    return Field.objects.bulk_create(new_fields)


def create_values(data, entries_result, fields_result):
    """Create EntryValues"""
    new_values = []
    for row_number in range(0, len(data)):
        row = data[row_number]
        entry = entries_result[row_number]

        # For each field in the row
        for field_number in range(0, len(row)):

            value = row[field_number]
            field = fields_result[field_number]

            new_values.append(
                FieldValue(field=field, entry=entry, value=value))

    return FieldValue.objects.bulk_create(new_values)


def process_geodataset_file(filefield, geodataset, created):
    """Process a geodataset file submission

    Process a file submitted on a geodataset form. This happens after the
    Geodataset object has been created or updated.

    Args:
        filefield: the 'file' field from cleaned_data
        geodataset: the recently created/updated GeoDataset
        created: true/false if the object is being created or not
    """

    data, headers, ocd_ids = read_geodataset_file(filefield)

    # If there are existing entries/fields/values, delete them. Do this as late
    # as possible so if an exception happens above it doesn't delete data.
    if not created:
        empty_existing_geodataset(geodataset)

    entries_result = create_entries(ocd_ids, geodataset)

    fields_result = create_fields(headers, geodataset)

    create_values(data, entries_result, fields_result)


def generate_csv_data(geodataset):
    """Generate a CSV from a geodataset"""
    fields = list(Field.objects.filter(
        geodataset=geodataset).values_list(
            'name', flat=True).order_by('created_at'))
    values = FieldValue.objects.filter(
        entry__geodataset=geodataset).select_related('entry__district',
                                                     'entry__geodataset',
                                                     'field')

    results = OrderedDict()
    for value in values:
        if value.entry.district.ocd_id not in results:
            results[value.entry.district.ocd_id] = {}
        results[value.entry.district.ocd_id][value.field.name] = value.value

    final = []
    for key, value in results.iteritems():
        value['ocd_id'] = key
        final.append(value)

    fields.insert(0, 'ocd_id')

    return (final, fields)
