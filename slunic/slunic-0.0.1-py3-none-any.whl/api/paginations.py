from collections import OrderedDict
from django.core.paginator import InvalidPage
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from slunic.paginator import CachedPaginator
from slunic.utils import make_fragment_key


class CachedPageNumberPagination(PageNumberPagination):
    page_size = 40
    page_size_query_param = "per_page"
    max_page_size = 1000
    django_paginator_class = CachedPaginator

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        # get cache key from viewsets otherwise create new fragment key
        cache_key = getattr(view, "cache_list_key", None)
        cache_timeout = getattr(view, "cache_list_timeout", None)
        if not cache_key:
            number = request.query_params.get(self.page_query_param, 1)
            kwargs = {"mode": "api", "per_page": self.page_size, "number": number}
            cache_key = make_fragment_key(queryset.model, request, **kwargs)

        # create paginator
        paginator = self.django_paginator_class(
            queryset,
            page_size,
            request=request,
            cache_key=cache_key,
            cache_timeout=cache_timeout,
        )
        page_number = self.get_page_number(request, paginator)

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(page_number=page_number, message=str(exc))
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_page_object_response(self):
        page = self.page
        paginator = page.paginator
        return OrderedDict(
            [
                (
                    "paginator",
                    OrderedDict(
                        [
                            ("count", paginator.count),
                            ("num_pages", paginator.num_pages),
                            ("page_range", [i for i in paginator.page_range]),
                        ]
                    ),
                ),
                ("number", page.number),
                ("has_next", page.has_next()),
                ("has_previous", page.has_previous()),
                ("next_page_number", page.next_page_number() if page.has_next() else None),
                ("previous_page_number", page.previous_page_number() if page.has_previous() else None),
            ]
        )

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("page", self.get_page_object_response()),
                    ("size", self.get_page_size(self.request)),
                    ("results", data),
                ]
            )
        )
