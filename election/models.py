"""Election-related Models"""
from django.db import models

from branding.mixins import OrganizationMixin
from kennedy_common.utils.models import TimestampModel
from election.choices import DISTRICT_TYPES, ELECTION_TYPES, STATES


class State(TimestampModel):
    """A US State or Territory"""
    code = models.CharField(
        'Code', max_length=2, choices=[(x, x) for x, y in STATES],
        primary_key=True, editable=False)
    name = models.CharField(
        'Name', max_length=50)
    is_state = models.BooleanField()
    senate_2018 = models.BooleanField()
    governor_2018 = models.BooleanField()
    automatic_vr = models.BooleanField()
    online_vr = models.BooleanField()
    same_day_vr = models.BooleanField()
    eday_vr = models.BooleanField()
    early_vote_in_person = models.BooleanField()
    in_person_absentee = models.BooleanField()
    early_vote_by_mail = models.BooleanField()
    early_vote_by_mail_fault = models.BooleanField()
    perm_absentee = models.BooleanField()
    election_calendar_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)

    class Meta(object):
        """Meta options for State"""
        verbose_name = "State"
        verbose_name_plural = "States"

    def __str__(self):
        return self.name


class LegislativeDistrict(TimestampModel):
    """A district with an OCD ID"""
    name = models.CharField('Name', max_length=150)
    state = models.ForeignKey(State)
    ocd_id = models.CharField('OCD ID', max_length=100)
    district_type = models.CharField(
        'District Type', choices=DISTRICT_TYPES, max_length=50)

    def __str__(self):
        """String representation of a Civic District"""
        return self.ocd_id


class Election(TimestampModel):
    """An election"""
    election_type = models.CharField(
        'Election Type', choices=ELECTION_TYPES, max_length=50)
    state = models.ForeignKey(State)
    date = models.DateField()
    polls_open = models.CharField(blank=True, max_length=50)
    polls_close = models.CharField(blank=True, max_length=50)
    polls_notes = models.CharField(blank=True, max_length=100)

    def __str__(self):
        """String representation of Election"""
        return "{state} {election_type} Election".format(
            state=self.state, election_type=self.election_type)


class OrganizationElection(TimestampModel, OrganizationMixin):
    """Many to many join table of elections an org is participating in"""
    election = models.ForeignKey(Election)
    email_wrapper = models.ForeignKey('mailer.EmailWrapper')

    class Meta(object):
        """Meta options for OrganizationElection"""
        unique_together = ['organization', 'election']
