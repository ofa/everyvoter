"""Test the election calendar"""
from datetime import datetime

from django.db import models
from django.test import TestCase, override_settings
from smalluuid import SmallUUID
from mock import patch
from model_mommy import mommy

from everyvoter_common.utils.tests import EveryVoterTestMixin
from mailer.send_calendar import mailing_calendar


class TestCalendar(EveryVoterTestMixin, TestCase):
    """Test the send calendar"""
    def setUp(self):
        """Setup the test"""
        self.organization = self.create_organization()

        self.election1 = self.create_election(
            evip_start_date=datetime(2018, 7, 5),
            evip_close_date=datetime(2018, 7, 10),
            vbm_application_deadline=datetime(2018, 7, 15),
            vbm_return_date=datetime(2018, 7, 20),
            vr_deadline=datetime(2018, 7, 25),
            vr_deadline_online=datetime(2018, 7, 24),
            election_date=datetime(2018, 7, 30),
            election_type='general')

        self.election2 = self.create_election(
            evip_start_date=datetime(2018, 12, 5),
            evip_close_date=datetime(2018, 12, 10),
            vbm_application_deadline=datetime(2018, 12, 15),
            vbm_return_date=datetime(2018, 12, 20),
            vr_deadline=datetime(2018, 12, 25),
            vr_deadline_online=datetime(2018, 12, 24),
            election_date=datetime(2018, 12, 30),
            election_type='general')

        # Create templates for each deadline
        self.template_evip_start_date = self.create_template(
            email__organization=self.organization,
            deadline_type='evip_start_date',
            days_to_deadline=5,
            election_type='general')

        self.template_evip_close_date = self.create_template(
            email__organization=self.organization,
            deadline_type='evip_close_date',
            days_to_deadline=5,
            election_type='general')

        # pylint: disable=invalid-name
        self.template_vbm_application_deadline = self.create_template(
            email__organization=self.organization,
            deadline_type='vbm_application_deadline',
            days_to_deadline=5,
            election_type='general')

        self.template_vbm_return_date = self.create_template(
            email__organization=self.organization,
            deadline_type='vbm_return_date',
            days_to_deadline=5,
            election_type='general')

        self.template_vr_deadline = self.create_template(
            email__organization=self.organization,
            deadline_type='vr_deadline',
            days_to_deadline=5,
            election_type='general')

        self.template_election_date = self.create_template(
            email__organization=self.organization,
            deadline_type='election_date',
            days_to_deadline=5,
            election_type='general')

        self.template_election_day = self.create_template(
            email__organization=self.organization,
            deadline_type='election_date',
            days_to_deadline=0,
            election_type='general')

    def test_length(self):
        """Test the length of the response"""

        # Get the calendar, and turn it into a list
        calendar = mailing_calendar(organization=self.organization)
        calendar_list = list(calendar)

        # Confirm there are 12 emails
        self.assertEquals(len(calendar_list), 14)

    def test_ordering(self):
        """Test the ordering of the emails"""

        # Get the calendar, and turn it into a list
        calendar = mailing_calendar(organization=self.organization)
        calendar_list = list(calendar)

        # Confirm the emails are in the correct order
        self.assertEquals(calendar_list[0].id, self.template_evip_start_date.id)
        self.assertEquals(calendar_list[7].id, self.template_evip_start_date.id)

        self.assertEquals(calendar_list[1].id, self.template_evip_close_date.id)
        self.assertEquals(calendar_list[8].id, self.template_evip_close_date.id)

        self.assertEquals(
            calendar_list[2].id, self.template_vbm_application_deadline.id)
        self.assertEquals(
            calendar_list[9].id, self.template_vbm_application_deadline.id)

        self.assertEquals(calendar_list[3].id, self.template_vbm_return_date.id)
        self.assertEquals(calendar_list[10].id, self.template_vbm_return_date.id)

        self.assertEquals(calendar_list[4].id, self.template_vr_deadline.id)
        self.assertEquals(calendar_list[11].id, self.template_vr_deadline.id)

        self.assertEquals(calendar_list[5].id, self.template_election_date.id)
        self.assertEquals(calendar_list[12].id, self.template_election_date.id)

        self.assertEquals(calendar_list[6].id, self.template_election_day.id)
        self.assertEquals(calendar_list[13].id, self.template_election_day.id)

    def test_annotated(self):
        """Confirm each annotated field"""
        self.create_user(organization=self.organization)
        self.create_user(organization=self.organization)

        calendar = mailing_calendar(organization=self.organization)
        calendar_list = list(calendar)

        mailing1 = calendar_list[0]

        self.assertEquals(
            type(mailing1.election_id), int)
        self.assertEquals(mailing1.election_id, self.election1.id)

        org_election = self.election1.organizationelection_set.get(
            organization=self.organization)
        self.assertEquals(
            type(mailing1.organizationelection_id), int)
        self.assertEquals(mailing1.organizationelection_id, org_election.pk)

        self.assertEquals(type(mailing1.send_date), datetime)
        self.assertEquals(mailing1.send_date, datetime(2018, 6, 30))

        self.assertEquals(
            type(mailing1.election_state_id), unicode)
        self.assertEquals(mailing1.election_state_id, 'IL')

        self.assertEquals(
            type(mailing1.total_recipients), long)
        self.assertEquals(mailing1.total_recipients, 2)

        # Problem: UUIDs are returned as UUIDs and not SmallUUIDs. Submitted
        # a question to StackOverflow about this.
        #self.assertEquals(type(mailing1.email_uuid), SmallUUID)
        #self.assertEquals(
        #    mailing1.email_uuid, self.template_evip_start_date.email.uuid)

    def test_election(self):
        """Test the election ids"""

        # Get the calendar, and turn it into a list
        calendar = mailing_calendar(organization=self.organization)
        calendar_list = list(calendar)

        # Confirm the first 7 emails are for the first election
        self.assertEquals(calendar_list[0].election_id, self.election1.pk)
        self.assertEquals(calendar_list[1].election_id, self.election1.pk)
        self.assertEquals(calendar_list[2].election_id, self.election1.pk)
        self.assertEquals(calendar_list[3].election_id, self.election1.pk)
        self.assertEquals(calendar_list[4].election_id, self.election1.pk)
        self.assertEquals(calendar_list[5].election_id, self.election1.pk)
        self.assertEquals(calendar_list[6].election_id, self.election1.pk)

        # Confirm the final 7 emails are for the second election
        self.assertEquals(calendar_list[7].election_id, self.election2.pk)
        self.assertEquals(calendar_list[8].election_id, self.election2.pk)
        self.assertEquals(calendar_list[9].election_id, self.election2.pk)
        self.assertEquals(calendar_list[10].election_id, self.election2.pk)
        self.assertEquals(calendar_list[11].election_id, self.election2.pk)
        self.assertEquals(calendar_list[12].election_id, self.election2.pk)
        self.assertEquals(calendar_list[13].election_id, self.election2.pk)

    def test_send_date(self):
        """Test the send date"""

        # Get the calendar, and turn it into a list
        calendar = mailing_calendar(organization=self.organization)
        calendar_list = list(calendar)

        # Confirm Early Vote Start date
        self.assertEquals(calendar_list[0].send_date, datetime(2018, 6, 30))
        self.assertEquals(calendar_list[7].send_date, datetime(2018, 11, 30))

        # Confirm Early Vote close date
        self.assertEquals(calendar_list[1].send_date, datetime(2018, 7, 5))
        self.assertEquals(calendar_list[8].send_date, datetime(2018, 12, 5))

        # Confirm Vote By Mail Application date
        self.assertEquals(calendar_list[2].send_date, datetime(2018, 7, 10))
        self.assertEquals(calendar_list[9].send_date, datetime(2018, 12, 10))

        # Confirm Vote By Mail Return date
        self.assertEquals(calendar_list[3].send_date, datetime(2018, 7, 15))
        self.assertEquals(calendar_list[10].send_date, datetime(2018, 12, 15))

        # Confirm Voter Registration date
        self.assertEquals(calendar_list[4].send_date, datetime(2018, 7, 20))
        self.assertEquals(calendar_list[11].send_date, datetime(2018, 12, 20))

        # Confirm 5 day out election day send
        self.assertEquals(calendar_list[5].send_date, datetime(2018, 7, 25))
        self.assertEquals(calendar_list[12].send_date, datetime(2018, 12, 25))

        # Confirm election day email goes out on election day
        self.assertEquals(calendar_list[6].send_date, datetime(2018, 7, 30))
        self.assertEquals(calendar_list[13].send_date, datetime(2018, 12, 30))

    def test_online_vote(self):
        """Test an organization that is using the online VR date"""
        self.organization.online_vr = False
        self.organization.save()

        calendar = mailing_calendar(organization=self.organization)
        calendar_list = list(calendar)

        # Confirm we got the templates we need back
        self.assertEqual(len(calendar_list), 14)

        # Confirm Voter Registration date based on non-online date
        self.assertEquals(calendar_list[4].send_date, datetime(2018, 7, 20))
        self.assertEquals(calendar_list[11].send_date, datetime(2018, 12, 20))

        self.organization.online_vr = True
        self.organization.save()

        calendar_online = mailing_calendar(organization=self.organization)
        calendar_online_list = list(calendar_online)

        # Confirm the number of emails hasn't changed
        self.assertEqual(len(calendar_online_list), 14)

        # Confirm Voter Registration date
        self.assertEquals(
            calendar_online_list[4].send_date, datetime(2018, 7, 19))
        self.assertEquals(
            calendar_online_list[11].send_date, datetime(2018, 12, 19))

    def test_send_count(self):
        """Test that the send count is correct"""
        # Create a new organization
        organization = self.create_organization()

        # Create 15 users in that organization
        for _ in range(0, 15):
            self.create_user(organization=organization)

        # Create a voting reg deadline template
        mommy.make(
            'mailer.MailingTemplate',
            email__organization=organization,
            deadline_type='vr_deadline',
            days_to_deadline=5,
            election_type='general')

        # Get the OrganizationElection for each election we created in setUp
        org_election1 = self.election1.organizationelection_set.get(
            organization=organization)

        org_election2 = self.election2.organizationelection_set.get(
            organization=organization)

        # Get the calendar, turn it into a list
        calendar = mailing_calendar(organization=organization)
        calendar_list = list(calendar)

        # Check the length of the list
        self.assertEquals(len(calendar_list), 2)

        # Confirm our recipient count is right
        self.assertEquals(calendar_list[0].total_recipients, 15)
        self.assertEquals(calendar_list[0].total_recipients, 15)

        # As a quick test, also make sure the python orgelection count is good
        self.assertEquals(org_election1.total_recipients, 15)
        self.assertEquals(org_election2.total_recipients, 15)

        # Confirm the org election IDs
        self.assertEquals(
            calendar_list[0].organizationelection_id, org_election1.id)
        self.assertEquals(
            calendar_list[1].organizationelection_id, org_election2.id)

    def test_date_filter(self):
        """
        Test that you can request a set date and only get results for that date
        """

        # Get templates for election day of election 1
        limited_calendar = mailing_calendar(
            organization=self.organization, date=datetime(2018, 7, 30))
        calendar_list = list(limited_calendar)

        self.assertEqual(len(calendar_list), 1)
        self.assertEqual(calendar_list[0].id, self.template_election_day.pk)
        self.assertEqual(calendar_list[0].election_id, self.election1.id)
        self.assertEqual(calendar_list[0].send_date, datetime(2018, 7, 30))

    def test_active_only(self):
        """Test where calendar only shows messages for email enabled orgs"""
        # Confirm the organizaton is enabled for email
        self.organization.email_active = True
        self.organization.save()
        self.assertTrue(self.organization.email_active)

        # Get the calendar without the email active filter and turn into a list
        calendar = mailing_calendar(organization=self.organization)
        calendar_list = list(calendar)

        self.assertEqual(len(calendar_list), 14)

        self.organization.email_active = False
        self.organization.save()
        self.assertFalse(self.organization.email_active)

        active_calendar = mailing_calendar(organization=self.organization,
                                           email_active=True)
        active_calendar_list = list(active_calendar)

        self.assertEqual(len(active_calendar_list), 0)
