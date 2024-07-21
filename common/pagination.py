from rest_framework.pagination import LimitOffsetPagination


class MyLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

    def get_paginated_response(self, data):
        return {
            "count": self.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        }
