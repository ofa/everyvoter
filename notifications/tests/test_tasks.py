"""Test tasks related to rendering"""
from datetime import datetime

from django.test import TestCase
import pytz
from mock import patch, call

from everyvoter_common.utils.tests import EveryVoterTestMixin
from notifications.tasks import daily_sample_batch


class TestBatchSample(EveryVoterTestMixin, TestCase):
    """Test the daily batch sampling task"""
    def setUp(self):
        """Setup the test"""
        self.election = self.create_election(
            election_date=datetime(2018, 7, 30),
            election_type='general')

        # Generate a timezone-aware datetime to be returned by a patched
        # localtime()
        self.now = datetime(2018, 7, 29, 1, 1, 1).replace(
            tzinfo=pytz.utc)

    @patch('notifications.tasks.timezone')
    @patch('notifications.tasks.sample_email')
    def test_one(self, sample_patch, timezone_patch):
        """Test where there is one upcoming email"""
        # The day before the election that has an email
        timezone_patch.localtime.return_value = self.now

        organization = self.create_organization()

        recipient = self.create_staff(
            organization=organization,
            email='single_recipient@test.localhost')
        recipient.notificationsetting.daily_batch_sample = True
        recipient.notificationsetting.save()

        # Add non-recipients
        self.create_user(organization=organization)
        self.create_staff(organization=organization)

        # Create a new election-day email
        template_election_day = self.create_template(
            email__organization=organization,
            deadline_type='election_date',
            days_to_deadline=0,
            election_type='general')

        daily_sample_batch.delay()

        sample_patch.delay.assert_called_once_with(
            to_address='single_recipient@test.localhost',
            user_id=recipient.id,
            email_id=template_election_day.email_id,
            election_id=self.election.id,
            district_ids=None)

    @patch('notifications.tasks.timezone')
    @patch('notifications.tasks.sample_email')
    def test_multiple_org(self, sample_patch, timezone_patch):
        """Test multiple emails from multiple orgs"""
        timezone_patch.localtime.return_value = self.now

        # Create everything for org1
        org1 = self.create_organization()

        recipient_org1 = self.create_staff(
            organization=org1,
            email='org1_email@org1.localhost')
        recipient_org1.notificationsetting.daily_batch_sample = True
        recipient_org1.notificationsetting.save()

        # Create dummy users/staff who should not get email
        self.create_user(organization=org1)
        self.create_staff(organization=org1)

        template_election_day_org1 = self.create_template(
            email__organization=org1,
            deadline_type='election_date',
            days_to_deadline=0,
            election_type='general')

        # Create everything for org2
        org2 = self.create_organization()

        recipient_org2 = self.create_staff(
            organization=org2,
            email='org2_email@org2.localhost')
        recipient_org2.notificationsetting.daily_batch_sample = True
        recipient_org2.notificationsetting.save()

        self.create_user(organization=org2)
        self.create_staff(organization=org2)

        template_election_day_org2 = self.create_template(
            email__organization=org2,
            deadline_type='election_date',
            days_to_deadline=0,
            election_type='general')

        # Run the task
        daily_sample_batch.delay()

        expected_calls = [
            call(
                to_address='org1_email@org1.localhost',
                user_id=recipient_org1.id,
                email_id=template_election_day_org1.email_id,
                election_id=self.election.id,
                district_ids=None),
            call(
                to_address='org2_email@org2.localhost',
                user_id=recipient_org2.id,
                email_id=template_election_day_org2.email_id,
                election_id=self.election.id,
                district_ids=None),
        ]

        sample_patch.delay.assert_has_calls(expected_calls)
