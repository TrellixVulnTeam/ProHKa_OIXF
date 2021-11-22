from rest_framework import pagination
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class CommentPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
