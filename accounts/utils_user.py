"""Utilities related to creating users"""
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

from accounts.models import User
from location.utils import get_location
from location.models import UserLocation


def create_user(organization, email, address, first_name, last_name):
    """Create a new user

    Function to create a new user on Kennedy

    Args:
        organization: Organization
        email: Email address of new user
        address: Street Address of new user
        first_name: First name of user (optional)
        last_name: Last name of new user (optional)
    """

    # Run the email through the email validator incase someone puts their
    # address in the email field
    email_validator = EmailValidator('Invalid Email Address')
    email_validator(email)

    # Check to see if the user already exists. We retain the case of emails but
    # only allow 1 email in the system regardless of capitalization, thus the
    # use of `__iexact`. Raise our custom `UserExists` error for easy exception
    # handling elsewhere.
    if User.objects.filter(
            organization=organization, email__iexact=email).exists():
        raise ValidationError('User with that email address already exists')

    # Return a Location for this user. This either creates a new Location or
    # finds an existing one. This also does all our geocode magic.
    location = get_location(address)

    user = User(
        organization=organization,
        first_name=first_name,
        last_name=last_name,
        email=email,
        location=location
    )
    user.save()

    # Attach the user to the location
    UserLocation(user=user, location=location).save()

    return user


def update_user_location(user, address):
    """Update the location of a user

    Update the details of an existing user

    Args:
        user: User object
        address: Address to change to
    """
    location = get_location(address)

    if location not in user.locations.all():
        UserLocation.objects.create(
            user=user, location=location)

    user.location = location
    user.save()
