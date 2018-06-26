"""Settings for the Celery Task Runner"""
# pylint: disable=line-too-long,invalid-name
import os

from celery.schedules import crontab
from kombu import Queue
import environ

env = environ.Env(
    DEBUG=(bool, False),

    BROKER_URL=(str, 'pyamqp://guest@localhost//'),

    # Some Celery defaults found at https://www.cloudamqp.com/docs/celery.html
    BROKER_POOL_LIMIT=(int, 1),
    BROKER_HEARTBEAT=(int, 30),
    BROKER_CONNECTION_TIMEOUT=(int, 30),
    CELERY_TASK_SERIALIZER=(str, 'json'),
    CELERY_EVENT_QUEUE_EXPIRES=(int, 60),
    CELERY_ALWAYS_EAGER=(bool, True),
    CELERY_TIMEZONE=(str, 'UTC'),
    CELERY_SEND_EVENTS=(bool, False),
    CELERY_RESULT_BACKEND=(str, 'django-db'),
    CELERY_WORKER_CONCURRENCY=(int, 6)
)


# If CloudAMQP is enabled, use that as the broker URL
if os.environ.get('CLOUDAMQP_URL', False):
    CELERY_BROKER_URL = os.environ.get('CLOUDAMQP_URL')
else:
    CELERY_BROKER_URL = env('BROKER_URL')

CELERY_TASK_SERIALIZER = env('CELERY_TASK_SERIALIZER')

CELERY_BROKER_POOL_LIMIT = env('BROKER_POOL_LIMIT')
CELERY_BROKER_HEARTBEAT = env('BROKER_HEARTBEAT')
CELERY_BROKER_CONNECTION_TIMEOUT = env('BROKER_CONNECTION_TIMEOUT')
CELERY_WORKER_CONCURRENCY = env('CELERY_WORKER_CONCURRENCY')

CELERY_SEND_EVENTS = env('CELERY_SEND_EVENTS')
CELERY_EVENT_QUEUE_EXPIRES = env('CELERY_EVENT_QUEUE_EXPIRES')

if os.environ.get('CELERY_ALWAYS_EAGER', False):
    CELERY_TASK_ALWAYS_EAGER = env('CELERY_ALWAYS_EAGER')
else:
    CELERY_TASK_ALWAYS_EAGER = env('DEBUG')

CELERY_TASK_EAGER_PROPAGATES = True

# By default EveryVoter does not consume results
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')

CELERYBEAT_SCHEDULE = {
}

CELERY_TASK_DEFAULT_QUEUE = 'default'
CELERY_TASK_QUEUES = {
    Queue('default', routing_key='task.#'),
    Queue('high_memory', routing_key='high_memory.#'),
    Queue('feedback', routing_key='feedback.#'),
    Queue('user_import', routing_key='user_import.#'),
    Queue('bulk', routing_key='bulk.#'),
    Queue('bulk_priority', routing_key='bulk_priority.#'),
}

CELERY_TASK_ROUTES = ([
    ('user_import.tasks.import_user', {'queue': 'user_import', 'routing_key': 'user_import.user_import'}),
    ('user_import.tasks.*', {'queue': 'high_memory'}),
    ('mailer.tasks.send_email', {'queue': 'bulk_priority'}),
    ('mailer.tasks.update_status', {'queue': 'default'}),
    ('mailer.tasks.generate_stats', {'queue': 'default'}),
    ('mailer.tasks.*', {'queue': 'high_memory'}),
    ('feedback.tasks.*', {'queue': 'feedback'}),
],)

CELERY_TIMEZONE = env('CELERY_TIMEZONE')
