"""HireFire-Related Views"""
from django.http import Http404
from django.conf import settings
from django.views.generic.base import View
from django.http import JsonResponse

from everyvoter.celery import app as celery_app


class HireFireView(View):
    """View for Hirefire"""
    def get(self, request, *args, **kwargs):
        """Handle a GET request"""
        token = kwargs['hirefire_token']

        if (token != settings.HIREFIRE_TOKEN or
                settings.HIREFIRE_TOKEN == ''):
            raise Http404('Invalid Token')

        result = []

        with celery_app.connection_or_acquire() as conn:
            for queue in settings.HIREFIRE_QUEUES:
                count = celery_app.amqp.queues[queue](
                    conn.default_channel).queue_declare(
                        passive=True).message_count
                result.append({queue: count})

        return JsonResponse(result, safe=False)
