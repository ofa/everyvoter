"""Test the mailserver code in the mailer app"""
import logging

from django.test import TestCase, override_settings
from mock import patch

from everyvoter_common.utils.tests import EveryVoterTestMixin
from mailer.mailserver import deliver


class TestDeliver(EveryVoterTestMixin, TestCase):
    """Test the create_user method"""
    def setUp(self):
        logging.disable(logging.CRITICAL)

    @override_settings(EMAIL_ACTIVE=True)
    @override_settings(SES_CONFIGURATIONSET_NAME='everyvoter-set')
    @override_settings(APP_NAME='cool-app')
    @patch('mailer.mailserver.client')
    def test_success(self, mock):
        """Test a successful call"""
        mock.send_email.return_value = {'MessageId': 'fake-message-id'}

        input_tags = {
            'Example': 'One'
        }

        response = deliver(
            'to@example.local', 'from@example.local', 'Subject', 'Body',
            input_tags)

        self.assertEqual(response, 'fake-message-id')

        send_email_call_kwargs = mock.send_email.call_args_list[0][1]
        self.assertEqual(send_email_call_kwargs['Source'],
                         'from@example.local')
        self.assertEqual(send_email_call_kwargs['Destination']['ToAddresses'],
                         ['to@example.local'])
        self.assertEqual(send_email_call_kwargs['ConfigurationSetName'],
                         'everyvoter-set')

        # Because Tags is a dictionary with one extra field turned into a list
        # of dictionaries there is essentially no clean way of testing the tags
        # and thus we need to loop through and hope we've covered all the
        # possibilities
        for tag in send_email_call_kwargs['Tags']:
            self.assertIn(tag['Name'], ['Example', 'app'])
            self.assertIn(tag['Value'], ['One', 'cool-app'])

    @override_settings(EMAIL_ACTIVE=False)
    @patch('mailer.mailserver.client')
    def test_disabled(self, mock):
        """Test that an email is not sent with EMAIL_ACTIVE is false"""
        response = deliver(
            'to@example.com', 'from@example.local', 'Subject', 'Body', {})
        self.assertEqual(response, '')
        self.assertFalse(mock.send_email.called)
