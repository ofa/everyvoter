"""Command to set a user to have all admin permissions"""
from django.core.management.base import BaseCommand, CommandError

from accounts.models import User


class Command(BaseCommand):
    """Command to turn a user into a staff user"""
    help = "Give a user with a specified email address staff access"

    def add_arguments(self, parser):
        """Add arguments to the management command"""
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
        """Handle command."""
        email = options['user_email'][0]
        organization_id = options['organization_id'][0]

        try:
            user = User.objects.get(
                email__iexact=email, organization_id=organization_id)
        except User.DoesNotExist:
            raise CommandError(u'User with email "{}" and organization {} does '
                               'not exist'.format(email, organization_id))

        if user.is_staff:
            raise CommandError(
                u'User {} is already a staff member'.format(user))

        # User will be made staff
        user.is_staff = True

        user.save()

        self.stdout.write(self.style.SUCCESS(
            'Successfully made "%s" a staff member' % user))
