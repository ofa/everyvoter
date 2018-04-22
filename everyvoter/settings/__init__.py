"""Settings for Kennedy App"""
# We use wildcard imports here to bring all the settings from the smaller
# settings files into this __init__ file. This is essentially concatinating
# multiple files into one large settings.py


import environ

# Load all key/values from a `.env` file into the configuration
environ.Env.read_env('.env')


# pylint: disable=wildcard-import
from .base_settings import *
from .storage_settings import *
from .celery_settings import *
