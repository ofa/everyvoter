"""Mailer-related tasks"""
import time
import logging

from celery import shared_task
from django.utils import timezone
import newrelic.agent

from election.models import OrganizationElection
from mailer.mailserver import deliver
from mailer.models import Email, Mailing, EmailActivity, Unsubscribe
from mailer.send_calendar import mailing_calendar
from rendering.render_email import compose_email

logger = logging.getLogger('email')


@shared_task
def trigger_mailings():
    """Lookup all mailings expected for that day and trigger them"""
    today_calendar = mailing_calendar(
        date=timezone.localtime(), email_active=True)
    full_calendar = list(today_calendar)

    logger.info(u'Mailing Trigger Fired. Found %s items to send',
                len(full_calendar))

    # If the calendar is empty, this won't actually trigger anything
    for mailing in full_calendar:
        # Emails with 2 or less days from the deadline should be prioritized
        priority = max(3 - mailing.days_to_deadline, 0)
        initialize_mailing.apply_async(
            kwargs={
                'template_email_id': mailing.email_id,
                'organizationelection_id': mailing.organizationelection_id,
                'priority': priority
            },
            priority=priority
        )

        logger.info(u'Mailing Triggered. Template %s OElection %s Priority %s',
                    mailing.email_id, mailing.organizationelection_id,
                    priority)


@shared_task
def initialize_mailing(template_email_id, organizationelection_id, priority):
    """Hey fa"""
    source_email = Email.objects.select_related('mailingtemplate').get(
        id=template_email_id)
    source_org_election = OrganizationElection.objects.select_related(
        'organization', 'organization__from_address').get(
            pk=organizationelection_id)
    source_blocks = source_email.blocks.only('id')
    source_categories = source_email.categories.only('id')

    new_email = Email(
        organization=source_org_election.organization,
        subject=source_email.subject,
        pre_header=source_email.pre_header,
        from_name=source_email.from_name,
        body_above=source_email.body_above,
        body_below=source_email.body_below)
    new_email.save()

    new_email.blocks.set(source_blocks)
    new_email.categories.set(source_categories)

    new_mailing = Mailing(
        email=new_email,
        template=source_email.mailingtemplate,
        organization_election=source_org_election,
        from_email=source_org_election.organization.from_address.address,
        source='',
        status='pending')
    new_mailing.save()

    initialize_recipients.apply_async(
        kwargs={
            'email_id': new_email.id,
            'organizationelection_id': source_org_election.id,
            'priority': priority
        },
        priority=priority
    )

    logger.info(u'Mailing Initalized. Email %s OElection %s Org %s',
                new_mailing.pk, source_org_election.id,
                source_org_election.organization_id)

    newrelic.agent.add_custom_parameter('email_id', new_email.pk)
    newrelic.agent.add_custom_parameter(
        'organization_id', source_org_election.organization_id)


@shared_task
def initialize_recipients(email_id, organizationelection_id, priority):
    """Create recipients"""
    mailing = Mailing.objects.select_related('organization_election').get(
        email__id=email_id)
    orgelection = mailing.organization_election

    # Get a list of all recipients of an emails
    recipients = list(orgelection.get_recipients().values_list(
        'pk', flat=True))
    total_recipients = len(recipients)

    mailing.count = total_recipients
    mailing.status = 'queued'
    mailing.save()

    logger.info(u'Mailing Recipient Initalizing. Email %s OElection %s Org %s',
                email_id, orgelection, orgelection.organization_id)

    newrelic.agent.add_custom_parameter('email_id', email_id)
    newrelic.agent.add_custom_parameter(
        'organization_id', orgelection.organization_id)

    recipient_number = 1
    for recipient_id in recipients:
        final = bool(recipient_number == total_recipients)

        send_email.apply_async(
            kwargs={
                'email_id': email_id,
                'recipient_id': recipient_id,
                'election_id': orgelection.election_id,
                'recipient_number': recipient_number,
                'final': final
            },
            priority=priority
        )

        recipient_number += 1


@shared_task
def update_status(email_id, recipient_number, final):
    """Update the mailing status"""
    mailing = Mailing.objects.select_related('email').get(email__id=email_id)

    newrelic.agent.add_custom_parameter('email_id', email_id)
    newrelic.agent.add_custom_parameter(
        'organization_id', mailing.email.organization_id)
    newrelic.agent.add_custom_parameter('final', final)
    newrelic.agent.add_custom_parameter('recipient_number', recipient_number)

    logger.info(u'Mailing Status Update. Email %s Recipient # %s Final %s',
                email_id, recipient_number, final)

    # If the mailing has already been marked as sent, bail out
    if mailing.status == 'sent':
        return

    mailing.status = 'sending'
    mailing.sent = recipient_number

    # If it's the first recipient start the send clock
    if recipient_number == 1:
        mailing.send_start = timezone.now()

    if final:
        time.sleep(5)
        mailing.status = 'sent'

        # If it's the final recipient stop the send clock
        mailing.send_finish = timezone.now()

        total_sent = mailing.email.emailactivity_set.filter(
            activity='send').count()
        mailing.sent = total_sent

    mailing.save()


@shared_task
def send_email(email_id, recipient_id, election_id, recipient_number, final):
    """Send an individual email"""
    newrelic.agent.add_custom_parameter('recipient_number', recipient_number)
    newrelic.agent.add_custom_parameter('recipient_id', recipient_id)

    result = compose_email(recipient_id, email_id, election_id)

    tags = {
        'email_id': result['email_id'],
        'recipient_id': result['recipient_id'],
        'organization_id': result['organization_id']
    }

    message_id = deliver(
        to_address=result['to_address'],
        from_address=result['from_address'],
        subject=result['subject'],
        html=result['body'],
        tags=tags)

    EmailActivity(
        message_id=message_id,
        email_id=result['email_id'],
        recipient_id=result['recipient_id'],
        activity='send').save()

    # The first, every 1000, or final email, update the count and status
    if recipient_number == 1 or not recipient_number % 1000 or final:

        if recipient_number == 1 or final:
            priority = 10
        else:
            priority = 4

        update_status.apply_async(
            kwargs={
                'email_id': email_id,
                'recipient_number': recipient_number,
                'final': final
            },
            priority=priority)


@shared_task
def trigger_stats():
    """Trigger the stats counter for all mailings"""
    mailings = Mailing.objects.all()
    for mailing in mailings:
        generate_stats.delay(mailing.id)


@shared_task
def generate_stats(mailing_id):
    """Generate stats and attach it to a mailing"""
    mailing = Mailing.objects.get(id=mailing_id)

    newrelic.agent.add_custom_parameter('email_id', mailing.email.id)
    newrelic.agent.add_custom_parameter(
        'organization_id', mailing.email.organization_id)

    email_activities = mailing.email.emailactivity_set.all()
    stats = {}
    stats['unique_clicks'] = email_activities.filter(
        activity='click').distinct('message_id').count()
    stats['unique_opens'] = email_activities.filter(
        activity='open').distinct('message_id').count()
    stats['complaints'] = email_activities.filter(
        activity='complaint').distinct('message_id').count()
    stats['bounces'] = email_activities.filter(
        activity='bounce').distinct('message_id').count()
    stats['unsubscribes'] = Unsubscribe.objects.filter(
        email=mailing.email).distinct('user').count()

    mailing.sent = email_activities.filter(
        activity='send').count()
    mailing.stats = stats
    mailing.save(update_fields=['stats', 'sent'])
