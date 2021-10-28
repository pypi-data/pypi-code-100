import json
import logging
from datetime import date, datetime
from gzip import GzipFile
from io import BytesIO
from typing import Any, Optional, Union

import requests
from dateutil.tz import tzutc

from posthog.utils import remove_trailing_slash
from posthog.version import VERSION

_session = requests.sessions.Session()

DEFAULT_HOST = "https://app.posthog.com"
USER_AGENT = "posthog-python/" + VERSION


def post(
    api_key: str, host: Optional[str] = None, path=None, gzip: bool = False, timeout: int = 15, **kwargs
) -> requests.Response:
    """Post the `kwargs` to the API"""
    log = logging.getLogger("posthog")
    body = kwargs
    body["sentAt"] = datetime.utcnow().replace(tzinfo=tzutc()).isoformat()
    url = remove_trailing_slash(host or DEFAULT_HOST) + path
    body["api_key"] = api_key
    data = json.dumps(body, cls=DatetimeSerializer)
    log.debug("making request: %s", data)
    headers = {"Content-Type": "application/json", "User-Agent": USER_AGENT}
    if gzip:
        headers["Content-Encoding"] = "gzip"
        buf = BytesIO()
        with GzipFile(fileobj=buf, mode="w") as gz:
            # 'data' was produced by json.dumps(),
            # whose default encoding is utf-8.
            gz.write(data.encode("utf-8"))
        data = buf.getvalue()

    res = _session.post(url, data=data, headers=headers, timeout=timeout)

    if res.status_code == 200:
        log.debug("data uploaded successfully")

    return res


def _process_response(
    res: requests.Response, success_message: str, *, return_json: bool = True
) -> Union[requests.Response, Any]:
    log = logging.getLogger("posthog")
    if not res:
        raise APIError(
            "N/A",
            "Error when fetching PostHog API, please make sure you are using your public project token/key and not a private API key.",
        )
    if res.status_code == 200:
        log.debug(success_message)
        return res.json() if return_json else res
    try:
        payload = res.json()
        log.debug("received response: %s", payload)
        raise APIError(res.status_code, payload["detail"])
    except ValueError:
        raise APIError(res.status_code, res.text)


def decide(api_key: str, host: Optional[str] = None, gzip: bool = False, timeout: int = 15, **kwargs) -> Any:
    """Post the `kwargs to the decide API endpoint"""
    res = post(api_key, host, "/decide/", gzip, timeout, **kwargs)
    return _process_response(res, success_message="Feature flags decided successfully")


def batch_post(
    api_key: str, host: Optional[str] = None, gzip: bool = False, timeout: int = 15, **kwargs
) -> requests.Response:
    """Post the `kwargs` to the batch API endpoint for events"""
    res = post(api_key, host, "/batch/", gzip, timeout, **kwargs)
    return _process_response(res, success_message="data uploaded successfully", return_json=False)


def get(api_key: str, url: str, host: Optional[str] = None, timeout: Optional[int] = None) -> requests.Response:
    url = remove_trailing_slash(host or DEFAULT_HOST) + url
    res = requests.get(url, headers={"Authorization": "Bearer %s" % api_key, "User-Agent": USER_AGENT}, timeout=timeout)
    return _process_response(res, success_message=f"GET {url} completed successfully")


class APIError(Exception):
    def __init__(self, status: Union[int, str], message: str):
        self.message = message
        self.status = status

    def __str__(self):
        msg = "[PostHog] {0} ({1})"
        return msg.format(self.message, self.status)


class DatetimeSerializer(json.JSONEncoder):
    def default(self, obj: Any):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()

        return json.JSONEncoder.default(self, obj)
