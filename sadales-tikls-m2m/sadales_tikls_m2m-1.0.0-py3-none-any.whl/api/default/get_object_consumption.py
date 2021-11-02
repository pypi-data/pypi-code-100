import datetime
from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.get_object_consumption_response_200_item import GetObjectConsumptionResponse200Item
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    o_eic: str,
    mp_nr: Union[Unset, None, str] = UNSET,
    m_nr: Union[Unset, None, str] = UNSET,
    d_f: datetime.datetime,
    d_t: datetime.datetime,
) -> Dict[str, Any]:
    url = "{}/get-object-consumption".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_d_f = d_f.isoformat()

    json_d_t = d_t.isoformat()

    params: Dict[str, Any] = {
        "oEIC": o_eic,
        "mpNr": mp_nr,
        "mNr": m_nr,
        "dF": json_d_f,
        "dT": json_d_t,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
        "verify": client.verify_ssl,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, List[GetObjectConsumptionResponse200Item]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = GetObjectConsumptionResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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


def _build_response(*, response: httpx.Response) -> Response[Union[Any, List[GetObjectConsumptionResponse200Item]]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    o_eic: str,
    mp_nr: Union[Unset, None, str] = UNSET,
    m_nr: Union[Unset, None, str] = UNSET,
    d_f: datetime.datetime,
    d_t: datetime.datetime,
) -> Response[Union[Any, List[GetObjectConsumptionResponse200Item]]]:
    kwargs = _get_kwargs(
        client=client,
        o_eic=o_eic,
        mp_nr=mp_nr,
        m_nr=m_nr,
        d_f=d_f,
        d_t=d_t,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    o_eic: str,
    mp_nr: Union[Unset, None, str] = UNSET,
    m_nr: Union[Unset, None, str] = UNSET,
    d_f: datetime.datetime,
    d_t: datetime.datetime,
) -> Optional[Union[Any, List[GetObjectConsumptionResponse200Item]]]:
    """The service returns data according to the APIKEY assigned to the object in addition to the rest of parameters for the data request. The service provides the consumption information only for objects with smart meters. The service provides information about both the consumption used for billing and the actual consumption from the smart meter, which was successfully read the first time the meter was read.
    Additional terms of use Maximum available consumption data period: one year from the end of the current billing period. If the request period exceeds one year, only one year of data, counting from the dT value element, is returned, i.e. for the last 365 days.
    """

    return sync_detailed(
        client=client,
        o_eic=o_eic,
        mp_nr=mp_nr,
        m_nr=m_nr,
        d_f=d_f,
        d_t=d_t,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    o_eic: str,
    mp_nr: Union[Unset, None, str] = UNSET,
    m_nr: Union[Unset, None, str] = UNSET,
    d_f: datetime.datetime,
    d_t: datetime.datetime,
) -> Response[Union[Any, List[GetObjectConsumptionResponse200Item]]]:
    kwargs = _get_kwargs(
        client=client,
        o_eic=o_eic,
        mp_nr=mp_nr,
        m_nr=m_nr,
        d_f=d_f,
        d_t=d_t,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    o_eic: str,
    mp_nr: Union[Unset, None, str] = UNSET,
    m_nr: Union[Unset, None, str] = UNSET,
    d_f: datetime.datetime,
    d_t: datetime.datetime,
) -> Optional[Union[Any, List[GetObjectConsumptionResponse200Item]]]:
    """The service returns data according to the APIKEY assigned to the object in addition to the rest of parameters for the data request. The service provides the consumption information only for objects with smart meters. The service provides information about both the consumption used for billing and the actual consumption from the smart meter, which was successfully read the first time the meter was read.
    Additional terms of use Maximum available consumption data period: one year from the end of the current billing period. If the request period exceeds one year, only one year of data, counting from the dT value element, is returned, i.e. for the last 365 days.
    """

    return (
        await asyncio_detailed(
            client=client,
            o_eic=o_eic,
            mp_nr=mp_nr,
            m_nr=m_nr,
            d_f=d_f,
            d_t=d_t,
        )
    ).parsed
