from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.mercury_assessment_order import MercuryAssessmentOrder
from ...models.mercury_error_response import MercuryErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    uuid: str,
    *,
    client: Client,
    report: Union[Unset, None, bool] = UNSET,
    authorization: Union[Unset, str] = UNSET,
    x_api_key: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/mercury/getOrder/{uuid}".format(client.base_url, uuid=uuid)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if authorization is not UNSET:
        headers["authorization"] = authorization
    if x_api_key is not UNSET:
        headers["x-api-key"] = x_api_key

    params: Dict[str, Any] = {
        "report": report,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[MercuryAssessmentOrder, MercuryErrorResponse]]:
    if response.status_code == 200:
        response_200 = MercuryAssessmentOrder.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = MercuryErrorResponse.from_dict(response.json())

        return response_404
    if response.status_code == 500:
        response_500 = MercuryErrorResponse.from_dict(response.json())

        return response_500
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[MercuryAssessmentOrder, MercuryErrorResponse]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    uuid: str,
    *,
    client: Client,
    report: Union[Unset, None, bool] = UNSET,
    authorization: Union[Unset, str] = UNSET,
    x_api_key: Union[Unset, str] = UNSET,
) -> Response[Union[MercuryAssessmentOrder, MercuryErrorResponse]]:
    kwargs = _get_kwargs(uuid=uuid, client=client, report=report, authorization=authorization, x_api_key=x_api_key,)

    response = httpx.get(verify=client.verify_ssl, **kwargs,)

    return _build_response(response=response)


def sync(
    uuid: str,
    *,
    client: Client,
    report: Union[Unset, None, bool] = UNSET,
    authorization: Union[Unset, str] = UNSET,
    x_api_key: Union[Unset, str] = UNSET,
) -> Optional[Union[MercuryAssessmentOrder, MercuryErrorResponse]]:
    """ Get an existing order by ID. It will move from `Completed` to `Fulfilled` if the order has results. """

    return sync_detailed(
        uuid=uuid, client=client, report=report, authorization=authorization, x_api_key=x_api_key,
    ).parsed


async def asyncio_detailed(
    uuid: str,
    *,
    client: Client,
    report: Union[Unset, None, bool] = UNSET,
    authorization: Union[Unset, str] = UNSET,
    x_api_key: Union[Unset, str] = UNSET,
) -> Response[Union[MercuryAssessmentOrder, MercuryErrorResponse]]:
    kwargs = _get_kwargs(uuid=uuid, client=client, report=report, authorization=authorization, x_api_key=x_api_key,)

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    uuid: str,
    *,
    client: Client,
    report: Union[Unset, None, bool] = UNSET,
    authorization: Union[Unset, str] = UNSET,
    x_api_key: Union[Unset, str] = UNSET,
) -> Optional[Union[MercuryAssessmentOrder, MercuryErrorResponse]]:
    """ Get an existing order by ID. It will move from `Completed` to `Fulfilled` if the order has results. """

    return (
        await asyncio_detailed(
            uuid=uuid, client=client, report=report, authorization=authorization, x_api_key=x_api_key,
        )
    ).parsed
