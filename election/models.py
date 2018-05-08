"""Election-related Models"""
from django.db import models
from django.dispatch import receiver
from django.utils.functional import cached_property
from django.db.models.signals import post_save

from accounts.models import User
from branding.mixins import OrganizationMixin
from everyvoter_common.utils.models import TimestampModel, UUIDModel
from election.choices import DISTRICT_TYPES, ELECTION_TYPES, STATES


class State(TimestampModel):
    """A US State or Territory"""
    code = models.CharField(
        'Code', max_length=2, choices=[(x, x) for x, y in STATES],
        primary_key=True, editable=False)
    name = models.CharField(
        'Name', max_length=50)
    is_state = models.BooleanField(
        help_text='Whether locale is a state')
    senate_2018 = models.BooleanField(
        help_text='Whether at least 1 U.S. Senate seat in the state will '
                  'appear on the general election ballot')
    governor_2018 = models.BooleanField(
        help_text='Whether the state\'s Governor\'s seat will appear on the '
                  'general election ballot')
    has_vr = models.BooleanField(help_text='Whether the state registers '
                                           'voters (North Dakota doesn\'t)')
    automatic_vr = models.BooleanField(
        help_text='Whether the state offers automatic voter registration')
    online_vr = models.BooleanField(
        help_text='Whether the state offers online voter registration')
    same_day_vr = models.BooleanField(
        help_text='Whether the state offers same day voter registration, '
                  'defined here as the ability to register to vote and also '
                  'cast a vote prior to election day')
    eday_vr = models.BooleanField(
        help_text='Whether the state offers election day voter registration, '
                  'defined here as the ability to register to vote and also '
                  'cast a vote on election day')
    early_vote_in_person = models.BooleanField(
        help_text='Whether the state offers some form of voting prior to '
                  'election day via a personal appearance')
    in_person_absentee = models.BooleanField(
        help_text='Whether the only form of voting prior to election day via '
                  'personal appearance is at a single location per jurisdiction'
    )
    early_vote_by_mail = models.BooleanField(
        help_text='Whether the state allows for voting by mail prior to '
                  'election day')
    early_vote_by_mail_fault = models.BooleanField(
        help_text='Whether there are restrictions as to who can vote by mail '
                  'prior to election day')
    early_vote_by_county = models.BooleanField(
        help_text='Whether the availability or dates of early votes is '
                  'county-by-county')
    perm_absentee = models.BooleanField(
        help_text='Whether the state offers a permanent absentee option in '
                  'which a voter can either elect (or will automatically '
                  'receive) a mail ballot')
    election_calendar_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)

    class Meta(object):
        """Meta options for State"""
        verbose_name = "State"
        verbose_name_plural = "States"
        ordering = ['name']

    def __unicode__(self):
        return self.name


class LegislativeDistrict(TimestampModel):
    """A district with an OCD ID"""
    name = models.CharField('Name', max_length=150)
    state = models.ForeignKey(State)
    ocd_id = models.CharField('OCD ID', max_length=100)
    district_type = models.CharField(
        'District Type', choices=DISTRICT_TYPES, max_length=50)

    def __unicode__(self):
        """String representation of a Civic District"""
        return self.name


class Election(TimestampModel):
    """An election"""
    election_type = models.CharField(
        'Election Type', choices=ELECTION_TYPES, max_length=50)
    voting_districts = models.ManyToManyField(
        LegislativeDistrict,
        verbose_name='Voting Districts',
        help_text='One or more districts voting in the election (i.e. who '
                  'should get information about this election)')
    state = models.ForeignKey(
        State, help_text='State under whose rules the election follows.')
    election_date = models.DateField('Election Date')
    vr_deadline = models.DateField(
        'Voter Registration Deadline',
        null=True, blank=True, # North Dakota does not have voter registration
        help_text='The deadline by which voters in the state must register to '
                  'vote')
    vr_deadline_online = models.DateField(
        'Online Voter Registration Deadline',
        null=True, blank=True,
        help_text='The explicit deadline by which voters in the state must '
                  'register to vote online in order to vote')
    evip_start_date = models.DateField(
        'Early Vote In-Person Start Date',
        null=True, blank=True,
        help_text='The date in which early voting in person begins in the '
                  'state')
    evip_close_date = models.DateField(
        'Early Vote In-Person Close Date',
        null=True, blank=True,
        help_text='The date that early voting in person ends in the state')
    vbm_application_deadline = models.DateField(
        'Vote By Mail Application Deadline',
        help_text='the date by which voters must return their applications '
                  'applying to vote by mail', null=True, blank=True)
    vbm_return_date = models.DateField(
        'Vote By Mail Ballot Return Date',
        help_text='The date by which voters must return their mailed ballots',
        null=True, blank=True)
    ev_notes = models.TextField(blank=True)
    vr_notes = models.TextField(blank=True)

    def __unicode__(self):
        """String representation of Election"""
        return "{state} {election_type} Election".format(
            state=self.state, election_type=self.get_election_type_display())


class OrganizationElection(TimestampModel, UUIDModel, OrganizationMixin):
    """Many to many join table of elections an org is participating in"""
    election = models.ForeignKey(Election)
    email_wrapper = models.ForeignKey('mailer.EmailWrapper')
    vbm_active = models.BooleanField(
        'Vote By Mail Notifications', default=True)
    evip_active = models.BooleanField(
        'Early Vote In Person Notifications', default=True)
    vr_active = models.BooleanField(
        'Voter Registration Notifications', default=True)
    eday_active = models.BooleanField(
        'Election Day Notifications', default=True)

    class Meta(object):
        """Meta options for OrganizationElection"""
        unique_together = ['organization', 'election']

    @property
    def recipients(self):
        """Recipients of emails about this election"""
        districts = self.election.voting_districts.values('pk')
        return User.objects.filter(
            location__districts__id__in=districts,
            unsubscribed=False,
            organization=self.organization).distinct()

    @cached_property
    def total_recipients(self):
        """Total number of recipients email is sent to"""
        return self.recipients.count()


@receiver(post_save, sender=Election)
def process_election(sender, instance, **kwargs):
    """Process a saved election"""
    if kwargs['created']:
        from election.utils import sync_elections
        sync_elections()
