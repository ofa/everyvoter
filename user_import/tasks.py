"""Import-Related Tasks"""
import unicodecsv
import uuid
import time

from celery import shared_task
from django.core.exceptions import ValidationError
from django.conf import settings
import requests

from user_import.models import UserImport, ImportRecord, ImportRecordStatus
from accounts.utils_user import create_user
from mailer.mailserver import deliver



def load_file(file_field):
    """Generate the path to a local file for a filefield

    Working with local files is great! You can scan through them easily and
    manipulate them much faster than if they're remote objects. There are two
    ways a file in django could be local: it could be part of a local-based
    storage (and thus have a `path` attribute) or it could be downloaded and
    put into a temporary folder. This function addresses both instances.

    Args:
        file_field: a file field on an object

    Returns:
        path to file
        string
    """
    try:
        return file_field.path
    except NotImplementedError:
        filename = '/tmp/{uuid}'.format(uuid=uuid.uuid4())
        request = requests.get(file_field.url, stream=True)
        with open(filename, 'wb') as file_obj:
            for chunk in request.iter_content(chunk_size=1024):
                if chunk:
                    file_obj.write(chunk)
        return filename


@shared_task
def ingest_import(user_import_id):
    """Ingest an import file"""
    user_import = UserImport.objects.get(pk=user_import_id)

    user_import.status = 'ingesting'
    user_import.save()

    ingested_count = 0

    try:
        filename = load_file(user_import.file)

        with open(filename, 'rb') as file_obj:
            reader = unicodecsv.DictReader(file_obj, encoding='utf-8-sig')
            if reader.fieldnames != [u'first_name',
                                     u'last_name',
                                     u'email',
                                     u'address']:
                raise Exception('Invalid fields.')

            for row in reader:
                ImportRecord(
                    user_import=user_import,
                    first_name=row.get('first_name', ''),
                    last_name=row.get('last_name', ''),
                    email=row.get('email', ''),
                    address=row.get('address', '')).save()
                ingested_count += 1

        user_import.ingested = ingested_count
        user_import.save()
        trigger_import.delay(user_import.pk)
    except Exception as error:
        user_import.status = 'failed'
        user_import.note = unicode(error)
        user_import.save()
        alert_failed_import.delay(user_import.pk)
        raise


@shared_task
def alert_failed_import(user_import_id):
    """Alert someone that an import failed"""
    user_import = UserImport.objects.get(pk=user_import_id)
    deliver(
        user_import.uploader.email,
        settings.DEFAULT_FROM_EMAIL,
        u'Import Processing Failure {}'.format(user_import.name),
        user_import.note)


@shared_task
def trigger_import(user_import_id):
    """Queue up all pending records that need to be imported"""

    imported_records = ImportRecordStatus.objects.filter(
        user_import_id=user_import_id).values_list(
            'import_record_id', flat=True)

    import_records = ImportRecord.objects.filter(
        user_import_id=user_import_id).exclude(
            id__in=imported_records).only('pk')

    total_records = import_records.count()

    UserImport.objects.filter(id=user_import_id).update(status='creating')

    current_record = 1
    for record in import_records:
        if current_record == total_records:
            final = True
        else:
            final = False

        import_user.delay(record.pk, current_record, final)

        current_record += 1


@shared_task
def import_user(import_record_id, current_record, final=False):
    """Import a specific user"""
    import_record = ImportRecord.objects.select_related(
        'user_import', 'user_import__organization').get(pk=import_record_id)

    status_record = ImportRecordStatus()
    status_record.user_import_id = import_record.user_import_id
    status_record.import_record = import_record

    # Overly broad exception handling system to handle all possible exceptions.
    # We're basically logging exceptions to the database instead of to stdout
    # or NewRelic, because digging through NewRelic to try to address issues
    # would be a nightmare. We should clean this up later.
    # pylint: disable=broad-except
    try:
        status_record.account = None
        status_record.status = 'success'
        status_record.account = create_user(
            import_record.user_import.organization,
            import_record.email,
            import_record.address,
            import_record.first_name,
            import_record.last_name)

    except ValidationError as error:
        status_record.status = 'failed'
        status_record.error_type = 'ValidationError'
        status_record.account = None
        status_record.note = unicode(error.message)

    except Exception as error:
        status_record.status = 'failed'
        status_record.error_type = type(error)
        status_record.note = unicode(error.message)
        status_record.account = None

    status_record.save()

    # Every 250 records or on the final record update the status of the job
    if not current_record % 250 or final:
        user_import = import_record.user_import

        # If it's the final record, sleep for 10 seconds to let other tasks
        # complete
        if final:
            time.sleep(10)
            user_import.status = 'finished'

        all_import_statuses = ImportRecordStatus.objects.filter(
            user_import=user_import)
        user_import.total_succeeded = all_import_statuses.filter(
            status='success').count()
        user_import.total_failed = all_import_statuses.filter(
            status='failed').count()

        import_record.user_import.save()
