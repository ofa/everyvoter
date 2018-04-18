"""API Urls"""
# pylint: disable=invalid-name
from django.conf.urls import url, include
from rest_framework import routers

from api.views import DistrictViewSet


router = routers.DefaultRouter()
router.register(r'districts', DistrictViewSet, base_name='districts')


urlpatterns = [
    url(r'^', include(router.urls)),
]
