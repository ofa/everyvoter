"""Models for the Kennedy App"""
import uuid

from django.core.exceptions import PermissionDenied
from django.db import models
from django.contrib.auth import models as auth_models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from branding.mixins import OrganizationMixin, OrganizationManagerMixin
from kennedy_common.utils.models import TimestampModel


class UserManager(OrganizationManagerMixin, auth_models.BaseUserManager):
    """Manager for the User model."""
    def create_user(self, *args, **kwargs):
        """Disable Django's built-in user creation system

        Because by default Django is not multi-tenant aware, using the default
        create_user could open up problems. All users should be created using
        the web-based user creation flow, then promoted to a staff member.
        """

        raise PermissionDenied(
            "Users cannot be created using Django's built-in auth")

    def create_superuser(self, *args, **kwargs):
        """Override default create_superuser

        We immediately call create_user so that our PermissionDenied exception
        is run.
        """
        self.create_user(*args, **kwargs)


class User(
        TimestampModel, OrganizationMixin, auth_models.AbstractBaseUser,
        auth_models.PermissionsMixin):
    """Kenedy application user"""
    username = models.CharField(
        'Username', max_length=150, unique=True, default=uuid.uuid4,
        editable=False)

    is_staff = models.BooleanField(_('Staff Status'), default=False)
    is_active = models.BooleanField(_('Active'), default=True, db_index=True)

    email = models.EmailField(_('Email Address'), editable=False)
    first_name = models.CharField(_('First Name'), max_length=100, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=200, blank=True)

    locations = models.ManyToManyField(
        'location.Location', through='location.UserLocation')

    # The actual username field will be email, but we can't add a unique
    # constraint on email, while we can on username
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'organization']

    objects = UserManager()

    class Meta(object):
        """Meta options for the model"""
        unique_together = ('email', 'organization')

    def __unicode__(self):
        """Unicode representation of the user"""
        if self.first_name and self.last_name:
            return self.first_name + u' ' + self.last_name
        else:
            return self.email

    def get_short_name(self):
        """Short name representation of user"""
        return self.first_name

    @cached_property
    def location(self):
        """Location the user is in"""
        return self.locations.select_related('state').get(
            userlocation__is_active=True)

    @cached_property
    def state(self):
        """State the user is in"""
        return self.location.state
