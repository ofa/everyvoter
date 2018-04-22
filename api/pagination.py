"""Django Rest Framework Pagination"""
from rest_framework.pagination import PageNumberPagination


class LargeResultsSetPagination(PageNumberPagination):
    """Pagination where there are a large number of results by default"""
    page_size = 1000
    page_size_query_param = 'limit'
    max_page_size = 10000


class StandardResultsSetPagination(PageNumberPagination):
    """Pagination where there are a small number of results by default"""
    page_size = 100
    page_size_query_param = 'limit'
    max_page_size = 1000
