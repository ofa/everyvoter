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

    class Meta(object):
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
        verbose_name = "Domain"
        verbose_name_plural = "Domains"

    def __str__(self):
        """String representation of the domain"""
        return self.hostname
