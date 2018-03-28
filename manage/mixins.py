"""Mixins for django management"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class ManageViewMixin(LoginRequiredMixin):
    """Mixin for all management pages"""
    def dispatch(self, request, *args, **kwargs):
        """Manage"""
        # Only staff can access management pages
        if request.user.is_authenticated() and not request.user.is_staff:
            return redirect('/')

        return super(ManageViewMixin, self).dispatch(request, *args, **kwargs)
