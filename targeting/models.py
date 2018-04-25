"""Target models"""
from django.db import models
from django.contrib.postgres.fields import JSONField

from branding.mixins import OrganizationMixin
from everyvoter_common.utils.models import TimestampModel, UUIDModel


TARGET_TYPES = (
    ('candidate', 'Elected Position'),
    ('ballot', 'Ballot Measure')
)


class Target(OrganizationMixin, UUIDModel, TimestampModel):
    """Electoral Target"""
    name = models.CharField('Name', max_length=50)
    dataset = JSONField('Dataset', null=True, blank=True)
    target_type = models.CharField(
        'Target Type', choices=TARGET_TYPES, max_length=50)
    election = models.ForeignKey('election.Election')
    district = models.ForeignKey('election.LegislativeDistrict')
    blocks = models.ManyToManyField('blocks.Block', blank=True)
    tags = models.ManyToManyField('targeting.TargetTag', blank=True)

    class Meta(object):
        """Target"""
        verbose_name = "Target"
        verbose_name_plural = "Targets"

    def __str__(self):
        return self.name


class TargetTag(OrganizationMixin, UUIDModel, TimestampModel):
    """Tag associated with a target"""
    name = models.CharField('Name', max_length=50)

    def __unicode__(self):
        """Unicode representation of TargetTags"""
        return self.name
