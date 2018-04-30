"""Models for Geodataset"""
from django.db import models

from branding.mixins import OrganizationMixin
from rendering.validators import validate_template
from everyvoter_common.utils.models import TimestampModel, UUIDModel


class GeoDataset(TimestampModel, UUIDModel, OrganizationMixin):
    """Dataset that contains blocks, targets, and data"""
    name = models.CharField('Name', max_length=50)

    class Meta(object):
        """Meta options for Geodataset model"""
        verbose_name = "GeoDataset"
        verbose_name_plural = "GeoDatasets"

    def __str__(self):
        pass


class Row(TimestampModel, UUIDModel):
    """Row of data in a geodataset"""
    geodataset = models.ForeignKey(GeoDataset)
    district = models.ForeignKey('election.LegislativeDistrict')

    class Meta(object):
        """Meta options for GeoDatasetRow model"""
        verbose_name = "Geo Dataset Row"
        verbose_name_plural = "Geo Dataset Rows"


class Field(TimestampModel, UUIDModel):
    """Field in a row of a geodataset"""
    row = models.ForeignKey(Row)
    name = models.CharField('Name', max_length=255)
    value = models.TextField('Value')

    class Meta(object):
        """Meta options for RowField model"""
        verbose_name = "Field"
        verbose_name_plural = "Fields"
