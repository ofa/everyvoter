"""Models for user import API"""
import uuid

from django.core.validators import FileExtensionValidator
from django.db import models

from branding.mixins import OrganizationMixin
from kennedy_common.utils.models import TimestampModel
from kennedy_common.utils.storages import HighValueStorage


RECORD_STATUSES = (
    ('success', 'Succeeded'),
    ('failed', 'Failed')
)

IMPORT_STATUSES = (
    ('pending', 'Pending'),
    ('failed', 'Failed'),
    ('ingesting', 'Ingesting'),
    ('creating', 'Creating Users'),
    ('finished', 'Finished')
)

IMPORT_ERROR_TYPES = (
    ('validation', 'Validation'),
    ('exception', 'Exception')
)


class UserImport(TimestampModel, OrganizationMixin):
    """Import of Users"""
    name = models.CharField('Import Name', max_length=50)
    total_succeeded = models.IntegerField(
        'Total Users Created', editable=False, default=0)
    total_failed = models.IntegerField(
        'Total Failures', editable=False, default=0)
    ingested = models.IntegerField('Total Ingested', editable=False, default=0)
    status = models.CharField('Status', max_length=50, choices=IMPORT_STATUSES)
    file = models.FileField(
        verbose_name='Source File',
        upload_to='user_imports/',
        storage=HighValueStorage(),
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    default = models.BooleanField(
        verbose_name='Default API Import', default=False, editable=False)
    uploader = models.ForeignKey('accounts.User', null=True)
    note = models.TextField(null=True, default=False)

    class Meta(object):
        """Meta options for model"""
        verbose_name = "User Import"
        verbose_name_plural = "User Imports"
        ordering = ['-modified_at']

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
    email = models.TextField(null=True)
    address = models.TextField(null=True)

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
    user_import = models.ForeignKey(UserImport)
    status = models.CharField(choices=RECORD_STATUSES, max_length=50)
    note = models.TextField(null=True)
    error_type = models.CharField(max_length=100, null=True)
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
