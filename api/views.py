"""EveryVoter API Views"""
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from api.serializers import DistrictSerializer
from election.models import LegislativeDistrict
from election.filters import LegislativeDistrictFilter


class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    """
    queryset = LegislativeDistrict.objects.all()
    serializer_class = DistrictSerializer
    filter_class = LegislativeDistrictFilter
    pagination_class = PageNumberPagination
    paginate_by = 10

    ordering = ['state', 'district_type']
