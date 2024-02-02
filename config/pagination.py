from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomSELTEQLimitOffsetPagination(PageNumberPagination):
    page_size_query_param = "limit"  # items per page
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            {
                "next": self.page.next_page_number() if self.page.has_next() else None,
                "previous": self.page.previous_page_number()
                if self.page.has_previous()
                else None,
                "count": self.page.paginator.count,
                "results": data,
            }
        )
