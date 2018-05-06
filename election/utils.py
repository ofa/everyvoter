"""Utilities for Elections"""
import uuid

from election.choices import STATES
from election.geocodio_ocdids import (
    GEOCODIO_OCDIDS_HOUSE, GEOCODIO_OCDIDS_SENATE
)


def sync_elections(election_model=None, orgelection_model=None,
                   organization_model=None):
    """Sync Elections

    Utility that creates OrganizationElections for all orgs for an Election

    Args:
        election_model: optional model for Election (allows us to use this in
                        migrations) (default: {None})
        orgelection_model: optional model for orgelection (for migrations)
                           (default: {None})
        organization_model: optional model for organization (for migrations)
                            (default: {None})

    """

    if not election_model:
        from election.models import Election as election_model

    if not organization_model:
        from branding.models import Organization as organization_model

    if not orgelection_model:
        from election.models import OrganizationElection as orgelection_model

    new_orgelections = []

    for organization in organization_model.objects.all():
        existing_orgelections = orgelection_model.objects.filter(
            organization=organization).values('election_id')
        missing_elections = election_model.objects.exclude(
            id__in=existing_orgelections)

        email_wrapper = organization.emailwrapper_set.get(default=True)

        for election in missing_elections:
            new_orgelections.append(orgelection_model(
                uuid=uuid.uuid4(),
                organization=organization,
                election=election,
                email_wrapper=email_wrapper
            ))

    orgelection_model.objects.bulk_create(new_orgelections)


def state_ocd_id(state):
    """Get the OCD ID of the state

    Returns the state OCD ID, which can be used both alone and as a prefix

    Args:
        state: state CD (uppercase)

    Returns:
        OCD ID of the state
        string
    """
    if state == 'DC':
        state_id = 'ocd-division/country:us/district:dc'
    else:
        state_id = 'ocd-division/country:us/state:{state}'.format(
            state=state.lower())
    return state_id


def cd_ocd_id(state, district_number):
    """Return the OCD ID for a congressional district

    Note: If the state/district only has 1 district this will return an empty
    list

    Args:
        state: state cd
        district_number: congressional district number
    """
    # States with only 1 rep return a 0 from geocodio but need a "1" for the
    # OCD ID
    if district_number == 0:
        district_number = 1

    # DC does not have a congressional district
    if state in ['DC']:
        return []

    return ['{state_id}/cd:{cd}'.format(
        state_id=state_ocd_id(state), cd=district_number)]


def state_leg_ocd_id(level, state, district_number):
    """Return the OCD ID for a state legislative result

    Args:
        level: state leg level (i.e. 'house' or 'state')
        state: state cd
        district_number: number of the distrct

    Returns:
        One or more OCD ID in a list
        list
    """
    if level == 'house':
        ocdid_exceptions = GEOCODIO_OCDIDS_HOUSE
        prefix = 'sldl'
    else:
        ocdid_exceptions = GEOCODIO_OCDIDS_SENATE
        prefix = 'sldu'

    if state in ocdid_exceptions.keys():
        return ocdid_exceptions[state].get(district_number, [])

    return ['{state_id}/{prefix}:{number}'.format(
        state_id=state_ocd_id(state), prefix=prefix,
        number=district_number)]


def geocodio_ocd_ids(result):
    """Get the Open Civic Data IDs for a Geocod.io Response

    This will return the OCD IDs for a given Geocod.io response.

    Args:
        result: selected result from geocod.io

    Returns:
        OCD IDs associated with the Geocod.io response
        list
    """

    state = result['address_components'].get('state')

    # If the state is not in our list of supported states, return nothing
    if state not in dict(STATES).keys():
        return []

    ids = [state_ocd_id(state)]

    fields = result.get('fields', {})


    # Congressional districts
    congressional_districts = fields.get(
        'congressional_districts', [])
    congressional_district = congressional_districts[0]

    # Some zipcodes will have multiple districts. We only want to return an ocd
    # id for results where we're positive we're looking at the right district
    if congressional_district.get('proportion', 0) == 1:
        federal_house_district_number = congressional_district.get(
            'district_number', 0)
        ids = ids + cd_ocd_id(state, federal_house_district_number)


    # If the result is just a place or a state (i.e. a zipcode, city, or state)
    # bail out here, as there is no guarantee our result will be accurate
    # enough to reliably get state legislative district data
    if result.get('accuracy_type') in ['state', 'place']:
        return ids


    # State Legislature
    state_leg = fields.get('state_legislative_districts', {})

    state_house = state_leg.get('house')
    if state_house:
        state_house_number = state_house.get('district_number')
        ids = ids + state_leg_ocd_id('house', state, state_house_number)

    state_senate = state_leg.get('senate')
    if state_senate:
        state_senate_number = state_senate.get('district_number')
        ids = ids + state_leg_ocd_id('senate', state, state_senate_number)

    return ids
