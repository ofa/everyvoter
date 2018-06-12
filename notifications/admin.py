"""Admin functionality for Notification app"""
from django.contrib import admin

from notifications.models import NotificationSetting

class NotificationSettingInline(admin.TabularInline):
    """Inline for notification settings"""
    model = NotificationSetting

    def has_delete_permission(self, request, obj=None):
        """Users can not be deleted via the django admin"""
        return False
