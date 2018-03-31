"""Admin functionality for user import app"""
from django.contrib import admin

from user_import import models


@admin.register(models.UserImport)
class UserImportAdmin(admin.ModelAdmin):
    """Admin View for User Import"""
    list_display = ('name', 'count', 'default', 'created_at', 'organization')
    search_fields = ('name',)
    readonly_fields = [
        'count'#, 'file'
    ]
    list_filter = ('organization__name',)

    def has_add_permission(self, request):
        """Imports can not be added via the django admin"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Imports can not be deleted via the django admin"""
        return False
