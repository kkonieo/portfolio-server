from rest_framework.pagination import PageNumberPagination

# 포스트 페이지네이션


class PostListPagination(PageNumberPagination):
    page_size = "3"

    page_size_query_param = "size"

    max_page_size = 50

    page_query_param = "page"
