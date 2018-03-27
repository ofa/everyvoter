"""Management command to change password

Overrides existing changepassword command from django.contrib.auth"""
from __future__ import unicode_literals

import getpass

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.utils.encoding import force_str

from accounts.models import User


class Command(BaseCommand):
    """Change Password Command"""
    help = "Change a user's password."
    requires_migrations_checks = True
    requires_system_checks = False

    def _get_pass(self, prompt="Password: "):
        """Get the password from the command prompt"""
        password = getpass.getpass(prompt=force_str(prompt))
        if not password:
            raise CommandError("aborted")
        return password

    def add_arguments(self, parser):
        """Add arguments to the command"""
        parser.add_argument(
            'organization_id',
            nargs=1,
            type=int,
            help='Primary key of user\'s organization')
        parser.add_argument(
            'user_email',
            nargs=1,
            type=str,
            help='Email address of user')

    def handle(self, *args, **options):
        """Handle execution of the management command"""
        email = options['user_email'][0]
        organization_id = options['organization_id'][0]

        try:
            user = User.objects.get(
                email__iexact=email, organization_id=organization_id)
        except User.DoesNotExist:
            raise CommandError(u'User with email "{}" and organization {} does '
                               'not exist'.format(email, organization_id))

        self.stdout.write("Changing password for user '%s'\n" % user)

        # pylint: disable=invalid-name
        MAX_TRIES = 3
        count = 0
        p1, p2 = 1, 2  # To make them initially mismatch.
        password_validated = False
        while (p1 != p2 or not password_validated) and count < MAX_TRIES:
            p1 = self._get_pass()
            p2 = self._get_pass("Password (again): ")
            if p1 != p2:
                self.stdout.write("Passwords do not match. Please try again.\n")
                count += 1
                # Don't validate passwords that don't match.
                continue
            try:
                validate_password(p2, user)
            except ValidationError as err:
                self.stderr.write('\n'.join(err.messages))
                count += 1
            else:
                password_validated = True

        if count == MAX_TRIES:
            raise CommandError("Aborting password change for user '%s' after %s"
                               " attempts" % (user, count))

        user.set_password(p1)
        user.save()

        return "Password changed successfully for user '%s'" % user
