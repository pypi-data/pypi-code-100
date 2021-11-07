import math
import typing
from . import object_
from .page import Page

T = typing.TypeVar('T')


class Paginator(typing.Generic[T]):

    def __init__(
            self,
            alfa_object: 'object_.AlfaCRUDObject',
            start_page: int = 0,
            page_size: int = 20,
            filters: typing.Dict[str, typing.Any] = None
    ):
        self._page_number = start_page
        self._page: typing.Optional[Page[T]] = None
        self._total = 0
        self._page_size = page_size
        self._filters = filters
        self._object = alfa_object

    def __aiter__(self) -> 'Paginator[T]':
        return self

    async def __anext__(self) -> Page[T]:
        if self._total and self._page_number >= self.total_page:
            raise StopAsyncIteration

        result = await self._object.list(
            page=self._page_number,
            count=self._page_size,
            **self._filters,
        )
        self._page_number += 1
        self._total = result["total"]

        return Page(
            number=self._page_number,
            items=result.get("items"),
            total=self._total,
        )

    @property
    def total_page(self) -> int:
        """
        Get total page by total count and page size
        :return:
        """
        return math.ceil(self._total / self._page_size)

    @property
    def page(self) -> Page[T]:
        return self._page
