"""Settings for the Celery Task Runner"""
# pylint: disable=line-too-long,invalid-name
import os

from celery.schedules import crontab
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
    CELERY_RESULT_BACKEND=(str, 'django-db')
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

CELERY_SEND_EVENTS = env('CELERY_SEND_EVENTS')
CELERY_EVENT_QUEUE_EXPIRES = env('CELERY_EVENT_QUEUE_EXPIRES')

if os.environ.get('CELERY_ALWAYS_EAGER', False):
    CELERY_ALWAYS_EAGER = env('CELERY_ALWAYS_EAGER')
else:
    CELERY_ALWAYS_EAGER = env('DEBUG')

# By default Kennedy does not consume results
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')

CELERYBEAT_SCHEDULE = {
}

CELERY_TIMEZONE = env('CELERY_TIMEZONE')
