from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.mercury_configuration import MercuryConfiguration
from ...models.mercury_error_response import MercuryErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *, client: Client, authorization: Union[Unset, str] = UNSET, x_api_key: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/mercury/configuration".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if authorization is not UNSET:
        headers["authorization"] = authorization
    if x_api_key is not UNSET:
        headers["x-api-key"] = x_api_key

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[MercuryConfiguration, MercuryErrorResponse]]:
    if response.status_code == 200:
        response_200 = MercuryConfiguration.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = MercuryErrorResponse.from_dict(response.json())

        return response_401
    if response.status_code == 500:
        response_500 = MercuryErrorResponse.from_dict(response.json())

        return response_500
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[MercuryConfiguration, MercuryErrorResponse]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *, client: Client, authorization: Union[Unset, str] = UNSET, x_api_key: Union[Unset, str] = UNSET,
) -> Response[Union[MercuryConfiguration, MercuryErrorResponse]]:
    kwargs = _get_kwargs(client=client, authorization=authorization, x_api_key=x_api_key,)

    response = httpx.get(verify=client.verify_ssl, **kwargs,)

    return _build_response(response=response)


def sync(
    *, client: Client, authorization: Union[Unset, str] = UNSET, x_api_key: Union[Unset, str] = UNSET,
) -> Optional[Union[MercuryConfiguration, MercuryErrorResponse]]:
    """ Lists the assessment templates that are currently registered for your integration.
These are configured outside of the API, and represent the different candidate experiences
for each role pymetrics is being leveraged for.
 """

    return sync_detailed(client=client, authorization=authorization, x_api_key=x_api_key,).parsed


async def asyncio_detailed(
    *, client: Client, authorization: Union[Unset, str] = UNSET, x_api_key: Union[Unset, str] = UNSET,
) -> Response[Union[MercuryConfiguration, MercuryErrorResponse]]:
    kwargs = _get_kwargs(client=client, authorization=authorization, x_api_key=x_api_key,)

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *, client: Client, authorization: Union[Unset, str] = UNSET, x_api_key: Union[Unset, str] = UNSET,
) -> Optional[Union[MercuryConfiguration, MercuryErrorResponse]]:
    """ Lists the assessment templates that are currently registered for your integration.
These are configured outside of the API, and represent the different candidate experiences
for each role pymetrics is being leveraged for.
 """

    return (await asyncio_detailed(client=client, authorization=authorization, x_api_key=x_api_key,)).parsed
