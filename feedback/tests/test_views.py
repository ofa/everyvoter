"""Test for feedback views"""
import os
import json

from django.test import TestCase, override_settings
from mock import patch
from testfixtures import log_capture

from feedback.views import EmailFeedbackView


class TestEmailFeedbackHandleMessage(TestCase):
    """Test the handle_message() part of the EmailFeedbackView"""
    def setUp(self):
        """Setup the test"""
        self.view = EmailFeedbackView()

        self.path = os.path.dirname(os.path.abspath(__file__))

    @log_capture()
    def test_invalid_json(self, capture):
        """Test invalid JSON"""
        self.view.handle_message('hey', '')

        capture.check(
            ('feedback.views', 'ERROR', 'Message not valid JSON: hey')
        )

    @log_capture()
    def test_invalid_notice(self, capture):
        """Test invalid Notice Type"""
        with open(os.path.join(
            self.path, 'json/example_send.json')) as json_file:
            file_content = json_file.read()

            self.view.handle_message(file_content, '')

        capture.check(
            ('feedback.views', 'WARNING', 'Invalid Notice Type: Send')
        )

    @override_settings(APP_NAME='bad-app-name')
    @log_capture()
    def test_invalid_app_name(self, capture):
        """Test where the app name is wrong"""
        with open(os.path.join(
            self.path, 'json/example_click.json')) as json_file:
            self.view.handle_message(json_file.read(), '')

        capture.check(
            ('feedback.views', 'INFO', 'Invalid App Name: everyvoter-testing')
        )

    @override_settings(APP_NAME='everyvoter-testing')
    @patch('feedback.views.process_feedback')
    def test_success_feedback(self, mock):
        """Test a successful request"""
        with open(os.path.join(
            self.path, 'json/example_click.json')) as json_file:
            file_content = json_file.read()

            self.view.handle_message(file_content, '')

            mock.delay.assert_called_once_with(json.loads(file_content))
