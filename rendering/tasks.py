"""Rendering Related Tasks"""
from celery import shared_task
import newrelic.agent

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

    newrelic.agent.add_custom_parameter(
        'organization_id', result['organization_id'])
    newrelic.agent.add_custom_parameter(
        'email_id', result['email_id'])

    final_subject = u'[sample] {}'.format(result['subject'])

    deliver(
        to_address=to_address,
        from_address=result['from_address'],
        subject=final_subject,
        html=result['body'])
