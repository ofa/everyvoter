"""Models for the block functionality"""
from django.db import models

from branding.mixins import OrganizationMixin
from rendering.validators import validate_template
from everyvoter_common.utils.models import TimestampModel, UUIDModel


class Block(TimestampModel, UUIDModel, OrganizationMixin):
    """Block of content"""
    name = models.CharField('Block Name', max_length=50)
    code = models.TextField('HTML Code', validators=[validate_template])
    tag = models.ForeignKey(
        'blocks.BlockTag', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta(object):
        """Meta options for BLock"""
        verbose_name = "Block"
        verbose_name_plural = "Blocks"

    def __unicode__(self):
        """Unicode representation of the block"""
        return self.name


class BlockTag(TimestampModel, UUIDModel, OrganizationMixin):
    """Tag used for blocks"""
    name = models.CharField('Blog Tag Name', max_length=50)

    class Meta(object):
        """Meta options for Blog Tag"""
        verbose_name = "Block Tag"
        verbose_name_plural = "Block Tags"

    def __unicode__(self):
        """Unicode representation of the block"""
        return self.name


class BlockManyToMany(TimestampModel):
    """Abstract M2M join model between an upcoming or past email and a block"""
    priority = models.IntegerField(default=0)
    block = models.ForeignKey('blocks.Block')

    class Meta(object):
        """Meta options for abstract model"""
        abstract = True
        ordering = ['priority']


class TemplateBlocks(BlockManyToMany):
    """Many to many between upcoming emails and blocks"""
    template = models.ForeignKey('mailer.MailingTemplate')

    class Meta(object):
        """Meta options for TemplateBlocks"""
        verbose_name = "Template Blocks"
        verbose_name_plural = "Template Blocks"


class MailingBlocks(BlockManyToMany):
    """Many to many between past emails and blocks"""
    mailing = models.ForeignKey('mailer.Mailing')

    class Meta(object):
        """Meta options for MailingBlocks"""
        verbose_name = "Mailing Blocks"
        verbose_name_plural = "Mailing Blocks"
