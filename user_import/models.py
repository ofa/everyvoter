"""Models for user import API"""
import uuid
import os

from django.db import models

from branding.mixins import OrganizationMixin
from kennedy_common.utils.models import TimestampModel
from kennedy_common.utils.storages import AttachmentStorage


RECORD_STATUSES = (
    ('success', 'Succeeded'),
    ('failed', 'Failed')
)


class UserImport(TimestampModel, OrganizationMixin):
    """Import of Users"""
    name = models.CharField('Name', max_length=50)
    count = models.IntegerField('Total Records', editable=False, default=0)
    file = models.FileField(
        upload_to='user_imports/',
        storage=AttachmentStorage(),
        null=True)
    default = models.BooleanField(
        verbose_name='Default API Import', default=False, editable=False)

    class Meta(object):
        """Meta options for model"""
        verbose_name = "User Import"
        verbose_name_plural = "User Imports"

    def __unicode__(self):
        """Unicode representation of the import"""
        return self.name


class ImportRecord(models.Model):
    """Raw data from an import file"""
    # pylint: disable=invalid-name
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_import = models.ForeignKey(UserImport)
    first_name = models.TextField(null=True)
    last_name = models.TextField(null=True)
    email = models.TextField()
    address = models.TextField()

    class Meta(object):
        """Meta obtions for model"""
        verbose_name = "Import Record"
        verbose_name_plural = "Import Records"

    def __unicode__(self):
        """Unicode representation of the import record"""
        return self.email


class ImportRecordStatus(TimestampModel):
    """Status of the import of a specific user"""
    import_record = models.OneToOneField(ImportRecord)
    status = models.CharField(choices=RECORD_STATUSES, max_length=50)
    note = models.TextField(null=True)
    account = models.ForeignKey('accounts.User', null=True)

    class Meta(object):
        """Meta options for model"""
        verbose_name = "Import Record Status"
        verbose_name_plural = "Import Record Statuses"

    def __unicode__(self):
        """Unicode representation of the import record status"""
        if self.account:
            return unicode(self.account)
        else:
            return unicode(self.import_record)
