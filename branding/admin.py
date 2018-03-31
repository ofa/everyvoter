"""Admin functionality for branding app"""
from django.contrib import admin

from branding import models


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Admin View for Organization"""
    list_display = ('name', 'platform_name')
    search_fields = ('name',)

    def has_add_permission(self, request):
        """Organizations can not be added via the django admin"""
        return False


@admin.register(models.Domain)
class DomainAdmin(admin.ModelAdmin):
    """Admin View for Domain"""
    list_display = ('hostname', 'organization')
    search_fields = ('hostname',)
