"""Models for the block functionality"""
from django.db import models

from branding.mixins import OrganizationMixin
from rendering.validators import validate_template
from everyvoter_common.utils.models import TimestampModel, UUIDModel
from everyvoter_common.utils.soft_delete import SoftDeleteModel, ActiveManager


class BlockManager(ActiveManager):
    """Manager for blocks"""
    def get_queryset(self):
        queryset = super(BlockManager, self).get_queryset()
        queryset = queryset.exclude(geodataset__deleted=True)
        return queryset



class Block(SoftDeleteModel, TimestampModel, UUIDModel, OrganizationMixin):
    """Block of content"""
    name = models.CharField('Block Name', max_length=50)
    code = models.TextField('HTML Code', validators=[validate_template])
    categories = models.ManyToManyField(
        'blocks.BlockCategory', blank=True)
    weight = models.IntegerField('Weight', default=50)
    geodataset = models.ForeignKey('geodataset.GeoDataset')

    objects = BlockManager()

    class Meta(object):
        """Meta options for BLock"""
        verbose_name = "Block"
        verbose_name_plural = "Blocks"

    def __unicode__(self):
        """Unicode representation of the block"""
        return self.name


class BlockCategory(TimestampModel, UUIDModel, OrganizationMixin):
    """Category used for blocks"""
    name = models.CharField('Blog Category Name', max_length=50)

    class Meta(object):
        """Meta options for Blog Tag"""
        verbose_name = "Block Category"
        verbose_name_plural = "Block Categories"

    def __unicode__(self):
        """Unicode representation of the block"""
        return self.name
