"""Models for Geodataset"""
from django.db import models
from django.utils.functional import cached_property

from branding.mixins import OrganizationMixin
from everyvoter_common.utils.models import TimestampModel, UUIDModel


class GeoDataset(TimestampModel, UUIDModel, OrganizationMixin):
    """Dataset that contains blocks, targets, and data"""
    name = models.CharField('Name', max_length=50)
    categories = models.ManyToManyField(
        'geodataset.GeoDatasetCategory', blank=True)

    class Meta(object):
        """Meta options for Geodataset model"""
        verbose_name = "GeoDataset"
        verbose_name_plural = "GeoDatasets"

    def __unicode__(self):
        """String representation of model"""
        return self.name


class Entry(TimestampModel, UUIDModel):
    """Entry of data in a geodataset"""
    geodataset = models.ForeignKey(GeoDataset)
    district = models.ForeignKey('election.LegislativeDistrict')
    fields = models.ManyToManyField(
        'geodataset.Field', through='geodataset.FieldValue', blank=True)

    class Meta(object):
        """Meta options for GeoDatasetRow model"""
        verbose_name = "Geo Dataset Entry"
        verbose_name_plural = "Geo Dataset Entry"

    def __unicode__(self):
        """Unicode representation of the entry"""
        return u'{geodataset} {district}'.format(
            geodataset=self.geodataset.name, district=self.district.ocd_id)

    @cached_property
    def data(self):
        """Data for the entry in dictionary format"""
        return dict(self.fields.values_list(
            'name', 'fieldvalue__value'))



class Field(TimestampModel, UUIDModel):
    """Field in a geodataset"""
    name = models.CharField('Name', max_length=255)
    geodataset = models.ForeignKey(GeoDataset)

    class Meta(object):
        """Meta options for Field model"""
        verbose_name = "Field"
        verbose_name_plural = "Fields"

    def __unicode__(self):
        """Unicode representation of the field"""
        return self.name


class FieldValue(TimestampModel, UUIDModel):
    """Value of a field in an entry of a geodataset"""
    field = models.ForeignKey(Field)
    entry = models.ForeignKey(Entry)
    value = models.TextField()


class GeoDatasetCategory(TimestampModel, UUIDModel, OrganizationMixin):
    """Category used for GeoDatasets"""
    name = models.CharField('GeoDataset Category Name', max_length=50)

    class Meta(object):
        """Meta options for Blog Tag"""
        verbose_name = "GeoDataset Category"
        verbose_name_plural = "GeoDataset Categories"

    def __unicode__(self):
        """Unicode representation of the category"""
        return self.name
