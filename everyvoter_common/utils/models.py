"""Utility models for whatsnext"""
from django.db import models
from django.utils.text import slugify
from django_smalluuid.models import SmallUUIDField, uuid_default


class CacheMixinModel(object):
    """
    Mixin which generates a cache key for an object
    This is a mixin which you can use to generate a unique key for key/value
    cache purposes on an object-by-object basis.
    """
    MODEL_REVISION_NUMBER = 1

    class Meta(object):
        """Meta info for TimeStamp abstract model"""
        abstract = True

    def cache_key(self):
        """
        Generate a cache key for the model
        We put this in TimeStampModel because it's reliant on modified_at,
        plus it's the easiest way to show up across the app
        """
        key = u"modelkey {app} {model} {revision} {pk} {modified}".format(
            app=self._meta.app_label,
            model=self._meta.model_name,
            revision=self.MODEL_REVISION_NUMBER,
            pk=self.pk,
            modified=self.modified_at)
        return slugify(key)


class TimestampModel(CacheMixinModel, models.Model):
    """
    Abstract model that adds created_at, modified_at and the cache_key property
    """
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta(object):
        """Meta info for TimeStamp abstract model"""
        abstract = True


class UUIDModel(models.Model):
    """Abstract model that adds a UUID Field"""
    uuid = SmallUUIDField(default=uuid_default(), editable=False,
                          db_index=True)

    class Meta(object):
        """Meta info for TimeStamp abstract model"""
        abstract = True
