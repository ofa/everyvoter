"""Democracy Works consumer code"""
import logging

from django.conf import settings
from django.utils.timezone import localtime
import requests
import newrelic.agent

from .models import Response as APIResponse, DateChange
from election.models import Election


# pylint: disable=invalid-name
logger = logging.getLogger('democracy_sync')


@newrelic.agent.function_trace()
def api_fetch():
    """Fetch the data from the DW API"""
    headers = {
        'Authorization': 'apikey {}'.format(settings.DEMOCRACY_WORKS_API_KEY),
        'Accept': 'application/json'
    }

    response = requests.get(
        settings.DEMOCRACY_WORKS_API_URL,
        headers=headers)

    logger.info(u'Sync: API Pull - URL: %s Status Code: %s Time: %s',
                settings.DEMOCRACY_WORKS_API_URL, response.status_code,
                response.elapsed.total_seconds())

    if response.status_code != 200:
        raise Exception(
            'Bad Response from Democracy Works {}'.format(
                response.status_code))

    return response.json()


def get_response():
    """Get today's DemocracyWorks API Response. Pull from DW if needed

    As the DemocracyWorks API is (a) rate limited and (b) rarely changes, we
    can grab the response once per day per installation of EveryVoter and store
    that API response in the database. This will also let us look back on past
    data pulls.
    """
    # Attempt to get the latest response from the database
    today_response = APIResponse.objects.filter(
        created_at__gte=localtime().replace(
            hour=0, minute=0, second=0, microsecond=0)).first()

    # If a response for today is not found, request it from the DW API
    if not today_response:
        today_response = APIResponse(data=api_fetch())
        today_response.save()

    return today_response


def process_election(response, list_number):
    election_data = response.data[list_number]

    election_date = election_data['date'][:10]
    district_ocd_id = election_data['district-divisions'][0]['ocd-id']
    election = Election.objects.filter(
        voting_districts__ocd_id=district_ocd_id,
        election_date=election_date).first()

    if not election:
        return None

    response.elections.add(election)

    changes = []

    election.election_date = election_data['date'][:10]

    for method in election_data['district-divisions'][0]['voting-methods']:
        if method['type'] == 'early-voting':
            if unicode(election.evip_start_date) != method['start'][:10]:
                old_deadline = election.evip_start_date
                new_deadline = method['start'][:10]
                election.evip_start_date = new_deadline
                logger.info(u'Sync: Process Election %s Change: '
                            'evip_start_date %s %s',
                            election, old_deadline, new_deadline)
                changes.append(DateChange(
                    response=response,
                    election=election,
                    field='evip_start_date',
                    old_date=old_deadline,
                    new_date=new_deadline))

            if unicode(election.evip_close_date) != method['end'][:10]:
                old_deadline = election.evip_close_date
                new_deadline = method['end'][:10]
                election.evip_close_date = new_deadline
                logger.info(u'Sync: Process Election %s Change: '
                            'evip_close_date %s %s',
                            election, old_deadline, new_deadline)
                changes.append(DateChange(
                    response=response,
                    election=election,
                    field='evip_close_date',
                    old_date=old_deadline,
                    new_date=new_deadline))


        elif method['type'] == 'by-mail' and not method['primary']:

            if unicode(election.vbm_application_deadline) != method[
                    'ballot-request-deadline-received'][:10]:
                old_deadline = election.vbm_application_deadline
                new_deadline = method[
                    'ballot-request-deadline-received'][:10]
                election.vbm_application_deadline = new_deadline
                logger.info(u'Sync: Process Election %s Change: '
                            'vbm_application_deadline %s %s',
                            election, old_deadline, new_deadline)
                changes.append(DateChange(
                    response=response,
                    election=election,
                    field='vbm_application_deadline',
                    old_date=old_deadline,
                    new_date=new_deadline))

    for method in election_data['district-divisions'][0][
            'voter-registration-methods']:

        if method['type'] == 'online':
            if unicode(election.vr_deadline_online) != method[
                    'deadline-online'][:10]:
                old_deadline = election.vr_deadline_online
                new_deadline = method['deadline-online'][:10]
                election.vr_deadline_online = new_deadline
                logger.info(u'Sync: Process Election %s Change: '
                            'vr_deadline_online %s %s',
                            election, old_deadline, new_deadline)
                changes.append(DateChange(
                    response=response,
                    election=election,
                    field='vr_deadline_online',
                    old_date=old_deadline,
                    new_date=new_deadline))

        elif method['type'] == 'by-mail':
            deadline = method.get('deadline-postmarked',
                                  method.get('deadline-received'))
            if unicode(election.vr_deadline) != deadline[:10]:
                old_deadline = election.vr_deadline
                new_deadline = deadline[:10]
                election.vr_deadline = new_deadline
                logger.info(u'Sync: Process Election %s Change: vr_deadline '
                            '%s %s',
                            election, old_deadline, new_deadline)
                changes.append(DateChange(
                    response=response,
                    election=election,
                    field='vr_deadline',
                    old_date=old_deadline,
                    new_date=new_deadline))

    election.save()
    DateChange.objects.bulk_create(changes)

    logger.info(u'Sync: Process Election %s %s Changes',
                election, len(changes))
