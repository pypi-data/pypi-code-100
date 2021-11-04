from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.mercury_error_response import MercuryErrorResponse
from ...models.o_auth_token_request import OAuthTokenRequest
from ...models.o_auth_token_response import OAuthTokenResponse
from ...types import Response


def _get_kwargs(*, client: Client, json_body: OAuthTokenRequest,) -> Dict[str, Any]:
    url = "{}/mercury/oauth/token".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[MercuryErrorResponse, OAuthTokenResponse]]:
    if response.status_code == 201:
        response_201 = OAuthTokenResponse.from_dict(response.json())

        return response_201
    if response.status_code == 400:
        response_400 = MercuryErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = MercuryErrorResponse.from_dict(response.json())

        return response_401
    if response.status_code == 500:
        response_500 = MercuryErrorResponse.from_dict(response.json())

        return response_500
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[MercuryErrorResponse, OAuthTokenResponse]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *, client: Client, json_body: OAuthTokenRequest,
) -> Response[Union[MercuryErrorResponse, OAuthTokenResponse]]:
    kwargs = _get_kwargs(client=client, json_body=json_body,)

    response = httpx.post(verify=client.verify_ssl, **kwargs,)

    return _build_response(response=response)


def sync(*, client: Client, json_body: OAuthTokenRequest,) -> Optional[Union[MercuryErrorResponse, OAuthTokenResponse]]:
    """ The response's bearer token must be used in the `Authorization` header for any other API request. Tokens are valid for only a period of time.

All requests, with the exception of this one, also require an API Key to be supplied in the `X-Api-Key` request header.
pymetrics will supply this along with the OAuth Client ID and Secret.
 """

    return sync_detailed(client=client, json_body=json_body,).parsed


async def asyncio_detailed(
    *, client: Client, json_body: OAuthTokenRequest,
) -> Response[Union[MercuryErrorResponse, OAuthTokenResponse]]:
    kwargs = _get_kwargs(client=client, json_body=json_body,)

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *, client: Client, json_body: OAuthTokenRequest,
) -> Optional[Union[MercuryErrorResponse, OAuthTokenResponse]]:
    """ The response's bearer token must be used in the `Authorization` header for any other API request. Tokens are valid for only a period of time.

All requests, with the exception of this one, also require an API Key to be supplied in the `X-Api-Key` request header.
pymetrics will supply this along with the OAuth Client ID and Secret.
 """

    return (await asyncio_detailed(client=client, json_body=json_body,)).parsed
