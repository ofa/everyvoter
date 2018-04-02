"""Test the mailserver code in the mailer app"""
from django.test import TestCase, override_settings
from mock import patch

from kennedy_common.utils.tests import KennedyTestMixin
from mailer.mailserver import deliver


class TestDeliver(KennedyTestMixin, TestCase):
    """Test the create_user method"""

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

        # Because Tags is a dictionary with one extra field turned into a list
        # of dictionaries there is essentially no clean way of testing the tags
        # and thus we need to loop through and hope we've covered all the
        # possibilities
        for tag in send_email_call_kwargs['Tags']:
            self.assertIn(tag['Name'], ['Example', 'app'])
            self.assertIn(tag['Value'], ['One', 'cool-app'])
