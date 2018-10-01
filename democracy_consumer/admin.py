"""Admin functionality for democracy works consumer app"""
from django.contrib import admin

from .models import Response, DateChange


@admin.register(Response)
class APIResponseAdmin(admin.ModelAdmin):
    """Admin View for Democracy Works API Response"""


@admin.register(DateChange)
class DateChangeAdmin(admin.ModelAdmin):
    """Admin view for Democracy Works Date Change"""
    list_display = ('election', 'response', 'field', 'old_date', 'new_date')
    readonly_fields = [
        'election', 'field', 'response', 'old_date', 'new_date'
    ]
    list_filter = ('election__state', 'election__election_type', 'response')
