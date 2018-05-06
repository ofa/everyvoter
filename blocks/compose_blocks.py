"""Compose blocks"""
from blocks.models import Block
from geodataset.models import FieldValue


def get_district_blocks(districts):
    """Get the block entries one or more district(s) could ever see"""
    district_blocks = Block.objects.filter(
        geodataset__entry__district_id__in=districts.values('pk')
        ).extra(select={'entry_id': '"geodataset_entry"."id"'}).order_by(
            '-weight')

    return district_blocks


def get_data(entry_ids):
    """Get a dictionary of all the values for the email"""
    raw_values = FieldValue.objects.filter(
        entry_id__in=entry_ids).select_related('field')

    result = {}
    for value in raw_values:
        key = "entry{}".format(value.entry_id)
        if key not in result:
            result[key] = {}
        result[key][value.field.name] = value.value

    return result


def compose_blocks(districts, email=None, block=None):
    """Compose the source and context for the blocks section"""
    possible_blocks = get_district_blocks(districts)

    if email:
        final_blocks = possible_blocks.filter(
            id__in=email.blocks.all().values('pk'))
    else:
        final_blocks = possible_blocks.filter(id=block.pk)

    final_blocks_list = list(final_blocks)
    entry_ids = [x.entry_id for x in final_blocks_list]
    context_data = get_data(entry_ids)

    final_source = []
    for block in final_blocks_list:
        final_source.append("{{% with dataset=entry{entry_id} %}}{block}"
                            "{{% endwith %}}".format(
                                entry_id=block.entry_id, block=block.code))

    return (context_data, '\n'.join(final_source))
