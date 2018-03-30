"""Models related to different organizations"""
from django.core.cache import cache
from django.db import models

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
        help_text='Domain to attach all links to', related_name='primary_domain')
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


class Domain(TimestampModel, OrganizationMixin):
    """Domain that app is hosted at"""
    hostname = models.CharField('Hostname', max_length=100, unique=True)

    class Meta(object):
        """Meta options for domain"""
        verbose_name = "Domain"
        verbose_name_plural = "Domains"

    def __str__(self):
        """String representation of the domain"""
        return self.hostname

    def save(self, *args, **kwargs):
        """Save the domain"""
        # Only one domain can be "default" per organization
        if self.is_primary:
            # select all other default items
            queryset = Domain.objects.filter(
                organization=self.organization, is_primary=True)
            # except self (if self already exists)
            if self.pk:
                queryset = queryset.exclude(pk=self.pk)
            # and deactive them
            queryset.update(is_primary=False)

        return super(Domain, self).save(*args, **kwargs)
