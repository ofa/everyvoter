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

        queue_counts = {}

        with celery_app.connection_or_acquire() as conn:
            for queue in settings.HIREFIRE_QUEUES:
                count = celery_app.amqp.queues[queue](
                    conn.default_channel).queue_declare(
                        passive=True).message_count
                queue_counts[queue] = count

        results = []

        worker_priority = queue_counts.get('bulk_priority', 0)

        results.append(
            {
                'name': 'worker_priority',
                'quantity': worker_priority
            })

        worker = queue_counts.get('bulk', 0)
        worker += queue_counts.get('default', 0)
        worker += queue_counts.get('feedback', 0)

        results.append(
            {
                'name': 'worker_general',
                'quantity': worker
            })

        worker_import = queue_counts.get('user_import', 0)

        results.append(
            {
                'name': 'worker_import',
                'quantity': worker_import
            })

        worker_high_memory = queue_counts.get('high_memory', 0)
        results.append({
            'name': 'worker_high_memory',
            'quantity': worker_high_memory
            })

        return JsonResponse(results, safe=False)
