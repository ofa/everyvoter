"""Test tasks.py in feedback"""
import os
import json

from django.test import TestCase, override_settings
from mock import patch

from accounts.models import User
from mailer.models import EmailActivity, Unsubscribe
from feedback.tasks import (
    process_tags, extract_email, global_unsubscribe, process_feedback
)
from everyvoter_common.utils.tests import EveryVoterTestMixin


def load_example(filename):
    """Load a JSON file and return it"""
    path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(
        path, 'json/example_{file}.json'.format(file=filename))) as json_file:
        return json.load(json_file)


class TestExtract(TestCase):
    """Test the functions that extract data from messages"""
    def test_process_tags(self):
        """Test where tags are present"""
        filled = load_example('tags_filled')
        organization_id, mailing_id, recipient_id = process_tags(filled)

        self.assertEqual(organization_id, 1)
        self.assertEqual(mailing_id, 44)
        self.assertEqual(recipient_id, 100)

    def test_process_missing_tags(self):
        """Test where the tags are not present"""
        unfilled = load_example('tags_empty')
        organization_id, mailing_id, recipient_id = process_tags(unfilled)

        self.assertIsNone(organization_id)
        self.assertIsNone(mailing_id)
        self.assertIsNone(recipient_id)

    def test_extract_email(self):
        """Test extracting email from the mail part of the message"""
        bounce = load_example('bounce')
        click = load_example('click')

        self.assertEqual(
            extract_email(bounce['mail']), 'bounce@simulator.amazonses.com')
        self.assertEqual(extract_email(click['mail']), 'ssmith@ishouldvote.us')


class TestGlobalUnsubscribe(EveryVoterTestMixin, TestCase):
    """Test the global_unsubscribe function"""
    def test_unaffiliated_unsubscribe(self):
        """Test an unsubscribe where there is no mailing or user"""
        global_unsubscribe('unsubtest@test.local', 'bounce')

        unsub = Unsubscribe.objects.get(email='unsubtest@test.local')

        self.assertIsNone(unsub.organization)
        self.assertIsNone(unsub.mailing)
        self.assertIsNone(unsub.user)
        self.assertTrue(unsub.global_unsub)
        self.assertEqual(unsub.origin, 'bounce')
        self.assertEqual(unsub.reason, '')

    def test_affiliated_unsubscribe(self):
        """Test an unsubscribe affiliated with other objects

        TODO: Test this with Mailing
        """
        organization = self.create_organization()
        user = self.create_user(organization=organization)
        user_email = user.email

        self.assertFalse(user.unsubscribed)

        global_unsubscribe(
            user_email, 'complaint', reason='A Complaint',
            organization_id=organization.pk, mailing_id=None,
            recipient_id=user.pk)

        unsub = Unsubscribe.objects.get(email=user_email)

        self.assertEqual(unsub.organization, organization)
        self.assertEqual(unsub.user, user)
        self.assertIsNone(unsub.mailing)
        self.assertEqual(unsub.origin, 'complaint')
        self.assertEqual(unsub.reason, 'A Complaint')

        # Pull the user again to make sure that user is marked as unsubscribed
        user_repull = User.objects.get(pk=user.pk)
        self.assertTrue(user_repull.unsubscribed)


class TestProcessFeedback(EveryVoterTestMixin, TestCase):
    """Test processing feedback"""
    def setUp(self):
        """Setup the test"""
        self.tags_patch = patch('feedback.tasks.process_tags')
        self.addCleanup(self.tags_patch.stop)
        self.mock_tags_patch = self.tags_patch.start()

        self.unsub_patch = patch('feedback.tasks.global_unsubscribe')
        self.addCleanup(self.unsub_patch.stop)
        self.mock_unsub_patch = self.unsub_patch.start()

    def test_complaint(self):
        """Test a complaint"""
        organization = self.create_organization()
        user = self.create_user(organization=organization)

        complaint = load_example('complaint')
        mid = '01000162c1dade8e-7e98c826-366e-45d3-bf70-3552abc1ca99-000000'
        email = 'complaint@simulator.amazonses.com'

        self.mock_tags_patch.return_value = (organization.pk, None, user.pk)

        process_feedback(complaint)

        activity = EmailActivity.objects.get(message_id=mid)
        self.assertIsNone(activity.mailing)
        self.assertEqual(activity.recipient, user)
        self.assertEqual(activity.activity, 'complaint')

        self.mock_unsub_patch.assert_called_once_with(
            email, 'complaint', 'Complaint', organization.pk, None, user.pk)

    def test_hard_bounce(self):
        """Test a hard bounce with a recipient"""
        organization = self.create_organization()
        user = self.create_user(organization=organization)

        bounce = load_example('bounce')
        mid = '01000162c1d957c2-3de85a8f-04f1-4005-a902-61231a95628a-000000'
        email = 'bounce@simulator.amazonses.com'

        self.mock_tags_patch.return_value = (organization.pk, None, user.pk)

        process_feedback(bounce)

        activity = EmailActivity.objects.get(message_id=mid)
        self.assertIsNone(activity.mailing)
        self.assertEqual(activity.recipient, user)
        self.assertEqual(activity.activity, 'bounce')

        self.mock_unsub_patch.assert_called_once_with(
            email, 'bounce', 'smtp; 550 5.1.1 user unknown', organization.pk,
            None, user.pk)

    def test_suppression(self):
        """Test an email to a suppressed email address w/o a recipient"""
        bounce = load_example('suppression')
        mid = '01000162c1db46a8-c19ffb50-59c2-46b1-9fde-6a2d6894b110-000000'
        email = 'suppressionlist@simulator.amazonses.com'

        # Reasons are cut off after 255 characters
        reason = ('Amazon SES has suppressed sending to this address because '
                  'it has a recent history of bouncing as an invalid address. '
                  'For more information about how to remove an address from '
                  'the suppression list, see the Amazon SES Developer Guide: '
                  'http://docs.aws.amazon.')

        self.mock_tags_patch.return_value = (None, None, None)

        process_feedback(bounce)

        activity = EmailActivity.objects.get(message_id=mid)
        self.assertIsNone(activity.mailing)
        self.assertIsNone(activity.recipient)
        self.assertEqual(activity.activity, 'bounce')

        self.mock_unsub_patch.assert_called_once_with(
            email, 'bounce', reason, None, None, None)

    def test_soft_bounce(self):
        """Test a hard bounce with a recipient"""
        user = self.create_user()

        soft_bounce = load_example('outofoffice')
        mid = '01000162c1da489d-888942ee-338b-4b6b-b05d-a25cebbfbd5d-000000'

        self.mock_tags_patch.return_value = (None, None, user.pk)

        process_feedback(soft_bounce)

        activity = EmailActivity.objects.get(message_id=mid)
        self.assertIsNone(activity.mailing)
        self.assertEqual(activity.recipient, user)
        self.assertEqual(activity.activity, 'soft_bounce')

        self.assertFalse(self.mock_unsub_patch.called)

    def test_open(self):
        """Test an open"""
        user = self.create_user()

        open_message = load_example('open')
        mid = '01000162c1d60ad8-f3163420-9b55-483c-aebf-ad4c4f994461-000000'

        self.mock_tags_patch.return_value = (None, None, user.pk)

        process_feedback(open_message)

        activity = EmailActivity.objects.get(message_id=mid, activity='open')
        self.assertIsNone(activity.mailing)
        self.assertEqual(activity.recipient, user)
        self.assertEqual(activity.activity, 'open')

        self.assertFalse(self.mock_unsub_patch.called)

    def test_click(self):
        """Test a click"""
        user = self.create_user()

        open_message = load_example('click')
        mid = '01000162c1d60ad8-f3163420-9b55-483c-aebf-ad4c4f994461-000000'

        self.mock_tags_patch.return_value = (None, None, user.pk)

        process_feedback(open_message)

        activity = EmailActivity.objects.get(message_id=mid, activity='click')
        self.assertIsNone(activity.mailing)
        self.assertEqual(activity.recipient, user)
        self.assertEqual(activity.activity, 'click')
        self.assertEqual(activity.link, 'https://localhost/register-to-vote/')

        self.assertFalse(self.mock_unsub_patch.called)
