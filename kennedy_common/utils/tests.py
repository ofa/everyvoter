"""Common mixins for tests"""
import os
import json
import uuid

from model_mommy import mommy

from accounts.utils_user import create_user
from branding.models import Organization, Domain
from location.utils import get_location

# pylint: disable=invalid-name
path = os.path.dirname(os.path.abspath(__file__))
illinois_file = os.path.join(
    path, 'data/geocodio_illinois.json')
with open(illinois_file) as json_file:
    illinois_geocode = json.loads(json_file.read())


class KennedyTestMixin(object):
    """Mixin for Kennedy tests"""
    def create_organization(self):
        """Create an organization with the test domain"""
        domain = Domain.objects.get(hostname='testserver')
        return mommy.make('Organization', primary_domain=domain)

    def create_location(self, state_id='IL', address=None):
        """Create a new Location"""
        from mock import patch, Mock
        if not address:
            address = unicode(uuid.uuid4())

        with patch('location.utils.GeocodioClient') as patch:
            mock_geocode_result = Mock()
            mock_geocode_result.geocode.return_value = illinois_geocode
            patch.return_value = mock_geocode_result

            return get_location(address)

    def create_user(self, organization=None, location=None):
        """Create a new user"""
        from mock import patch

        # If no organization is passed in, use the default one created in the
        # branding migration
        if not organization:
            organization = Organization.objects.get(pk=1)

        with patch('accounts.utils_user.get_location') as patch:
            patch.return_value = self.create_location()
            email = unicode(uuid.uuid4()) + '@localhost.com'
            return create_user(organization, email, '20009', 'Joe', 'Smith')

    def create_superuser(self, organization=None):
        """Create a new superuser"""
        user = self.create_user(organization)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user
