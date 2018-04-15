"""Views related to processing feedback from ESP"""
import json
import logging

from django.conf import settings
from django_sns_view.views import SNSEndpoint

from feedback.tasks import process_feedback


# pylint: disable=invalid-name
logger = logging.getLogger(__name__)


class EmailFeedbackView(SNSEndpoint):
    """Process SNS Email Requests"""
    topic_settings_key = 'SES_FEEDBACK_TOPIC_ARN'

    def handle_message(self, message, payload):
        """Process an incoming email feedback message"""

        try:
            data = json.loads(message)
        except ValueError:
            logger.error('Message not valid JSON: %s', message)
            return

        # AWS will report-back delivery and receipt notifications if you want
        # it to. If we get those by accident we don't want them going any
        # further.
        if (data.get('eventType') not in
                ['Bounce', 'Click', 'Complaint', 'Open']):
            logger.warning('Invalid Notice Type: %s', data.get('eventType'))
            return

        # Check to make sure the source of the notification is the same
        # instance of the app as this one (incase there are multiple staging or
        # demo instances but they share one queue)
        app = data.get('mail', {}).get('tags', {}).get('app', [])[0]
        if app != settings.APP_NAME:
            logger.info('Invalid App Name: %s', app)
            return

        # Pass the feedback to a queue for later processing.
        process_feedback.delay(data)
