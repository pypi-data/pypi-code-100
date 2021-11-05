import json as json_
import typing

import aiohttp

from .exceptions import ApiException


def make_url(hostname: str, api_method: str, branch_id: int = 0) -> str:
    """
    Make url for api call
    :param hostname: hostname
    :param api_method: api method
    :param branch_id: branch id
    :return: full url
    """
    if branch_id:
        return f"https://{hostname}/v2api/{branch_id}/{api_method}"
    else:
        return f"https://{hostname}/v2api/{api_method}"


def check_response(
        code: int,
        body: str,
        request_info: typing.Optional[aiohttp.RequestInfo] = None
) -> typing.Dict[str, typing.Any]:
    """
    Check response
    :param code: response code
    :param request_info: request info
    :param body: response text
    :return: checked response
    """
    if code >= 500:
        raise ApiException(code, body, request_info)

    try:
        json_response = json_.loads(body)
    except ValueError:
        json_response = {}

    if code >= 400:
        raise ApiException(code, json_response.get("errors") or json_response.get("message") or body, request_info)

    return json_response
