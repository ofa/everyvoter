"""Models for DemocracyWorks API consumer app"""
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.timezone import localtime

from everyvoter_common.utils.models import TimestampModel, UUIDModel


FIELD_CHOICES = [
    ('election_date', 'Election Date'),
    ('vr_deadline', 'Voter Registration Deadline'),
    ('vr_deadline_online', 'Online Voter Registration Deadline'),
    ('evip_start_date', 'Early Vote In-Person Start Date'),
    ('evip_close_date', 'Early Vote In-Person Close Date'),
    ('vbm_application_deadline', 'Vote By Mail Application Deadline'),
    ('vbm_return_date', 'Vote By Mail Ballot Return Date')
]


class Response(UUIDModel, TimestampModel):
    """Democracy Works API Response"""
    data = JSONField()
    elections = models.ManyToManyField('election.Election')

    class Meta(object):
        """Meta options for model"""
        verbose_name = "API Response"
        verbose_name_plural = "API Responses"
        ordering = ['-created_at']

    def __unicode__(self):
        """Unicode representation of api"""
        return u"{} Response".format(
            localtime(self.created_at).strftime("%b %d %Y %H:%M:%S"))


class DateChange(TimestampModel):
    """Date Change"""
    field = models.CharField(choices=FIELD_CHOICES, max_length=50)
    election = models.ForeignKey('election.Election')
    response = models.ForeignKey(Response)
    old_date = models.DateField(null=True)
    new_date = models.DateField(null=True)

    class Meta(object):
        """Meta options for model"""
        verbose_name = "Change"
        verbose_name_plural = "Changes"
        unique_together = ('field', 'response', 'election')
        ordering = ('response', 'election__state', 'field')

    def __unicode__(self):
        """Unicode representation of the change"""
        return u"{} Change from {} to {}".format(
            self.field, self.old_date, self.new_date)
