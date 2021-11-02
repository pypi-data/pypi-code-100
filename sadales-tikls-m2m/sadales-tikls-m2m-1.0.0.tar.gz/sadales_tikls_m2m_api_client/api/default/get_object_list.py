from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.get_object_list_response_200 import GetObjectListResponse200
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/get-object-list".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "verify": client.verify_ssl,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, GetObjectListResponse200]]:
    if response.status_code == 200:
        response_200 = GetObjectListResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 500:
        response_500 = None

        return response_500
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, GetObjectListResponse200]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
) -> Response[Union[Any, GetObjectListResponse200]]:
    kwargs = _get_kwargs(
        client=client,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
) -> Optional[Union[Any, GetObjectListResponse200]]:
    """The service returns information about the object information available to the customer or their representative in accordance with the APIKEY assigned to the object."""

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
) -> Response[Union[Any, GetObjectListResponse200]]:
    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
) -> Optional[Union[Any, GetObjectListResponse200]]:
    """The service returns information about the object information available to the customer or their representative in accordance with the APIKEY assigned to the object."""

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
