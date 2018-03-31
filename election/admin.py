"""Admin functionality for election app"""
from django.contrib import admin

from election import models


@admin.register(models.State)
class StateAdmin(admin.ModelAdmin):
    """Admin View for State"""
    list_display = ('name', 'code')
    search_fields = ('name',)

    def has_add_permission(self, request):
        """Organizations can not be added via the django admin"""
        return False


@admin.register(models.Election)
class ElectionAdmin(admin.ModelAdmin):
    """Admin View for Election"""
    list_display = ('state', 'election_type')
    search_fields = ('state',)
