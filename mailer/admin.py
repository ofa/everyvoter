"""Django Admin Panels for App"""
from django.contrib import admin

from mailer import models

@admin.register(models.SendingAddress)
class SendingAddressAdmin(admin.ModelAdmin):
    """Admin View for SendingAddress"""
    list_display = ('address', 'organization')
    list_filter = ('organization__name',)
    actions = None

    def has_delete_permission(self, request, obj=None):
        """The primary address can not be deleted via the django admin"""
        if obj and obj.pk == 1:
            return False
        else:
            return True
