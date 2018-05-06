"""Serializers for the EveryVoter project"""
from rest_framework import serializers

from election.models import LegislativeDistrict


class DistrictSerializer(serializers.ModelSerializer):
    """Serializer for LegislativeDistrict"""
    page_size = 700

    class Meta(object):
        """Meta options for serializer"""
        model = LegislativeDistrict
        fields = ('id', 'name', 'state', 'ocd_id', 'district_type')
