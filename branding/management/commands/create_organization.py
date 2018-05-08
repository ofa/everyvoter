"""Command to create a new organization"""
from django.core.management.base import BaseCommand

from branding.utils import get_or_create_organization


class Command(BaseCommand):
    """Command to create a new organization"""
    help = "Create a new organization"

    def handle(self, *args, **options):
        """Handle command."""

        org_name = raw_input('Enter the name of the organization: ')
        platform_name = raw_input('Enter the name of the platform: ')
        hostname = raw_input('Enter the default hostname of the platform: ')
        homepage = raw_input('Enter the organization\'s homepage: ')

        new_organization, _ = get_or_create_organization(
            org_name, platform_name, hostname, homepage)

        self.stdout.write(self.style.SUCCESS(
            'New platform "{platform_name}" made with ID "{id}"'.format(
                platform_name=new_organization.platform_name,
                id=new_organization.pk)))
