import json
import urllib
import uuid

import circle
from circle import error, error_classes, http_client
from circle.circle_response import CircleResponse


class APIRequestor:
    def __init__(self, api_key=None, api_base=None, client=None, proxy_url=None):
        self.api_base = api_base or circle.api_base
        self.api_key = api_key or circle.api_key
        self.proxy_url = proxy_url or circle.proxy_url
        if client:
            self._client = client
        elif circle.default_http_client:
            """Users can change the default http client with circle.default_http_client"""
            self._client = circle.default_http_client
        else:
            """If no default http client is set, set one to avoid creating one for every request."""
            circle.default_http_client = http_client.new_default_http_client()
            self._client = circle.default_http_client

    def handle_error_response(self, rbody, rcode, resp, rheaders):
        try:
            err = self.specific_api_error(rbody, rcode, resp, rheaders)
        except (KeyError, TypeError):
            raise error.APIError(
                f"Invalid response from Circle API: {rbody}. HTTP response code {rcode}",
                rbody,
                rcode,
                resp,
            )
        raise err

    def specific_api_error(self, rbody, rcode, resp, rheaders):

        api_error_code = resp["code"]
        try:
            return error_classes.ERROR_CLASSES[api_error_code](
                code=resp["code"],
                body=resp,
                status_code=rcode,
                headers=rheaders,
            )
        except KeyError:
            return error.UnknownError(body=resp, status_code=rcode)

    def interpret_response(self, rbody, rcode, rheaders):
        try:

            resp = CircleResponse(rbody, rcode, rheaders)
        except Exception:
            raise Exception(
                f"Invalid response from API: {rbody} (HTTP response code: {rcode})",
                rbody,
                rcode,
                rheaders,
            )
        if not 200 <= rcode < 300:
            self.handle_error_response(rbody, rcode, resp.data, rheaders)
        return resp

    def request_headers(self, api_key):
        referer = "https://getlinus.io"
        user_agent = "Circle Python SDK"  # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
        headers = {
            "Authorization": "Bearer %s" % api_key,
            "Referer": referer,
            "User-Agent": user_agent,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        return headers

    def request(self, method, url, params={}, headers=None):
        rbody, rcode, rheaders, api_key = self.request_raw(method.lower(), url, params)
        resp = self.interpret_response(rbody, rcode, rheaders)
        return resp, api_key

    def _get_proxies(self, proxy_url):
        proxies = None
        if proxy_url:
            proxies = {"https": proxy_url}
        return proxies

    def request_raw(self, method, url, params={}, supplied_headers=None):
        if self.api_key:
            api_key = self.api_key
        else:
            from circle import api_key

            api_key = api_key

        if api_key is None:
            raise error.MalformedAuthorizationError(message="Missing API key")

        # best effort to populate proxy_url?
        proxy_url = self.proxy_url or circle.proxy_url

        abs_url = "%s%s" % (self.api_base, url)

        if method in (
            "post",
            "put",
            "patch",
        ):
            params.setdefault("idempotencyKey", uuid.uuid4().__str__())
            post_data = json.dumps(params)
        elif method in (
            "get",
            "delete",
        ):
            post_data = None
            if params:
                abs_url = abs_url + "?" + urllib.parse.urlencode(params)
        else:
            raise error.APIConnectionError(
                f"Invalid HTTP method, {method}."
                f"This is probably an issue with the circle SDK."
            )

        headers = self.request_headers(api_key)
        proxies = self._get_proxies(proxy_url)

        if supplied_headers is not None:
            for key, val in supplied_headers.items():
                headers[key] = val

        rbody, rcode, rheaders = self._client.request_with_retries(
            method, abs_url, headers, post_data, proxies
        )

        return rbody, rcode, rheaders, api_key
