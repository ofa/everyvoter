"""Utilities for location app"""
from django.conf import settings

from django.core.exceptions import ValidationError
from geocodio import GeocodioClient
from geocodio.exceptions import GeocodioDataError

from election.choices import STATES
from election.models import LegislativeDistrict
from election.utils import geocodio_ocd_ids
from location.models import GeoLookup, Location


def geocode_address(address):
    """Geocode an address

    Take an address, send it to Geocode.io, and return a result for use in the
    app. Ensure that it's a US address in a state (or DC) we support.

    Args:
        address: unicode address

    Returns:
        (Created Boolean, GeoLookup object)
        Tuple
    """
    # If we've looked up this address before, use the result we got
    lookup_object = GeoLookup.objects.filter(lookup=address[:255]).first()
    if lookup_object:
        geocode_response = lookup_object.response
        created = False
    else:
        geocodio_client = GeocodioClient(settings.GEOCODIO_KEY)

        # If the address is bad or not detailed enough, this will raise a
        # GeocodioDataError. We should catch that and pass it up as a
        # validation error like we do with all other validation exceptions
        try:
            geocode_response = geocodio_client.geocode(
                address, fields=['cd116', 'stateleg', 'timezone'])
        except GeocodioDataError as error:
            raise ValidationError(unicode(error))

        # Save the response as a GeoLookup to save us from hitting the geocode
        # service for the same addresses over-and-over (this is most helpful
        # for zipcodes)
        lookup_object = GeoLookup(
            lookup=address[:255],
            response=geocode_response)
        lookup_object.save()
        created = True

    # Sometimes Geocode.io can parse the address but cannot find it on a map.
    # In those cases, return a ValidationError and let some other method handle
    # it.
    if len(geocode_response.get('results')) == 0:
        raise ValidationError(
            'Address could not be found. Try a valid zipcode or state.')

    result = geocode_response['results'][0]
    address_components = result['address_components']

    # Geocod.io supports some other countries (like Canada) but we don't.
    if address_components.get('country') != 'US':
        raise ValidationError('Not a US Address')

    # We only support some states in the app. If you try to import someone from
    # a territory reject the input.
    if address_components.get('state') not in dict(STATES).keys():
        raise ValidationError('Not a supported US state (or DC)')

    return (created, lookup_object)


def get_location(address):
    """Get a Location for an address

    Get a fully fleshed out Location for an address. If a Location for an
    address already exists, return that location. Otherwise, create a new one.

    Args:
        address: Unfiltered address
    """
    # Step 1 is get a clean geocoded object
    geocode_created, geocode_object = geocode_address(address)

    # Thanks to checking done in geocode_address(), we know there is at least
    # one result. Use the first one.
    geocode_result = geocode_object.response['results'][0]

    location, location_created = Location.objects.get_or_create(
        formatted_address=geocode_result['formatted_address'],
        state_id=geocode_result['address_components'].get('state'))

    # If the geocode object is new or the location is new, add it to the M2M
    # field.
    if geocode_created or location_created:
        location.lookups.add(geocode_object)

    # Get the electoral districts for this address and attach them to the
    # Location.
    if location_created:
        ocd_ids = geocodio_ocd_ids(geocode_result)
        districts = LegislativeDistrict.objects.filter(ocd_id__in=ocd_ids)
        location.districts.set(districts)

    return location
