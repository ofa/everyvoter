"""Rendering Related Tasks"""
from celery import shared_task
from email.utils import formataddr

from rendering.render_email import compose_email
from mailer.mailserver import deliver


@shared_task
def sample_email(to_address, user_id, email_id, election_id, district_ids):
    """Sample an email to an end user"""
    result = compose_email(
        user_id,
        email_id,
        election_id,
        district_ids)

    final_from_address = formataddr(
        (result['from_name'], result['from_address']))

    final_subject = u'Sample: {}'.format(result['subject'])

    deliver(
        to_address=to_address,
        from_address=final_from_address,
        subject=final_subject,
        html=result['body'])
