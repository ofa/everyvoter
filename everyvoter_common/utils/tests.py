"""Common mixins for tests"""
import os
import json
import uuid
from datetime import timedelta

from django.utils.timezone import now
from model_mommy import mommy

from accounts.utils_user import create_user
from accounts.models import User
from branding.models import Organization
from branding.utils import get_or_create_organization
from location.utils import get_location
from election.models import LegislativeDistrict, Election

# pylint: disable=invalid-name
path = os.path.dirname(os.path.abspath(__file__))
illinois_file = os.path.join(
    path, 'data/geocodio_illinois.json')
with open(illinois_file) as json_file:
    illinois_geocode = json.loads(json_file.read())


class EveryVoterTestMixin(object):
    """Mixin for EveryVoter tests"""
    def create_organization(self, email_active=False, wrapper=None):
        """Create an organization with the test domain"""
        name = unicode(uuid.uuid4())
        platform_name = unicode(uuid.uuid4())
        hostname = unicode(uuid.uuid4())
        homepage = u'http://' + unicode(uuid.uuid4())
        organization, _ = get_or_create_organization(
            name=name, platform_name=platform_name, hostname=hostname,
            homepage=homepage)

        if email_active:
            organization.email_active = True
            organization.save()

        return organization

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

    def create_user(self, organization=None, location=None, first='Joe',
                    last='Smith', email=None):
        """Create a new user"""
        from mock import patch

        # If no organization is passed in, use the default one created in the
        # branding migration
        if not organization:
            organization = Organization.objects.get(pk=1)

        if not email:
            email = unicode(uuid.uuid4()) + '@localhost.com'

        with patch('accounts.utils_user.get_location') as patch:
            patch.return_value = self.create_location()
            return create_user(organization, email, '20009', first, last)

    def create_superuser(self, *args, **kwargs):
        """Create a new superuser"""
        user = self.create_staff(*args, **kwargs)
        user.is_superuser = True
        user.save()
        return user

    def create_staff(self, *args, **kwargs):
        """Create a new staff member"""
        user = self.create_user(*args, **kwargs)
        user.is_staff = True
        user.save()
        user.set_password(User.objects.make_random_password())
        mommy.make('notifications.NotificationSetting', user=user)
        return user

    def create_template(self, **kwargs):
        """Create a mailing template"""
        kwargs['election_type'] = kwargs.get('election_type', 'general')
        kwargs['days_to_deadline'] = kwargs.get('days_to_deadline', 0)

        if 'email__organization' not in kwargs:
            kwargs['email__organization'] = self.create_organization()

        kwargs['deadline_type'] = kwargs.get('deadline_type', 'election_date')

        return mommy.make(
            'mailer.MailingTemplate',
            **kwargs)

    def create_mailing(self, **kwargs):
        """Create a mailing"""
        kwargs['email__organization'] = kwargs.get(
            'email__organization', self.create_organization())

        if 'organization_election' not in kwargs:
            election = self.create_election()
            org_election = election.organizationelection_set.get(
                organization=kwargs['email__organization'])
            kwargs['organization_election'] = org_election

        if 'template' not in kwargs:
            template = self.create_template(
                email__organization=kwargs['email__organization'])
            kwargs['template'] = template

        return mommy.make('mailer.Mailing', **kwargs)

    def create_election(self, voting_districts=None, **kwargs):
        """Create a new election"""

        # The election type is federal general
        kwargs['election_type'] = kwargs.get('election_type', 'general')

        # The state is Illinois
        kwargs['state_id'] = kwargs.get('state_id', 'IL')

        # The election is the date provided (or today)
        kwargs['election_date'] = kwargs.get('election_date', now())

        # The VR deadline was 29 days ago
        kwargs['vr_deadline'] = kwargs.get(
            'vr_deadline', kwargs['election_date'] - timedelta(days=29))

        # The Online VR deadline was 30 days ago
        kwargs['vr_deadline_online'] = kwargs.get(
            'vr_deadline_online', kwargs['election_date'] - timedelta(days=30))

        # Early Vote started 20 days ago
        kwargs['evip_start_date'] = kwargs.get(
            'evip_start_date', kwargs['election_date'] - timedelta(days=20))

        # Early Vote ended 5 days ago
        kwargs['evip_close_date'] = kwargs.get(
            'evip_close_date', kwargs['election_date'] - timedelta(days=5))

        # Vote By Mail Application Deadline was 3 days ago
        kwargs['vbm_application_deadline'] = kwargs.get(
            'vbm_application_deadline',
            kwargs['election_date'] - timedelta(days=3))

        # Vote by mail return date was yesterday
        kwargs['vbm_return_date'] = kwargs.get(
            'vbm_return_date', kwargs['election_date'] - timedelta(days=1))

        election = Election(**kwargs)
        election.save()

        # The districts targeted are the state of Illinois
        if not voting_districts:
            voting_districts = LegislativeDistrict.objects.filter(
                state_id='IL', district_type='state')

        election.voting_districts.set(voting_districts)

        return election
