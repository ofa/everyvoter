"""
WSGI config for kennedy project.
"""
# pylint: disable=invalid-name
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "everyvoter.settings")

# Fix django closing connection to Memcached after every request
from django.core.cache.backends.memcached import BaseMemcachedCache
BaseMemcachedCache.close = lambda self, **kwargs: None

application = get_wsgi_application()
