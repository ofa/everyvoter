"""Tasks"""
import datetime

from celery import shared_task
from django.template.loader import render_to_string
from django.utils.timezone import now
import newrelic.agent

from .consumer import get_response, process_election
from .models import DateChange, Response as APIResponse
from accounts.models import User
from mailer.mailserver import deliver


@shared_task
def sync_elections():
    """Sync the elections"""
    # Get the API response object
    response = get_response()

    total_responses = len(response.data)

    if total_responses > 0:
        for list_number in range(0, total_responses):
            process_election_task.delay(
                response_id=response.pk, list_number=list_number)


@shared_task
def process_election_task(response_id, list_number):
    """Task to sync an individual election"""
    response = APIResponse.objects.get(pk=response_id)
    process_election(response, list_number)


@shared_task
def notify_changes(recipient_ids, days_back=1):
    """Notify users of the most recent changes"""
    date_from = now() - datetime.timedelta(days=days_back)
    recent_changes = DateChange.objects.filter(
        created_at__gte=date_from).select_related()

    if not recent_changes.exists():
        return

    # Only send changes to recipients that actually exist, don't trust the
    # args sent to this function.
    recipients = User.objects.filter(id__in=recipient_ids).only('id')

    for recipient in recipients:
        send_change_notification.delay(recipient.id, days_back)


@shared_task
def send_change_notification(recipient_id, days_back):
    """Send an individual change notification"""
    date_from = now() - datetime.timedelta(days=days_back)
    recent_changes = DateChange.objects.filter(
        created_at__gte=date_from).select_related()

    recipient = User.objects.select_related(
        'organization', 'organization__primary_domain',
        'organization__from_address').get(id=recipient_id)

    newrelic.agent.add_custom_parameter(
        'recipient_id', recipient.pk)
    newrelic.agent.add_custom_parameter(
        'organization_id', recipient.organization.pk)


    tags = {
        'recipient_id': recipient.pk,
        'organization_id': recipient.organization.pk
    }

    context = {
        'recent_changes': recent_changes,
        'recipient': recipient
    }
    changes_copy = render_to_string(
        'democracy_consumer/email/change_notification.html', context)

    deliver(to_address=recipient.email,
            from_address=recipient.organization.from_address.address,
            subject='Recent DemocracyWorks Changes',
            html=changes_copy,
            tags=tags)

