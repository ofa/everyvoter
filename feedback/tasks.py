"""Tasks related to processing email feedback"""
from email.utils import parseaddr

from celery import shared_task
import newrelic.agent

from accounts.models import User
from mailer.models import EmailActivity, Unsubscribe


def int_return(number):
    """If is integer, return the integer, otherwise return the input"""
    if number:
        return int(number)
    return number


def process_tags(tags):
    """Process the tags from a response"""
    organization_id = int_return(tags.get("organization_id", [None])[0])
    email_id = int_return(tags.get("email_id", [None])[0])
    recipient_id = int_return(tags.get("recipient_id", [None])[0])

    return organization_id, email_id, recipient_id


def extract_email(mail):
    """Extract the email address from the mail part of a notice"""
    return parseaddr(mail['commonHeaders']['to'][0])[1]


# pylint: disable=too-many-arguments
def global_unsubscribe(address, origin, reason='', organization_id=None,
                       email_id=None, recipient_id=None):
    """Create a global unsubscription

    Create an unsubscription that unsubscribes the user from emails from all
    organizations using the platform. This is usually due to a bounce or
    complaint where our ESP would not only refuse to send the email again but
    may even penalize us for attempting to send to again.

    Args:
        address: email address
        origin: origin of the unsubscribe ('bounce' or 'complaint')
        reason: reason to be listed (default: {''})
        organization_id: ID of the organization (default: {None})
        email_id: ID of the Email (default: {None})
        recipient_id: ID of the recpient (default: {None})
    """
    Unsubscribe(
        organization_id=organization_id,
        address=address,
        email_id=email_id,
        user_id=recipient_id,
        origin=origin,
        reason=reason,
        global_unsub=True
    ).save()

    User.objects.filter(email__iexact=email).update(unsubscribed=True)


@shared_task
def process_feedback(data):
    """Task to process feedback from SES delivered via SNS

    SES delivers feedback (such as bounces, complaints, clicks, and opens) via
    SNS. We pass that to this task so we have a bit more control over writes to
    our database (too many writes? scale down the workers. extra capacity?
    scale em up!)

    Args:
        data: SNS message body (in python dictionary format)
    """
    mail = data['mail']
    tags = mail['tags']

    address = extract_email(mail)
    organization_id, email_id, recipient_id = process_tags(tags)

    newrelic.agent.add_custom_parameter('email_id', email_id)
    newrelic.agent.add_custom_parameter('organization_id', organization_id)
    newrelic.agent.add_custom_parameter('recipient_id', recipient_id)

    # Start the process of generating a new EmailActivity by creating one but
    # not saving it to the database.
    email_activity = EmailActivity(
        message_id=mail['messageId'],
        email_id=email_id,
        recipient_id=recipient_id)

    if data['eventType'] == 'Complaint':
        activity = 'complaint'
        reason = 'Complaint'
    elif (data['eventType'] == 'Bounce' and
          data['bounce']['bounceType'] == 'Permanent'):
        activity = 'bounce'
        reason = data['bounce']['bouncedRecipients'][0].get(
            'diagnosticCode', '')[:255]
    elif (data['eventType'] == 'Bounce' and
          data['bounce']['bounceType'] == 'Transient'):
        activity = 'soft_bounce'
    elif data['eventType'] == 'Click':
        activity = 'click'
        email_activity.link = data['click']['link'][:500]
    elif data['eventType'] == 'Open':
        activity = 'open'
    else:
        return

    # Attach an activity to our EmailActivity and save it to the database
    email_activity.activity = activity
    email_activity.save()

    # If the feedback is a hard bounce or complaint, creat a global
    # unsubscription
    if activity in ['bounce', 'complaint']:
        global_unsubscribe(address, activity, reason, organization_id,
                           email_id, recipient_id)
