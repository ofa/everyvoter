"""Branding-Related Middleware"""
from django.core.cache import cache
from django.conf import settings
from django.http import Http404
from django.http.request import split_domain_port

from branding.models import Domain
from branding.utils import org_domain_cache_key


class BrandingMiddleware(object):
    """Middleware to insert the current branding"""

    def __init__(self, get_response):
        """Initialize the Middleware"""
        self.get_response = get_response


    def __call__(self, request):
        """Process a request"""

        domain_name = split_domain_port(request.get_host())[0]
        cache_key = org_domain_cache_key(domain_name)

        organization = cache.get(cache_key)

        if not organization:
            domain_queryset = Domain.objects.select_related(
                'organization', 'organization__primary_domain')

            try:
                domain = domain_queryset.get(hostname=domain_name)
            except Domain.DoesNotExist:
                if settings.DEBUG:
                    domain = domain_queryset.first()
                else:
                    raise Http404

            organization = domain.organization

            if not settings.DEBUG:
                cache.set(cache_key, organization)

        request.organization = organization

        return self.get_response(request)
