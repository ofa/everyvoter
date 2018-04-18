"""Serializers for the Kennedy project"""
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from rest_framework.pagination import PageNumberPagination

from election.models import LegislativeDistrict


class DistrictSerializer(serializers.ModelSerializer):
    """Serializer for LegislativeDistrict"""
    page_size = 700

    class Meta(object):
        model = LegislativeDistrict
        fields = ('id', 'name', 'state', 'ocd_id', 'district_type')
