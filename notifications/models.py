"""Models for the block functionality"""
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from accounts.models import User
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


@receiver(post_save, sender=User)
def process_saved_staff(sender, instance, **kwargs):
    """When a staff member is saved, ensure there is a NotificationSetting"""
    if instance.is_staff:
        NotificationSetting.objects.get_or_create(user=instance)
