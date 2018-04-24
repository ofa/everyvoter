"""Models for Mailer"""
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.functional import cached_property
from django.template import Template
from django_smalluuid.models import SmallUUIDField, uuid_default

from branding.mixins import OrganizationMixin
from rendering.validators import validate_template
from everyvoter_common.utils.models import TimestampModel, UUIDModel
from election.choices import DEADLINES, ELECTION_TYPES


POSSIBLE_ACTIVITIES = (
    ('send', 'Sent'),
    ('bounce', 'Bounce'),
    ('soft_bounce', 'Soft Bounce'),
    ('complaint', 'Complaint'),
    ('open', 'Open'),
    ('click', 'Click')
)

UNSUBSCRIBE_ORIGINS = (
    ('user', 'Manual'),
    ('bounce', 'Bounce'),
    ('complaint', 'Complaint')
)


class SendingAddress(TimestampModel):
    """Address an email can be sent from. May need to be whitelisted by ESP"""
    # We assign organization manually instead of using the mixin because in the
    # mixin the field is not editable, and we need it to be editable in the
    # Django admin.
    organization = models.ForeignKey(
        'branding.Organization', db_index=True, null=True, blank=True,
        related_name='eligible_addresses')
    address = models.EmailField('Email Address')

    def __unicode__(self):
        """Unicode representation of the address"""
        return self.address


class EmailWrapper(TimestampModel, UUIDModel, OrganizationMixin):
    """Template for email"""
    name = models.CharField('Name', max_length=50)
    header = models.TextField('Header', validators=[validate_template])
    footer = models.TextField('Footer', validators=[validate_template])
    default = models.BooleanField('Default', default=False)

    class Meta(object):
        """Meta options for EmailTemplate object"""
        verbose_name = "Email Wrapper"
        verbose_name_plural = "Email Wrappers"

    def __unicode__(self):
        """Unicode representation of the template"""
        return self.name

    def save(self, *args, **kwargs):
        """Save the EmailWrapper"""

        # This should be stopped earlier, but test the email to prevent us from
        # ever saving an invalid template. This will raise a TemplateSyntaxError
        # if there is an obvious bug in the template. We should also run this
        # test as a verification in any view that edits this model.
        Template(self.header + u' ' + self.footer)

        # Only one email can be "default"
        if self.default:
            # select all other default items
            queryset = EmailWrapper.objects.filter(
                organization=self.organization, default=True)
            # except self (if self already exists)
            if self.pk:
                queryset = queryset.exclude(pk=self.pk)
            # and deactive them
            queryset.update(default=False)

        return super(EmailWrapper, self).save(*args, **kwargs)


class EmailTags(TimestampModel, OrganizationMixin):
    """Tags for emails"""
    name = models.CharField('Name', max_length=50)


class Email(TimestampModel, UUIDModel, OrganizationMixin):
    """Email

    An "Email" is either a template of an upcoming email, or the historical
    record of a past email.
    """
    subject = models.CharField('Subject Line', max_length=100,
                               validators=[validate_template])
    pre_header = models.CharField('Pre-Header Text', null=True, blank=True,
                                  max_length=100,
                                  validators=[validate_template])
    from_name = models.CharField('From Name', max_length=50)
    body_above = models.TextField(verbose_name='Email Body Above', blank=True,
                                  validators=[validate_template])
    body_below = models.TextField(verbose_name='Email Body Below', blank=True,
                                  validators=[validate_template])
    tags = models.ManyToManyField('mailer.EmailTags', blank=True)
    blocks = models.ManyToManyField(
        'blocks.Block', through='blocks.EmailBlocks', blank=True)


class MailingTemplate(TimestampModel):
    """Email template to be sent"""
    name = models.CharField('Name', max_length=50)
    deadline_type = models.CharField(
        'Deadline Type', choices=DEADLINES, max_length=50)
    election_type = models.CharField(
        'Election Type', choices=ELECTION_TYPES, max_length=50)
    days_to_deadline = models.IntegerField('Days to Deadline', default=0)
    email = models.OneToOneField('mailer.Email')


    class Meta(object):
        """Meta options for template"""
        verbose_name = "Template"
        verbose_name_plural = "Templates"


class Mailing(TimestampModel):
    """Siingle mailing from the app"""
    organization_election = models.ForeignKey(
        'election.OrganizationElection')
    template = models.ForeignKey('mailer.MailingTemplate')
    from_email = models.EmailField('From Email')
    stats = JSONField('Stats', null=True)
    source = models.CharField('Source Code', max_length=100)
    count = models.IntegerField(verbose_name='Recipients', default=0)
    email = models.OneToOneField('mailer.Email')

    class Meta(object):
        """Meta details about the Mailing model"""
        verbose_name = "Mailing"
        verbose_name_plural = "Mailings"

    @cached_property
    def election(self):
        """Election email is related to"""
        return self.organization_election.election

    @cached_property
    def state(self):
        """State the election is in"""
        return self.election.state


class EmailActivity(TimestampModel):
    """Single activity related to an email"""
    message_id = models.CharField('Message ID from ESP', max_length=100)
    mailing = models.ForeignKey(Mailing, null=True)
    recipient = models.ForeignKey('accounts.User', null=True)
    activity = models.CharField(
        'Action Type', choices=POSSIBLE_ACTIVITIES, max_length=50)
    link = models.CharField(
        'Click URL', max_length=500, null=True, default=None)

    class Meta(object):
        """Meta options for EmailActivity model"""
        verbose_name = "Email Activity"
        verbose_name_plural = "Email Activities"


class UnsubscribeManager(models.Manager):
    """Manager for Unsubscribe model"""
    def check_global(self, email):
        """Check to see if an email is globally unsubscribed"""
        return self.get_queryset().filter(
            email__iexact=email, global_unsub=True).exists()


class Unsubscribe(TimestampModel, UUIDModel):
    """Unsubscription"""
    organization = models.ForeignKey(
        'branding.Organization', editable=False, db_index=True, null=True)
    email = models.EmailField()
    user = models.ForeignKey('accounts.User', null=True)
    mailing = models.ForeignKey(Mailing, null=True)
    origin = models.CharField(
        choices=UNSUBSCRIBE_ORIGINS, max_length=50)
    reason = models.CharField('Reason', max_length=255, blank=True)
    global_unsub = models.BooleanField('Applies Globally', db_index=True)

    objects = UnsubscribeManager()

    class Meta(object):
        """Meta options for Unsubscribe model"""
        verbose_name = "Unsubscribe"
        verbose_name_plural = "Unsubscribes"

    def __unicode__(self):
        return self.email
