"""Tasks"""
from celery import shared_task

from .consumer import get_response, process_election
from .models import Response as APIResponse


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
