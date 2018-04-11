"""Location-related Models"""
from django.db import models
from django.contrib.postgres.fields import JSONField

from kennedy_common.utils.models import TimestampModel


class UserLocation(TimestampModel):
    """A specific location for a user"""
    user = models.ForeignKey('accounts.User')
    location = models.ForeignKey('Location')

    class Meta(object):
        """Meta options for the UserLocation Model"""
        verbose_name = "User Location"
        verbose_name_plural = "User Locations"


class Location(TimestampModel):
    """Location of one or more users"""
    formatted_address = models.CharField('Address', max_length=255)
    state = models.ForeignKey('election.State', db_index=True)
    districts = models.ManyToManyField('election.LegislativeDistrict')
    lookups = models.ManyToManyField('GeoLookup')

    class Meta(object):
        """Meta options for the Location model"""
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __unicode__(self):
        """Unicode representation of the Location"""
        return self.formatted_address


class GeoLookup(TimestampModel):
    """Lookup on Geocod.io"""
    lookup = models.CharField(
        'Lookup', help_text="Address provided by user", max_length=255)
    response = JSONField()

    class Meta(object):
        """Meta options for the GeoLookup object"""
        verbose_name = "Geocoding Lookup"
        verbose_name_plural = "Geocoding Lookups"

    def __unicode__(self):
        """Unicode representation of the lookup"""
        return self.lookup
