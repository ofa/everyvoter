"""Models for the block functionality"""
from django.db import models

from branding.mixins import OrganizationMixin
from rendering.validators import validate_template
from everyvoter_common.utils.models import TimestampModel, UUIDModel


class Block(TimestampModel, UUIDModel, OrganizationMixin):
    """Block of content"""
    name = models.CharField('Block Name', max_length=50)
    code = models.TextField('HTML Code', validators=[validate_template])
    categories = models.ManyToManyField(
        'blocks.BlockCategory', blank=True)
    weight = models.IntegerField('Weight', default=50)
    geodataset = models.ForeignKey('geodataset.GeoDataset')

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


class EmailBlocks(TimestampModel):
    """Abstract M2M join model between an upcoming or past email and a block"""
    block = models.ForeignKey('blocks.Block')
    email = models.ForeignKey('mailer.Email')
