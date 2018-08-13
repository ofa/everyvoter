"""Views related to notifications"""
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse

from everyvoter_common.utils.uuid_slug_mixin import UUIDSlugMixin
from manage.mixins import ManageViewMixin
from notifications.models import NotificationSetting


class NotificationSettingUpdateView(ManageViewMixin, SuccessMessageMixin,
                                    UUIDSlugMixin, UpdateView):
    """Create a new import"""
    model = NotificationSetting
    fields = ['daily_batch_sample']
    slug_field = 'uuid'
    success_message = "Notification settings updated"
    context_object_name = 'setting'

    def get_queryset(self):
        """Only allow editing of users in the same organization"""
        queryset = super(NotificationSettingUpdateView, self).get_queryset()
        return queryset.filter(user__organization=self.request.organization)

    def get_success_url(self):
        """Get the success url"""
        return reverse(
            'manage:notifications:update_notificationsettings',
            args=[self.object.uuid])
