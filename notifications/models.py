"""Models for the block functionality"""
from django.db import models

from everyvoter_common.utils.models import TimestampModel, UUIDModel


class NotificationSettingManager(models.Manager):
    """Manager for NotificationSetting model."""
    def get_queryset(self):
        """
        Ensures that all queries for NotificationSettings also query the user
        """
        return super(NotificationSettingManager, self).get_queryset(
            ).select_related('user')


class NotificationSetting(TimestampModel, UUIDModel):
    """Notification settings for an individual user"""
    user = models.OneToOneField('accounts.User')
    daily_batch_sample = models.BooleanField(
        'Sample All Emails Daily', default=False)

    objects = NotificationSettingManager()

    class Meta(object):
        """Meta options for model"""
        verbose_name = "Notification Setting"
        verbose_name_plural = "Notification Settings"

    def __unicode__(self):
        return unicode(self.user)
