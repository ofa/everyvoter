"""Tests for the utils_user.py file in Accounts"""
from django.core.exceptions import ValidationError
from django.test import TestCase
from mock import patch

from accounts.models import User
from accounts.utils_user import create_user
from location.models import UserLocation
from everyvoter_common.utils.tests import EveryVoterTestMixin


class TestCreateUser(EveryVoterTestMixin, TestCase):
    """Test the create_user method"""
    def setUp(self):
        """Setup the test"""
        self.organization = self.create_organization()

    def test_invalid_email(self):
        """Test sending in an invalid email"""
        with self.assertRaises(ValidationError) as error:
            create_user(
                self.organization, 'fakeemail', '60657', 'First', 'Last')

        self.assertEqual(error.exception.message, u'Invalid Email Address')

    @patch('accounts.utils_user.get_location')
    def test_existing_user(self, mock):
        """Test a case where there is an existing user with the same email"""
        mock_location = self.create_location()
        mock.return_value = mock_location

        user = create_user(self.organization, 'validemail@localhost.com',
                           '60657', 'First', 'Last')

        self.assertTrue(UserLocation.objects.filter(
            user=user, location=mock_location).exists())

        with self.assertRaises(ValidationError) as error:
            create_user(self.organization, 'validemail@localhost.com',
                        '20009', 'First', 'Last')

        self.assertEqual(
            error.exception.message,
            u'User with that email address already exists')

    @patch('accounts.utils_user.get_location')
    def test_creates_user(self, mock):
        """Test that a new user is created"""
        mock_location = self.create_location()
        mock.return_value = mock_location

        user = create_user(self.organization, 'email@localhost.com',
                           '60657', 'First', 'Last')

        newuser = User.objects.get(pk=user.pk)

        self.assertEqual(newuser.organization, self.organization)
        self.assertEqual(newuser.email, 'email@localhost.com')
        self.assertEqual(newuser.first_name, 'First')
        self.assertEqual(newuser.last_name, 'Last')
        self.assertEqual(newuser.location, mock_location)

        # Verify creates UserLocation
        self.assertTrue(UserLocation.objects.filter(
            user=newuser, location=mock_location).exists())

        self.assertIn(mock_location, newuser.locations.all())
