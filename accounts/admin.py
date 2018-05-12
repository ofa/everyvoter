"""Django Admin Panels for App"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts import models

@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    """Admin View for Chapter"""
    list_display = ('first_name', 'last_name', 'email', 'is_staff',
                    'is_superuser', 'created_at', 'organization')
    fieldsets = (
        (None, {'fields': ('password', 'email', 'username', 'organization')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'created_at',
                                        'modified_at')}),
    )
    readonly_fields = [
        'is_superuser', 'email', 'username', 'created_at', 'modified_at',
        'organization'
    ]
    list_filter = ('organization__name', 'is_staff', 'is_superuser')
    ordering = ('id',)

    def has_add_permission(self, request):
        """No-one should be able to add users using the django admin"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Users can not be deleted via the django admin"""
        return False
