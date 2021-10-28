from typing import List, Union, cast

from httpx import Response

from neuroio.base import IAMBase, IAMBaseAsync, IAMBaseBase
from neuroio.constants import sentinel
from neuroio.utils import request_query_processing, validate_month_str


class BillingBase(IAMBaseBase):
    def get_url(self, key: str) -> str:
        return self.base_url + f"/v1/billing/{key}/"


class Impl(IAMBase, BillingBase):
    def usage(
        self,
        limit: int = 20,
        offset: int = 0,
        spaces_ids: Union[List[int], object] = sentinel,
        event_types: Union[List[int], object] = sentinel,
        month_from: Union[str, object] = sentinel,
        month_to: Union[str, object] = sentinel,
    ) -> Response:
        if month_to != sentinel:
            validate_month_str(cast(str, month_to))
        if month_from != sentinel:
            validate_month_str(cast(str, month_from))
        data = request_query_processing(locals(), ["self"])

        with self.get_client() as client:
            return client.get(url=self.get_url("usage"), params=data)

    def usage_total(
        self,
        spaces_ids: Union[List[int], object] = sentinel,
        event_types: Union[List[int], object] = sentinel,
        month_from: Union[str, object] = sentinel,
        month_to: Union[str, object] = sentinel,
    ) -> Response:
        if month_to != sentinel:
            validate_month_str(cast(str, month_to))
        if month_from != sentinel:
            validate_month_str(cast(str, month_from))
        data = request_query_processing(locals(), ["self"])

        with self.get_client() as client:
            return client.get(url=self.get_url("usage/total"), params=data)


class ImplAsync(IAMBaseAsync, BillingBase):
    async def usage(
        self,
        limit: int = 20,
        offset: int = 0,
        spaces_ids: Union[List[int], object] = sentinel,
        event_types: Union[List[int], object] = sentinel,
        month_from: Union[str, object] = sentinel,
        month_to: Union[str, object] = sentinel,
    ) -> Response:
        if month_to != sentinel:
            validate_month_str(cast(str, month_to))
        if month_from != sentinel:
            validate_month_str(cast(str, month_from))
        data = request_query_processing(locals(), ["self"])

        async with self.get_client() as client:
            return await client.get(url=self.get_url("usage"), params=data)

    async def usage_total(
        self,
        spaces_ids: Union[List[int], object] = sentinel,
        event_types: Union[List[int], object] = sentinel,
        month_from: Union[str, object] = sentinel,
        month_to: Union[str, object] = sentinel,
    ) -> Response:
        if month_to != sentinel:
            validate_month_str(cast(str, month_to))
        if month_from != sentinel:
            validate_month_str(cast(str, month_from))
        data = request_query_processing(locals(), ["self"])

        async with self.get_client() as client:
            return await client.get(
                url=self.get_url("usage/total"), params=data
            )
