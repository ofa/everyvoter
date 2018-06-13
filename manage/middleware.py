"""Management-Related Middleware"""
import re

from django.urls import reverse
from django.shortcuts import redirect


# pylint: disable=invalid-name
password_regex = re.compile('^/manage/admin/password_change')
admin_regex = re.compile('^/manage/admin')


class RestrictAdminMiddleware(object):
    """Middleware to prevent non-superusers from accessing the django admin"""

    def __init__(self, get_response):
        """Initialize the Middleware"""
        self.get_response = get_response


    def __call__(self, request):
        """Process a request"""

        # Only superusers should be able to access the admin, but all
        # authorized users should be able to access the password change URL
        # (at least until we build our own password change view)
        if (hasattr(request, 'user') and
                request.user.is_authenticated() and
                not request.user.is_superuser and
                (
                    admin_regex.match(request.path) and
                    not password_regex.match(request.path)
                )):
            return redirect(reverse('manage:manage'))

        return self.get_response(request)
