"""Secure storage backends for Kennedy

Swiped from Connect, because this should only ever be written once.
"""
# pylint: disable=no-init

from datetime import datetime
from smalluuid.smalluuid import SmallUUID

from django.conf import settings
from django.core.files.storage import get_storage_class


# pylint: disable=invalid-name
AttachmentStorageEngine = get_storage_class(
    import_path=getattr(
        settings,
        'ATTACHMENT_STORAGE_ENGINE',
        # We have to define a fallback of the FileSystemStorage here because
        # `get_storage_class`, by default, will attempt to make our
        # `AttachmentStorage` inherit from itself.
        'django.core.files.storage.FileSystemStorage')
)


def uniqify_filename(filename):
    """Generate a unique filename that maintains the extension"""
    return '{unique}.{existing_filename}'.format(
        unique=unicode(SmallUUID())[:5], existing_filename=filename)


def setting(name, default=None):
    """
    Helper function to get a Django setting by name or (optionally) return
    a default (or else ``None``).
    """
    return getattr(settings, name, default)



class AttachmentStorage(AttachmentStorageEngine):
    """AttachmentStorage is a secure django storage for all file attachments"""

    def get_available_name(self, name, max_length=None):
        """
        In order to prevent file overwriting one another this will generate
        a new filename with the format `YYMMDD.uniquehash.filename.extension`
        """
        # Set the format of our filename
        filename_format = '{path}/{date}.{filename}'

        # If the storage engine is S3, call _clean_name() to clean the name
        try:
            clean_name = self._clean_name(name)
        except AttributeError:
            clean_name = name

        # Generate the YYMMDD formatted date
        date = datetime.now().strftime('%y%m%d')

        # rsplit the filename on '/' so we have a 2 value list of
        # the path and filename
        splitname = clean_name.rsplit('/', 1)

        # Compile all the relevant strings to generate the full path/filename
        final_name = filename_format.format(
            path=splitname[0],
            date=date,
            filename=uniqify_filename(splitname[1])
        )
        return final_name


class HighValueStorage(AttachmentStorage):
    """
    A custom storage that, when attached to boto, will use object access
    control to make uploaded assets protected
    """

    default_acl = 'private'
    secure_urls = True
    bucket_name = settings.AWS_PRIVATE_STORAGE_BUCKET_NAME

    # We have to override any `custom_domain` set in the settings file
    # because our storage engine will take that setting as a signal that all
    # files have a 'public' ACL
    custom_domain = None

    querystring_expire = settings.AWS_PRIVATE_STORAGE_EXPIRATION
    querystring_auth = True
