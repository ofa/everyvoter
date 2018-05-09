"""Settings for logs"""
# pylint: disable=invalid-name
import environ

env = environ.Env(
    DJANGO_LOG_LEVEL=(str, 'INFO'),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': env('DJANGO_LOG_LEVEL'),
            'propagate': True,
        },
        'email': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        }
    },
}
