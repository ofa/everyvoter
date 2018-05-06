"""EveryVoter API Views"""
from rest_framework import viewsets

from api.pagination import LargeResultsSetPagination
from api.serializers import DistrictSerializer
from election.filters import LegislativeDistrictFilter
from election.models import LegislativeDistrict


class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing districts.
    """
    queryset = LegislativeDistrict.objects.all()
    serializer_class = DistrictSerializer
    filter_class = LegislativeDistrictFilter
    pagination_class = LargeResultsSetPagination

    ordering = ['state', 'district_type']
