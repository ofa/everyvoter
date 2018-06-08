"""Test tasks.py"""
from datetime import datetime, date, time, timedelta

from django.test import TestCase
from mock import patch, call
from model_mommy import mommy
import pytz

from everyvoter_common.utils.tests import EveryVoterTestMixin
from mailer.tasks import (
    trigger_mailings, initialize_mailing, initialize_recipients, update_status,
    send_email
)
from mailer.models import Mailing, EmailActivity


class TestTriggerMailings(EveryVoterTestMixin, TestCase):
    """Test the trigger mailings task"""
    def setUp(self):
        """Setup the test"""
        test_date = date(2018, 12, 24)
        test_time = time(12, 0, 0, tzinfo=pytz.timezone('US/Eastern'))

        self.test_datetime = datetime.combine(test_date, test_time)

    @patch('mailer.tasks.timezone')
    @patch('mailer.tasks.initialize_mailing')
    def test_empty_calendar(self, initialize_mailing_patch, timezone_patch):
        """Test an empty calendar"""
        timezone_patch.localtime.return_value = self.test_datetime

        trigger_mailings()

        self.assertFalse(initialize_mailing_patch.apply_async.called)

    @patch('mailer.tasks.timezone')
    @patch('mailer.tasks.initialize_mailing')
    def test_full_calendar(self, initialize_mailing_patch, timezone_patch):
        """Test that a full calendar is triggered"""
        timezone_patch.localtime.return_value = self.test_datetime

        org1 = self.create_organization(email_active=True)
        org2 = self.create_organization(email_active=True)

        today_election = self.create_election(election_date=self.test_datetime)
        org1_orgelection = today_election.organizationelection_set.get(
            organization=org1)

        upcoming_vr_election = self.create_election(
            vr_deadline=self.test_datetime + timedelta(days=2))
        org2_orgelection = upcoming_vr_election.organizationelection_set.get(
            organization=org2)

        # Create 2 templates for upcoming elections
        election_deadline_org_1 = self.create_template(
            email__organization=org1,
            deadline_type='election_date',
            days_to_deadline=0)

        vr_deadline_org_2 = self.create_template(
            email__organization=org2,
            deadline_type='vr_deadline',
            days_to_deadline=2)

        expected_calls = [
            call(kwargs={
                'template_email_id': election_deadline_org_1.email.pk,
                'priority': 3,
                'organizationelection_id': org1_orgelection.pk
                }, priority=3),
            call(kwargs={
                'template_email_id': vr_deadline_org_2.email.pk,
                'priority': 1,
                'organizationelection_id': org2_orgelection.pk
                }, priority=1),
        ]

        # Call the mailing
        trigger_mailings()

        self.assertEqual(initialize_mailing_patch.apply_async.call_count, 2)
        initialize_mailing_patch.apply_async.assert_has_calls(expected_calls)

    @patch('mailer.tasks.timezone')
    def test_inactive_org(self, timezone_patch):
        """Test organizations without active mass mailings"""
        timezone_patch.localtime.return_value = self.test_datetime
        org = self.create_organization(email_active=True)

        today_election = self.create_election(election_date=self.test_datetime)
        org_orgelection = today_election.organizationelection_set.get(
            organization=org)

        election_deadline_org = self.create_template(
            email__organization=org,
            deadline_type='election_date',
            days_to_deadline=0)

        self.assertTrue(org.email_active)

        with patch('mailer.tasks.initialize_mailing') as mailing_patch:
            trigger_mailings()

            self.assertTrue(mailing_patch.apply_async.called)
            mailing_patch.apply_async.assert_called_once_with(
                kwargs={
                    'template_email_id': election_deadline_org.email.pk,
                    'priority': 3,
                    'organizationelection_id': org_orgelection.pk
                }, priority=3)

        org.email_active = False
        org.save()

        with patch('mailer.tasks.initialize_mailing') as mailing_patch:
            trigger_mailings()

            self.assertFalse(mailing_patch.apply_async.called)


class TestInitializeMailing(EveryVoterTestMixin, TestCase):
    """Test the initialize_mailing task"""
    @patch('mailer.tasks.initialize_recipients')
    def test_creates_mailing(self, initialize_recipients_patch):
        """Test creating of a mailing"""
        org = self.create_organization()
        election = self.create_election()
        org_election = election.organizationelection_set.get(organization=org)

        template_options = {
            'email__organization': org,
            'email__subject': 'Test Subject',
            'email__pre_header': 'Test Pre Header',
            'email__from_name': 'Test From Name',
            'email__body_above': 'This is the above body',
            'email__body_below': 'This is the below body'
        }
        template = self.create_template(**template_options)

        block1 = mommy.make('blocks.Block')
        block2 = mommy.make('blocks.Block')

        template.email.blocks.add(block1)
        template.email.blocks.add(block2)

        category1 = mommy.make('mailer.EmailCategory')
        category2 = mommy.make('mailer.EmailCategory')

        template.email.categories.add(category1)
        template.email.categories.add(category2)

        initialize_mailing(template.email.pk, org_election.pk, 3)

        new_mailing = Mailing.objects.select_related('email').get(
            template=template)

        # Make sure we didn't just re-assign the old Email to the new Mailing
        self.assertFalse(new_mailing.email.id == template.email.id)

        # Confirm the new mailing is like the old template, with fresh info
        self.assertEqual(new_mailing.email.organization, org)
        self.assertEqual(new_mailing.email.subject, 'Test Subject')
        self.assertEqual(new_mailing.email.pre_header, 'Test Pre Header')
        self.assertEqual(new_mailing.email.from_name, 'Test From Name')
        self.assertEqual(new_mailing.email.body_above,
                         'This is the above body')
        self.assertEqual(new_mailing.email.body_below,
                         'This is the below body')
        self.assertEqual(new_mailing.organization_election, org_election)
        self.assertEqual(new_mailing.status, 'pending')

        self.assertEqual(2, new_mailing.email.categories.count())
        self.assertIn(category1, new_mailing.email.categories.all())
        self.assertIn(category2, new_mailing.email.categories.all())

        self.assertEqual(2, new_mailing.email.categories.count())
        self.assertIn(block1, new_mailing.email.blocks.all())
        self.assertIn(block2, new_mailing.email.blocks.all())

        self.assertTrue(initialize_recipients_patch.apply_async.called)

        initialize_recipients_patch.apply_async.assert_called_once_with(
            kwargs={
                'email_id': new_mailing.email.pk,
                'organizationelection_id': org_election.pk,
                'priority': 3
            }, priority=3)


class TestInitializeRecipients(EveryVoterTestMixin, TestCase):
    """Test the initalize recipients task"""
    @patch('mailer.tasks.send_email')
    def test_initialize_recipients(self, send_email_patch):
        """Test the initialize Recipients"""
        election = self.create_election()
        org = self.create_organization(email_active=True)
        org_election = election.organizationelection_set.get(organization=org)


        user1 = self.create_user(organization=org)
        user2 = self.create_user(organization=org)
        user3 = self.create_user(organization=org)

        self.assertEqual(election.state_id, 'IL')
        self.assertEqual(user1.location.state_id, 'IL')
        self.assertEqual(user2.location.state_id, 'IL')
        self.assertEqual(user3.location.state_id, 'IL')

        self.assertIn(user1, org_election.get_recipients())
        self.assertIn(user2, org_election.get_recipients())
        self.assertIn(user3, org_election.get_recipients())

        mailing = self.create_mailing(
            email__organization=org, organization_election=org_election)

        self.assertEqual(mailing.count, 0)
        self.assertEqual(mailing.status, 'pending')

        expected_calls = [
            call(kwargs={
                'email_id': mailing.email.id,
                'recipient_id': user1.id,
                'election_id': election.id,
                'recipient_number': 1,
                'final': False
                }, priority=3),
            call(kwargs={
                'email_id': mailing.email.id,
                'recipient_id': user2.id,
                'election_id': election.id,
                'recipient_number': 2,
                'final': False
                }, priority=3),
            call(kwargs={
                'email_id': mailing.email.id,
                'recipient_id': user3.id,
                'election_id': election.id,
                'recipient_number': 3,
                'final': True
                }, priority=3)
        ]

        initialize_recipients(mailing.email.id, org_election.id, 3)

        new_mailing = Mailing.objects.get(pk=mailing.pk)
        self.assertEqual(new_mailing.count, 3)
        self.assertEqual(new_mailing.status, 'queued')

        self.assertEqual(send_email_patch.apply_async.call_count, 3)
        send_email_patch.apply_async.assert_has_calls(expected_calls)



class TestUpdateStatus(EveryVoterTestMixin, TestCase):
    """Test the update_status functionality"""
    @patch('mailer.tasks.time')
    def test_update_status_nonfinal(self, time_patch):
        """Test updating the status of a non-final time"""
        mailing = self.create_mailing(status='queued')

        self.assertEqual(mailing.sent, 0)
        self.assertEqual(mailing.status, 'queued')

        update_status(mailing.email.id, 1000, False)

        self.assertFalse(time_patch.sleep.called)

        new_mailing = Mailing.objects.get(pk=mailing.pk)
        self.assertEqual(new_mailing.sent, 1000)
        self.assertEqual(new_mailing.status, 'sending')

    @patch('mailer.tasks.time')
    def test_update_status_final(self, time_patch):
        """Test updating the status of a final time"""
        mailing = self.create_mailing(status='queued')

        for _ in range(0, 10):
            mommy.make(
                'mailer.EmailActivity', email=mailing.email, activity='send')

        self.assertEqual(mailing.sent, 0)
        self.assertEqual(mailing.status, 'queued')

        # Pass in a number that doesn't reflect the final count to ensure the
        # database-based count is run.
        update_status(mailing.email.id, 1500, True)

        time_patch.sleep.assert_called_once_with(5)

        new_mailing = Mailing.objects.get(pk=mailing.pk)
        self.assertEqual(new_mailing.sent, 10)
        self.assertEqual(new_mailing.status, 'sent')


class TestSendEmail(EveryVoterTestMixin, TestCase):
    """Test the individual email sending task"""
    @patch('mailer.tasks.update_status')
    def test_send_email_final(self, update_status_patch):
        """Test that sending a final email updates the status"""
        org = self.create_organization()
        recipient = self.create_user(organization=org)
        election = self.create_election()
        mailing = self.create_mailing()

        send_email(mailing.email_id, recipient.id, election.id, 2, True)

        self.assertTrue(EmailActivity.objects.filter(
            email=mailing.email, activity='send', recipient=recipient).exists())

        update_status_patch.apply_async.assert_called_once_with(
            kwargs={
                'email_id': mailing.email_id,
                'recipient_number': 2,
                'final': True
            },
            priority=4)

    @patch('mailer.tasks.update_status')
    def test_send_email_thousand(self, update_status_patch):
        """Test that sending a 1000 divisible email updates the status"""
        org = self.create_organization()
        recipient = self.create_user(organization=org)
        election = self.create_election()
        mailing = self.create_mailing()

        send_email(mailing.email_id, recipient.id, election.id, 1000, False)

        self.assertTrue(EmailActivity.objects.filter(
            email=mailing.email, activity='send', recipient=recipient).exists())

        update_status_patch.apply_async.assert_called_once_with(
            kwargs={
                'email_id': mailing.email_id,
                'recipient_number': 1000,
                'final': False
            },
            priority=1)

    @patch('mailer.tasks.update_status')
    def test_send_email_thousand(self, update_status_patch):
        """Test sending the first message"""
        org = self.create_organization()
        recipient = self.create_user(organization=org)
        election = self.create_election()
        mailing = self.create_mailing()

        send_email(mailing.email_id, recipient.id, election.id, 1, False)

        self.assertTrue(EmailActivity.objects.filter(
            email=mailing.email, activity='send', recipient=recipient).exists())

        update_status_patch.apply_async.assert_called_once_with(
            kwargs={
                'email_id': mailing.email_id,
                'recipient_number': 1,
                'final': False
            },
            priority=4)

    @patch('mailer.tasks.timezone')
    @patch('mailer.tasks.time')
    @patch('mailer.tasks.deliver')
    def test_send_mailing(self, deliver_patch, time_patch, timezone_patch):
        """Test the send process, start to finish"""
        test_date = date(2018, 12, 24)
        test_time = time(12, 0, 0, tzinfo=pytz.timezone('US/Eastern'))
        election_datetime = datetime.combine(test_date, test_time)

        org = self.create_organization(email_active=True)
        org.platform_name = 'Great Platform'
        org.save()

        org.primary_domain.hostname = 'supertest.cool.com'
        org.primary_domain.save()

        recipient1 = self.create_user(organization=org, first='Adam',
                                      last='Cat', email='friends@sunset.local')
        recipient2 = self.create_user(organization=org, first='Nick',
                                      last='Smith', email='lovely@dogs.local')

        election = self.create_election(election_date=election_datetime)
        org_election = election.organizationelection_set.get(organization=org)

        wrapper = mommy.make('mailer.EmailWrapper',
                             header='{{ organization.platform_name }}',
                             footer='<a href="{{ unsubscribe_url }}"> '
                                    'Cool</a><a href="{{ manage_url }}"> '
                                    'Nifty!</a>',
                             default=False,
                             organization=org)
        org_election.email_wrapper = wrapper
        org_election.save()

        template = self.create_template(
            email__organization=org,
            deadline_type='election_date',
            days_to_deadline=0,
            email__subject='{{ recipient.first_name }} Hey!',
            email__from_name='Lovely People',
            email__body_above='Above {{recipient.email}}! https://google.com/',
            email__body_below='Below {{recipient.email}}! https://github.com/')

        timezone_patch.now.return_value = election_datetime
        timezone_patch.localtime.return_value = election_datetime

        deliver_patch.return_value = 'abcd123'

        trigger_mailings()

        mailing = Mailing.objects.select_related('email').get(template=template)
        self.assertEqual(mailing.status, 'sent')
        self.assertEqual(mailing.sent, 2)
        self.assertEqual(mailing.count, 2)

        # Call One: Adam Cat
        call_one = deliver_patch.call_args_list[0][1]

        self.assertEqual(
            call_one['to_address'], 'Adam Cat <friends@sunset.local>')
        self.assertEqual(
            call_one['from_address'], 'Lovely People <app@everyvoter.us>')
        self.assertEqual(
            call_one['subject'], 'Adam Hey!')

        tags_one = {
            'email_id': mailing.email.id,
            'recipient_id': recipient1.id,
            'organization_id': org.id
        }

        self.assertDictEqual(call_one['tags'], tags_one)

        self.assertIn('Great Platform', call_one['html'])
        self.assertIn('Above friends@sunset.local!', call_one['html'])
        self.assertIn('Below friends@sunset.local!', call_one['html'])
        self.assertIn('utm_medium=email', call_one['html'])
        self.assertIn('utm_source=ev', call_one['html'])
        self.assertIn(
            'https://supertest.cool.com/unsubscribe/', call_one['html'])
        self.assertIn(
            'https://supertest.cool.com/user/{}/'.format(recipient1.username),
            call_one['html'])

        # Call 2: Nick Smith
        call_two = deliver_patch.call_args_list[1][1]

        self.assertEqual(
            call_two['to_address'], 'Nick Smith <lovely@dogs.local>')
        self.assertEqual(
            call_one['from_address'], 'Lovely People <app@everyvoter.us>')
        self.assertEqual(
            call_two['subject'], 'Nick Hey!')

        tags_two = {
            'email_id': mailing.email.id,
            'recipient_id': recipient2.id,
            'organization_id': org.id
        }

        self.assertDictEqual(call_two['tags'], tags_two)

        self.assertIn('Great Platform', call_two['html'])
        self.assertIn('Above lovely@dogs.local!', call_two['html'])
        self.assertIn('Below lovely@dogs.local!', call_two['html'])
        self.assertIn('utm_medium=email', call_two['html'])
        self.assertIn('utm_source=ev', call_two['html'])
        self.assertIn(
            'https://supertest.cool.com/unsubscribe/', call_two['html'])
        self.assertIn(
            'https://supertest.cool.com/user/{}/'.format(recipient2.username),
            call_two['html'])
