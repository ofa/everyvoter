"""Models for user import API"""
import uuid
import os

from django.db import models

from branding.mixins import OrganizationMixin
from kennedy_common.utils.models import TimestampModel


RECORD_STATUSES = (
    ('success', 'Succeeded'),
    ('failed', 'Failed')
)


class UserImport(TimestampModel, OrganizationMixin):
    """Import of Users"""
    file = models.FileField(null=True)
    default = models.BooleanField(
        verbose_name='Default API Import', default=False, editable=False)

    class Meta(object):
        """Meta options for model"""
        verbose_name = "User Import"
        verbose_name_plural = "User Imports"

    def __unicode__(self):
        """Unicode representation of the import"""
        if self.file:
            return u"{created} {filename}".format(
                created=self.created_at, filename=os.path.basename(self.file.name))
        elif self.default:
            return "API Import"
        else:
            return "{created} {uuid}".format(
                created=self.created_at, uuid=self.id)


class ImportRecord(models.Model):
    """Raw data from an import file"""
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
