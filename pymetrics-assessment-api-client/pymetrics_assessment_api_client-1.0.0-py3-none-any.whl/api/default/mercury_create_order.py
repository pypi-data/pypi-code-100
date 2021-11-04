from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.mercury_error_response import MercuryErrorResponse
from ...models.mercury_order_create_response import MercuryOrderCreateResponse
from ...models.mercury_order_request import MercuryOrderRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    json_body: MercuryOrderRequest,
    authorization: Union[Unset, str] = UNSET,
    x_api_key: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/mercury/order".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if authorization is not UNSET:
        headers["authorization"] = authorization
    if x_api_key is not UNSET:
        headers["x-api-key"] = x_api_key

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[MercuryErrorResponse, MercuryOrderCreateResponse]]:
    if response.status_code == 200:
        response_200 = MercuryOrderCreateResponse.from_dict(response.json())

        return response_200
    if response.status_code == 201:
        response_201 = MercuryOrderCreateResponse.from_dict(response.json())

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


def _build_response(*, response: httpx.Response) -> Response[Union[MercuryErrorResponse, MercuryOrderCreateResponse]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: MercuryOrderRequest,
    authorization: Union[Unset, str] = UNSET,
    x_api_key: Union[Unset, str] = UNSET,
) -> Response[Union[MercuryErrorResponse, MercuryOrderCreateResponse]]:
    kwargs = _get_kwargs(client=client, json_body=json_body, authorization=authorization, x_api_key=x_api_key,)

    response = httpx.post(verify=client.verify_ssl, **kwargs,)

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    json_body: MercuryOrderRequest,
    authorization: Union[Unset, str] = UNSET,
    x_api_key: Union[Unset, str] = UNSET,
) -> Optional[Union[MercuryErrorResponse, MercuryOrderCreateResponse]]:
    """ Creates an assessment order for a candidate. This represents the transaction for a candidate's job application.

This is an idempotent operation, and may return an existing assessment order. The following inputs constitute the uniqueness criteria:
* `candidate.email`
* `assessment_id`
* `application_id`
 """

    return sync_detailed(client=client, json_body=json_body, authorization=authorization, x_api_key=x_api_key,).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: MercuryOrderRequest,
    authorization: Union[Unset, str] = UNSET,
    x_api_key: Union[Unset, str] = UNSET,
) -> Response[Union[MercuryErrorResponse, MercuryOrderCreateResponse]]:
    kwargs = _get_kwargs(client=client, json_body=json_body, authorization=authorization, x_api_key=x_api_key,)

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: MercuryOrderRequest,
    authorization: Union[Unset, str] = UNSET,
    x_api_key: Union[Unset, str] = UNSET,
) -> Optional[Union[MercuryErrorResponse, MercuryOrderCreateResponse]]:
    """ Creates an assessment order for a candidate. This represents the transaction for a candidate's job application.

This is an idempotent operation, and may return an existing assessment order. The following inputs constitute the uniqueness criteria:
* `candidate.email`
* `assessment_id`
* `application_id`
 """

    return (
        await asyncio_detailed(client=client, json_body=json_body, authorization=authorization, x_api_key=x_api_key,)
    ).parsed
