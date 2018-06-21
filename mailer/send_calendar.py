"""Utilities to get the sending calendar"""
from django.utils.timezone import localtime

from election.choices import STATES
from mailer.models import MailingTemplate


def mailing_calendar(organization=None, upcoming=False, date=None,
                     email_active=None, include_sent=False, limit=None,
                     state_id=None, election_id=None):
    """Gets the election calendar and returns an enhanced raw MailingTemplate"""

    query = """
    SELECT
           A.mailing_template_id as id,
           mt.name as name,
           mt.election_type as election_type,
           mt.days_to_deadline as days_to_deadline,
           mt.email_id AS email_id,
           mt.deadline_type,

           me.uuid as email_uuid,

           A.election_id as election_id,
           s.name as election_state,
           oe.id as organizationelection_id,
           oe.uuid as organizationelection_uuid,
           date_trunc('day', A.send_date) as send_date,
           oe.organization_id as organization_id,

           (SELECT count(DISTINCT accounts_user.id) FROM "accounts_user"
            INNER JOIN "location_location" ON ("accounts_user"."location_id" = "location_location"."id")
            INNER JOIN "location_location_districts"
                ON ("location_location"."id" = "location_location_districts"."location_id")
            WHERE ("location_location_districts"."legislativedistrict_id"
                IN (
                    SELECT U0."id" AS Col1 FROM "election_legislativedistrict" U0
                    INNER JOIN "election_election_voting_districts" U1
                        ON (U0."id" = U1."legislativedistrict_id")
                    WHERE U1."election_id" = A.election_id)
                        AND "accounts_user"."unsubscribed" = False
                        AND "accounts_user"."organization_id" = oe.organization_id
                )) as total_recipients

        FROM
        ((
            -- Registration (`vr_deadline`) Emails
            SELECT
                mt.id as mailing_template_id,
                e.id as election_id,
                CASE
                    WHEN o.online_vr = true AND e.vr_deadline_online is not null THEN
                        e.vr_deadline_online - cast(mt.days_to_deadline||' days' as Interval)
                    ELSE
                        e.vr_deadline - cast(mt.days_to_deadline||' days' as Interval)
                END as send_date
            FROM mailer_mailingtemplate mt
            JOIN mailer_email me ON mt.email_id = me.id
            LEFT JOIN election_election e ON mt.election_type = e.election_type
            JOIN election_state s ON e.state_id = s.code
            JOIN election_organizationelection oe ON
                me.organization_id = oe.organization_id AND e.id = oe.election_id
            JOIN branding_organization o ON o.id = oe.organization_id
            WHERE mt.deadline_type = 'vr_deadline' AND oe.vr_active = True AND mt.active = True
            AND (
                (o.disable_vr_sameday = false OR s.same_day_vr = false)
                AND
                (o.disable_vr_eday = false OR s.eday_vr = false)
            )
        ) UNION ALL (
            -- Early Vote Start `evip_start_date` Emails
            SELECT
                mt.id as mailing_template_id,
                e.id as election_id,
                e.evip_start_date - cast(mt.days_to_deadline||' days' as Interval) send_date
            FROM mailer_mailingtemplate mt
            JOIN mailer_email me ON mt.email_id = me.id
            LEFT JOIN election_election e ON mt.election_type = e.election_type
            JOIN election_organizationelection oe ON
                me.organization_id = oe.organization_id AND e.id = oe.election_id
            WHERE mt.deadline_type = 'evip_start_date' AND oe.evip_active = True AND mt.active = True
        ) UNION ALL (
            -- Early Vote End `evip_close_date` Emails
            SELECT
                mt.id as mailing_template_id,
                e.id as election_id,
                e.evip_close_date - cast(mt.days_to_deadline||' days' as Interval) send_date
            FROM mailer_mailingtemplate mt
            JOIN mailer_email me ON mt.email_id = me.id
            LEFT JOIN election_election e ON mt.election_type = e.election_type
            JOIN election_organizationelection oe ON
                me.organization_id = oe.organization_id AND e.id = oe.election_id
            WHERE mt.deadline_type = 'evip_close_date' AND oe.evip_active = True AND mt.active = True
        ) UNION ALL (
            -- Vote By Mail Applications Due `vbm_application_deadline` Emails
            SELECT
                mt.id as mailing_template_id,
                e.id as election_id,
                e.vbm_application_deadline - cast(mt.days_to_deadline||' days' as Interval) send_date
            FROM mailer_mailingtemplate mt
            JOIN mailer_email me ON mt.email_id = me.id
            LEFT JOIN election_election e ON mt.election_type = e.election_type
            JOIN election_organizationelection oe ON
                me.organization_id = oe.organization_id AND e.id = oe.election_id
            WHERE mt.deadline_type = 'vbm_application_deadline' AND oe.vbm_active = True AND mt.active = True
        ) UNION ALL (
            -- Vote By Mail Returns Due `vbm_return_date` Emails
            SELECT
                mt.id as mailing_template_id,
                e.id as election_id,
                e.vbm_return_date - cast(mt.days_to_deadline||' days' as Interval) send_date
            FROM mailer_mailingtemplate mt
            JOIN mailer_email me ON mt.email_id = me.id
            LEFT JOIN election_election e ON mt.election_type = e.election_type
            JOIN election_organizationelection oe ON
                me.organization_id = oe.organization_id AND e.id = oe.election_id
            WHERE mt.deadline_type = 'vbm_return_date' AND oe.vbm_active = True AND mt.active = True
        ) UNION ALL (
            -- Election Day `election_date` Emails
            SELECT
                mt.id as mailing_template_id,
                e.id as election_id,
                e.election_date - cast(mt.days_to_deadline||' days' as Interval) send_date
            FROM mailer_mailingtemplate mt
            JOIN mailer_email me ON mt.email_id = me.id
            LEFT JOIN election_election e ON mt.election_type = e.election_type
            JOIN election_organizationelection oe ON
                me.organization_id = oe.organization_id AND e.id = oe.election_id
            WHERE mt.deadline_type = 'election_date' AND oe.eday_active = True AND mt.active = True
        )) AS A
        JOIN mailer_mailingtemplate mt ON A.mailing_template_id = mt.id
        JOIN mailer_email me ON mt.email_id = me.id
        JOIN election_organizationelection oe ON
            A.election_id = oe.election_id AND oe.organization_id = me.organization_id
        JOIN election_election e ON
            A.election_id = e.id
        LEFT JOIN election_state s ON
            e.state_id = s.code
        JOIN branding_organization o ON oe.organization_id = o.id

        WHERE

        -- Allow us to use python to fill in queries as we want
        {org_filter}
        {date_filter}
        {upcoming_filter}
        {email_active_filter}
        {unsent_filter}
        {state_filter}
        {election_filter}


        -- Set a default so we get a "WHERE"
        True
        ORDER BY send_date ASC, id ASC
        {limit}
    """

    attrs = {}

    if include_sent:
        attrs['unsent_filter'] = ''
    else:
        attrs['unsent_filter'] = ('NOT EXISTS(SELECT 1 FROM mailer_mailing m '
                                  'WHERE m.organization_election_id = oe.id '
                                  'AND m.template_id = mt.id) AND')


    if organization:
        attrs['org_filter'] = 'oe.organization_id = {} AND'.format(
            organization.id)
    else:
        attrs['org_filter'] = ''

    if upcoming:
        attrs['upcoming_filter'] = 'send_date >= \'{}\' AND'.format(
            localtime().strftime('%Y%m%d'))
    else:
        attrs['upcoming_filter'] = ''

    if date:
        attrs['date_filter'] = 'send_date = \'{}\' AND'.format(
            date.strftime('%Y%m%d'))
    else:
        attrs['date_filter'] = ''

    if email_active:
        attrs['email_active_filter'] = 'o.email_active = true AND'
    else:
        attrs['email_active_filter'] = ''

    possible_states = [possible_state for possible_state, _ in STATES]
    if state_id and state_id not in possible_states:
        raise ValueError('Invalid State ID Provided')

    if state_id:
        attrs['state_filter'] = 'e.state_id = \'{}\' AND'.format(state_id)
    else:
        attrs['state_filter'] = ''

    if election_id:
        attrs['election_filter'] = 'e.id = {} AND'.format(int(election_id))
    else:
        attrs['election_filter'] = ''

    if limit:
        attrs['limit'] = 'LIMIT {}'.format(int(limit))
    else:
        attrs['limit'] = ''

    return MailingTemplate.objects.raw(query.format(**attrs))
