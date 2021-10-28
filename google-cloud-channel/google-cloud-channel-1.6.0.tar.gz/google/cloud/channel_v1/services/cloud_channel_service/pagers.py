# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Sequence,
    Tuple,
    Optional,
    Iterator,
)

from google.cloud.channel_v1.types import channel_partner_links
from google.cloud.channel_v1.types import customers
from google.cloud.channel_v1.types import entitlements
from google.cloud.channel_v1.types import offers
from google.cloud.channel_v1.types import products
from google.cloud.channel_v1.types import service


class ListCustomersPager:
    """A pager for iterating through ``list_customers`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.channel_v1.types.ListCustomersResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``customers`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListCustomers`` requests and continue to iterate
    through the ``customers`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.channel_v1.types.ListCustomersResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., service.ListCustomersResponse],
        request: service.ListCustomersRequest,
        response: service.ListCustomersResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.channel_v1.types.ListCustomersRequest):
                The initial request object.
            response (google.cloud.channel_v1.types.ListCustomersResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListCustomersRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[service.ListCustomersResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[customers.Customer]:
        for page in self.pages:
            yield from page.customers

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListCustomersAsyncPager:
    """A pager for iterating through ``list_customers`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.channel_v1.types.ListCustomersResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``customers`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListCustomers`` requests and continue to iterate
    through the ``customers`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.channel_v1.types.ListCustomersResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[service.ListCustomersResponse]],
        request: service.ListCustomersRequest,
        response: service.ListCustomersResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.channel_v1.types.ListCustomersRequest):
                The initial request object.
            response (google.cloud.channel_v1.types.ListCustomersResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListCustomersRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[service.ListCustomersResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[customers.Customer]:
        async def async_generator():
            async for page in self.pages:
                for response in page.customers:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListEntitlementsPager:
    """A pager for iterating through ``list_entitlements`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.channel_v1.types.ListEntitlementsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``entitlements`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListEntitlements`` requests and continue to iterate
    through the ``entitlements`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.channel_v1.types.ListEntitlementsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., service.ListEntitlementsResponse],
        request: service.ListEntitlementsRequest,
        response: service.ListEntitlementsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.channel_v1.types.ListEntitlementsRequest):
                The initial request object.
            response (google.cloud.channel_v1.types.ListEntitlementsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListEntitlementsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[service.ListEntitlementsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[entitlements.Entitlement]:
        for page in self.pages:
            yield from page.entitlements

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListEntitlementsAsyncPager:
    """A pager for iterating through ``list_entitlements`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.channel_v1.types.ListEntitlementsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``entitlements`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListEntitlements`` requests and continue to iterate
    through the ``entitlements`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.channel_v1.types.ListEntitlementsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[service.ListEntitlementsResponse]],
        request: service.ListEntitlementsRequest,
        response: service.ListEntitlementsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.channel_v1.types.ListEntitlementsRequest):
                The initial request object.
            response (google.cloud.channel_v1.types.ListEntitlementsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListEntitlementsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[service.ListEntitlementsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[entitlements.Entitlement]:
        async def async_generator():
            async for page in self.pages:
                for response in page.entitlements:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListTransferableSkusPager:
    """A pager for iterating through ``list_transferable_skus`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.channel_v1.types.ListTransferableSkusResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``transferable_skus`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListTransferableSkus`` requests and continue to iterate
    through the ``transferable_skus`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.channel_v1.types.ListTransferableSkusResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., service.ListTransferableSkusResponse],
        request: service.ListTransferableSkusRequest,
        response: service.ListTransferableSkusResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.channel_v1.types.ListTransferableSkusRequest):
                The initial request object.
            response (google.cloud.channel_v1.types.ListTransferableSkusResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListTransferableSkusRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[service.ListTransferableSkusResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[entitlements.TransferableSku]:
        for page in self.pages:
            yield from page.transferable_skus

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListTransferableSkusAsyncPager:
    """A pager for iterating through ``list_transferable_skus`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.channel_v1.types.ListTransferableSkusResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``transferable_skus`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListTransferableSkus`` requests and continue to iterate
    through the ``transferable_skus`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.channel_v1.types.ListTransferableSkusResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[service.ListTransferableSkusResponse]],
        request: service.ListTransferableSkusRequest,
        response: service.ListTransferableSkusResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.channel_v1.types.ListTransferableSkusRequest):
                The initial request object.
            response (google.cloud.channel_v1.types.ListTransferableSkusResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListTransferableSkusRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[service.ListTransferableSkusResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[entitlements.TransferableSku]:
        async def async_generator():
            async for page in self.pages:
                for response in page.transferable_skus:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListTransferableOffersPager:
    """A pager for iterating through ``list_transferable_offers`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.channel_v1.types.ListTransferableOffersResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``transferable_offers`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListTransferableOffers`` requests and continue to iterate
    through the ``transferable_offers`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.channel_v1.types.ListTransferableOffersResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., service.ListTransferableOffersResponse],
        request: service.ListTransferableOffersRequest,
        response: service.ListTransferableOffersResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.channel_v1.types.ListTransferableOffersRequest):
                The initial request object.
            response (google.cloud.channel_v1.types.ListTransferableOffersResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListTransferableOffersRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[service.ListTransferableOffersResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[service.TransferableOffer]:
        for page in self.pages:
            yield from page.transferable_offers

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListTransferableOffersAsyncPager:
    """A pager for iterating through ``list_transferable_offers`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.channel_v1.types.ListTransferableOffersResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``transferable_offers`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListTransferableOffers`` requests and continue to iterate
    through the ``transferable_offers`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.channel_v1.types.ListTransferableOffersResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[service.ListTransferableOffersResponse]],
        request: service.ListTransferableOffersRequest,
        response: service.ListTransferableOffersResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.channel_v1.types.ListTransferableOffersRequest):
                The initial request object.
            response (google.cloud.channel_v1.types.ListTransferableOffersResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListTransferableOffersRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[service.ListTransferableOffersResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[service.TransferableOffer]:
        async def async_generator():
            async for page in self.pages:
                for response in page.transferable_offers:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListChannelPartnerLinksPager:
    """A pager for iterating through ``list_channel_partner_links`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.channel_v1.types.ListChannelPartnerLinksResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``channel_partner_links`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListChannelPartnerLinks`` requests and continue to iterate
    through the ``channel_partner_links`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.channel_v1.types.ListChannelPartnerLinksResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., service.ListChannelPartnerLinksResponse],
        request: service.ListChannelPartnerLinksRequest,
        response: service.ListChannelPartnerLinksResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.channel_v1.types.ListChannelPartnerLinksRequest):
                The initial request object.
            response (google.cloud.channel_v1.types.ListChannelPartnerLinksResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListChannelPartnerLinksRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[service.ListChannelPartnerLinksResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[channel_partner_links.ChannelPartnerLink]:
        for page in self.pages:
            yield from page.channel_partner_links

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListChannelPartnerLinksAsyncPager:
    """A pager for iterating through ``list_channel_partner_links`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.channel_v1.types.ListChannelPartnerLinksResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``channel_partner_links`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListChannelPartnerLinks`` requests and continue to iterate
    through the ``channel_partner_links`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.channel_v1.types.ListChannelPartnerLinksResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[service.ListChannelPartnerLinksResponse]],
        request: service.ListChannelPartnerLinksRequest,
        response: service.ListChannelPartnerLinksResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.channel_v1.types.ListChannelPartnerLinksRequest):
                The initial request object.
            response (google.cloud.channel_v1.types.ListChannelPartnerLinksResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListChannelPartnerLinksRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[service.ListChannelPartnerLinksResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[channel_partner_links.ChannelPartnerLink]:
        async def async_generator():
            async for page in self.pages:
                for response in page.channel_partner_links:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListProductsPager:
    """A pager for iterating through ``list_products`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.channel_v1.types.ListProductsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``products`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListProducts`` requests and continue to iterate
    through the ``products`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.channel_v1.types.ListProductsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., service.ListProductsResponse],
        request: service.ListProductsRequest,
        response: service.ListProductsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.channel_v1.types.ListProductsRequest):
                The initial request object.
            response (google.cloud.channel_v1.types.ListProductsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListProductsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[service.ListProductsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[products.Product]:
        for page in self.pages:
            yield from page.products

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListProductsAsyncPager:
    """A pager for iterating through ``list_products`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.channel_v1.types.ListProductsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``products`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListProducts`` requests and continue to iterate
    through the ``products`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.channel_v1.types.ListProductsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[service.ListProductsResponse]],
        request: service.ListProductsRequest,
        response: service.ListProductsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.channel_v1.types.ListProductsRequest):
                The initial request object.
            response (google.cloud.channel_v1.types.ListProductsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListProductsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[service.ListProductsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[products.Product]:
        async def async_generator():
            async for page in self.pages:
                for response in page.products:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListSkusPager:
    """A pager for iterating through ``list_skus`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.channel_v1.types.ListSkusResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``skus`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListSkus`` requests and continue to iterate
    through the ``skus`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.channel_v1.types.ListSkusResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., service.ListSkusResponse],
        request: service.ListSkusRequest,
        response: service.ListSkusResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.channel_v1.types.ListSkusRequest):
                The initial request object.
            response (google.cloud.channel_v1.types.ListSkusResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListSkusRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[service.ListSkusResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[products.Sku]:
        for page in self.pages:
            yield from page.skus

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListSkusAsyncPager:
    """A pager for iterating through ``list_skus`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.channel_v1.types.ListSkusResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``skus`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListSkus`` requests and continue to iterate
    through the ``skus`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.channel_v1.types.ListSkusResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[service.ListSkusResponse]],
        request: service.ListSkusRequest,
        response: service.ListSkusResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.channel_v1.types.ListSkusRequest):
                The initial request object.
            response (google.cloud.channel_v1.types.ListSkusResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListSkusRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[service.ListSkusResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[products.Sku]:
        async def async_generator():
            async for page in self.pages:
                for response in page.skus:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListOffersPager:
    """A pager for iterating through ``list_offers`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.channel_v1.types.ListOffersResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``offers`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListOffers`` requests and continue to iterate
    through the ``offers`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.channel_v1.types.ListOffersResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., service.ListOffersResponse],
        request: service.ListOffersRequest,
        response: service.ListOffersResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.channel_v1.types.ListOffersRequest):
                The initial request object.
            response (google.cloud.channel_v1.types.ListOffersResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListOffersRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[service.ListOffersResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[offers.Offer]:
        for page in self.pages:
            yield from page.offers

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListOffersAsyncPager:
    """A pager for iterating through ``list_offers`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.channel_v1.types.ListOffersResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``offers`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListOffers`` requests and continue to iterate
    through the ``offers`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.channel_v1.types.ListOffersResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[service.ListOffersResponse]],
        request: service.ListOffersRequest,
        response: service.ListOffersResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.channel_v1.types.ListOffersRequest):
                The initial request object.
            response (google.cloud.channel_v1.types.ListOffersResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListOffersRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[service.ListOffersResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[offers.Offer]:
        async def async_generator():
            async for page in self.pages:
                for response in page.offers:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListPurchasableSkusPager:
    """A pager for iterating through ``list_purchasable_skus`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.channel_v1.types.ListPurchasableSkusResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``purchasable_skus`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListPurchasableSkus`` requests and continue to iterate
    through the ``purchasable_skus`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.channel_v1.types.ListPurchasableSkusResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., service.ListPurchasableSkusResponse],
        request: service.ListPurchasableSkusRequest,
        response: service.ListPurchasableSkusResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.channel_v1.types.ListPurchasableSkusRequest):
                The initial request object.
            response (google.cloud.channel_v1.types.ListPurchasableSkusResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListPurchasableSkusRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[service.ListPurchasableSkusResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[service.PurchasableSku]:
        for page in self.pages:
            yield from page.purchasable_skus

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListPurchasableSkusAsyncPager:
    """A pager for iterating through ``list_purchasable_skus`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.channel_v1.types.ListPurchasableSkusResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``purchasable_skus`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListPurchasableSkus`` requests and continue to iterate
    through the ``purchasable_skus`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.channel_v1.types.ListPurchasableSkusResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[service.ListPurchasableSkusResponse]],
        request: service.ListPurchasableSkusRequest,
        response: service.ListPurchasableSkusResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.channel_v1.types.ListPurchasableSkusRequest):
                The initial request object.
            response (google.cloud.channel_v1.types.ListPurchasableSkusResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListPurchasableSkusRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[service.ListPurchasableSkusResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[service.PurchasableSku]:
        async def async_generator():
            async for page in self.pages:
                for response in page.purchasable_skus:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListPurchasableOffersPager:
    """A pager for iterating through ``list_purchasable_offers`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.channel_v1.types.ListPurchasableOffersResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``purchasable_offers`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListPurchasableOffers`` requests and continue to iterate
    through the ``purchasable_offers`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.channel_v1.types.ListPurchasableOffersResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., service.ListPurchasableOffersResponse],
        request: service.ListPurchasableOffersRequest,
        response: service.ListPurchasableOffersResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.channel_v1.types.ListPurchasableOffersRequest):
                The initial request object.
            response (google.cloud.channel_v1.types.ListPurchasableOffersResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListPurchasableOffersRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[service.ListPurchasableOffersResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[service.PurchasableOffer]:
        for page in self.pages:
            yield from page.purchasable_offers

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListPurchasableOffersAsyncPager:
    """A pager for iterating through ``list_purchasable_offers`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.channel_v1.types.ListPurchasableOffersResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``purchasable_offers`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListPurchasableOffers`` requests and continue to iterate
    through the ``purchasable_offers`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.channel_v1.types.ListPurchasableOffersResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[service.ListPurchasableOffersResponse]],
        request: service.ListPurchasableOffersRequest,
        response: service.ListPurchasableOffersResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.channel_v1.types.ListPurchasableOffersRequest):
                The initial request object.
            response (google.cloud.channel_v1.types.ListPurchasableOffersResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListPurchasableOffersRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[service.ListPurchasableOffersResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[service.PurchasableOffer]:
        async def async_generator():
            async for page in self.pages:
                for response in page.purchasable_offers:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListSubscribersPager:
    """A pager for iterating through ``list_subscribers`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.channel_v1.types.ListSubscribersResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``service_accounts`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListSubscribers`` requests and continue to iterate
    through the ``service_accounts`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.channel_v1.types.ListSubscribersResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., service.ListSubscribersResponse],
        request: service.ListSubscribersRequest,
        response: service.ListSubscribersResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.channel_v1.types.ListSubscribersRequest):
                The initial request object.
            response (google.cloud.channel_v1.types.ListSubscribersResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListSubscribersRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[service.ListSubscribersResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[str]:
        for page in self.pages:
            yield from page.service_accounts

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListSubscribersAsyncPager:
    """A pager for iterating through ``list_subscribers`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.channel_v1.types.ListSubscribersResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``service_accounts`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListSubscribers`` requests and continue to iterate
    through the ``service_accounts`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.channel_v1.types.ListSubscribersResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[service.ListSubscribersResponse]],
        request: service.ListSubscribersRequest,
        response: service.ListSubscribersResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.channel_v1.types.ListSubscribersRequest):
                The initial request object.
            response (google.cloud.channel_v1.types.ListSubscribersResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = service.ListSubscribersRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[service.ListSubscribersResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[str]:
        async def async_generator():
            async for page in self.pages:
                for response in page.service_accounts:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
