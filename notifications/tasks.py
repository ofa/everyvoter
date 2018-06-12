"""Rendering Related Tasks"""
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from accounts.models import User
from mailer.send_calendar import mailing_calendar
from rendering.tasks import sample_email


@shared_task
def daily_sample_batch():
    """Bulk email samples of tomorrow's emails to users who opted in"""

    tomorrow = timezone.localtime() + timedelta(days=1)
    tomorrow_emails = mailing_calendar(date=tomorrow)

    for email in tomorrow_emails:
        users = User.objects.filter(
            notificationsetting__daily_batch_sample=True,
            organization_id=email.organization_id,
            is_staff=True).only('email', 'pk')

        for user in users:
            sample_email.delay(
                to_address=user.email,
                user_id=user.id,
                email_id=email.email_id,
                election_id=email.election_id,
                district_ids=None)
