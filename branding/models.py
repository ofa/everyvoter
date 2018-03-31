"""Models related to different organizations"""
from django.core.cache import cache
from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from branding.mixins import OrganizationMixin
from branding.utils import org_domain_cache_key
from kennedy_common.utils.models import TimestampModel


class Organization(TimestampModel):
    """Organization holding an OFAVotes Account"""
    name = models.CharField('Name', max_length=50)
    homepage = models.URLField('Homepage')
    platform_name = models.CharField('Platform Name', max_length=50)
    primary_domain = models.ForeignKey(
        'Domain', verbose_name='Primary Domain',
        help_text='Domain to attach all links to',
        related_name='primary_domain', null=True, default=False)
    elections = models.ManyToManyField(
        'election.Election', through='election.OrganizationElection')

    class Meta(object):
        """Meta options for Organization"""
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self):
        """String representation of the organization"""
        return self.name

    def save(self, *args, **kwargs):
        """Save the organization"""
        for domain in self.domain_set.all():
            cache.delete(org_domain_cache_key(domain.hostname))
        return super(Organization, self).save(self, *args, **kwargs)

    @cached_property
    def url(self):
        """Formatted URL of the domain"""
        if self.primary_domain:
            host = self.primary_domain.hostname
        else:
            host = Domain.objects.filter(organization=self).first()

        if settings.DEBUG:
            return 'http://{host}'.format(host=host)

        return 'https://{host}'.format(host=host)


class Domain(TimestampModel):
    """Domain that app is hosted at"""
    organization = models.ForeignKey(
        Organization, db_index=True)
    hostname = models.CharField('Hostname', max_length=100, unique=True)

    class Meta(object):
        """Meta options for domain"""
        verbose_name = "Domain"
        verbose_name_plural = "Domains"

    def __str__(self):
        """String representation of the domain"""
        return self.hostname

