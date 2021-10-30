from django.core.cache import cache
from django.utils.functional import cached_property
from django.core.paginator import Paginator, Page, PageNotAnInteger
from .configs import app_configs
from .utils import make_fragment_key


class CachedPaginator(Paginator):
    """
    A paginator that caches with `cache_key` = model class name
    the results on a page by page basis.
    """

    def __init__(
        self,
        object_list,
        per_page,
        orphans=0,
        request=None,
        allow_empty_first_page=True,
        cache_key=None,
        cache_timeout=None,
    ):
        super().__init__(
            object_list,
            per_page,
            orphans,
            allow_empty_first_page,
        )
        self.request = request
        self.model = object_list.model
        self.cache_key = cache_key
        self.cache_timeout = cache_timeout or app_configs.CACHE_OBJECT_LIST_TIMEOUT

    @cached_property
    def count(self):
        """
        The original django.core.paginator.count attribute in Django1.8
        is not writable and cant be setted manually, but we would like
        to override it when loading data from cache. (instead of recalculating it).
        So we make it writable via @cached_property.
        """
        return super(CachedPaginator, self).count

    def set_count(self, count):
        """
        Override the paginator.count value (to prevent recalculation)
        and clear num_pages and page_range which values depend on it.
        """
        self.count = count
        # if somehow we have stored .num_pages or .page_range (which are cached properties)
        # this can lead to wrong page calculations (because they depend on paginator.count value)
        # so we clear their values to force recalculations on next calls
        try:
            del self.num_pages
        except AttributeError:
            pass
        try:
            del self.page_range
        except AttributeError:
            pass

    @cached_property
    def num_pages(self):
        """This is not writable in Django1.8. We want to make it writable"""
        return super(CachedPaginator, self).num_pages

    @cached_property
    def page_range(self):
        """This is not writable in Django1.8. We want to make it writable"""
        return super(CachedPaginator, self).page_range

    def get_cache_key(self, number):
        if self.cache_key:
            return self.cache_key
        else:
            kwargs = {"per_page": self.per_page, "number": number}
            page_cache_key = make_fragment_key(self.model, self.request, **kwargs)
            return page_cache_key

    def page(self, number):
        """
        Returns a Page object for the given 1-based page number.

        This will attempt to pull the results out of the cache first, based on
        the requested page number. If not found in the cache,
        it will pull a fresh list and then cache that result + the total result count.
        """

        # In order to prevent counting the queryset
        # we only validate that the provided number is integer
        # The rest of the validation will happen when we fetch fresh data.
        # so if the number is invalid, no cache will be setted
        # number = self.validate_number(number)
        try:
            number = int(number)
        except (TypeError, ValueError):
            raise PageNotAnInteger("That page number is not an integer")

        page_cache_key = self.get_cache_key(number)
        page_data = cache.get(page_cache_key)

        if page_data is None:
            page = super().page(number)
            # cache not only the objects, but the total count too.
            page_data = (page.object_list, self.count)
            cache.set(page_cache_key, page_data, self.cache_timeout)
        else:
            cached_object_list, cached_total_count = page_data
            self.set_count(cached_total_count)
            page = Page(cached_object_list, number, self)

        return page
