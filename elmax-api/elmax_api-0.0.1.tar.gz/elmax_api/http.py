import asyncio
import functools
import logging
import time
from enum import Enum
from typing import Dict, List, Optional, Union

import httpx
import jwt
from yarl import URL

from elmax_api.constants import BASE_URL, ENDPOINT_LOGIN, USER_AGENT, ENDPOINT_DEVICES, ENDPOINT_DISCOVERY, \
    ENDPOINT_STATUS_ENTITY_ID, ENDPOINT_ENTITY_ID_COMMAND, DEFAULT_HTTP_TIMEOUT, BUSY_WAIT_INTERVAL
from elmax_api.exceptions import ElmaxBadLoginError, ElmaxApiError, ElmaxNetworkError, ElmaxBadPinError, \
    ElmaxPanelBusyError
from elmax_api.model.command import Command
from elmax_api.model.panel import PanelEntry, PanelStatus, EndpointStatus

_LOGGER = logging.getLogger(__name__)
_JWT_ALGS = ["HS256"]


async def helper(f, *args, **kwargs):
    if asyncio.iscoroutinefunction(f):
        return await f(*args, **kwargs)
    else:
        return f(*args, **kwargs)


def async_auth(func, *method_args, **method_kwargs):
    """
    Asynchronous decorator used to check validity of JWT token.
    It takes care to verify the validity of a JWT token before issuing the method call.
    In case the JWT is expired, or close to expiration date, it tries to renew it.
    """
    @functools.wraps(func, *method_args, **method_kwargs)
    async def wrapper(*args, **kwargs):
        # Check whether the client has a valid token to be used. We consider valid tokens with expiration time
        # > 10minutes. If not, try to login first and then proceed with the function call.
        now = time.time()
        _instance = args[0]
        assert isinstance(_instance, Elmax)
        exp_time = _instance.token_expiration_time
        if exp_time == 0:
            _LOGGER.warning("The API client was not authorized yet. Login will be attempted.")
            await _instance.login()
        elif exp_time < 0:
            _LOGGER.warning("The API client token is expired. Login will be attempted.")
            await _instance.login()
        elif (exp_time - now) < 600:
            _LOGGER.info(
                "The API client token is going to be expired soon. "
                "Login will be attempted right now to refresh it."
            )
            await _instance.login()
        # At this point, we assume the client has a valid token to use for authorized APIs. So let's use it.
        result = await helper(func, *args, **kwargs)
        return result

    return wrapper


class Elmax(object):
    """
    Elmax HTTP client.
    This class takes care of handling API calls against the ELMAX API cloud endpoint.
    It handles data marshalling/unmarshalling, login and token renewal upon expiration.
    """

    def __init__(self, username: str, password: str):
        """Client constructor.

        Args:
            username: Username to use for Elmax Authentication
            password: Password to use for Elmax Authentication
        """
        self._username = username
        self._password = password
        self._raw_jwt = None
        self._jwt = None
        self._areas = self._outputs = self._zones = []

    async def _request(
            self,
            method: "Elmax.HttpMethod",
            url: str,
            data: Optional[Dict] = None,
            authorized: bool = False,
            timeout: float = DEFAULT_HTTP_TIMEOUT
    ) -> Dict:
        """
        Executes a HTTP API request against a given endpoint, parses the output and returns the
        json to the caller. It handles most basic IO exceptions.
        If the API returns a non 200 response, this method raises an `ElmaxApiError`

        Args:
            method: HTTP method to use for the HTTP request
            url: Target request URL
            data: Json data/Data to post in POST messages. Ignored when issuing GET requests
            authorized: When set, the request is performed passing the stored authorization token

        Returns:
            Dict: The dictionary object containing authenticated JWT data

        Raises:
            ElmaxApiError: Whenever a non 200 return code is returned by the remote server
            ElmaxNetworkError: If the http request could not be completed due to a network error
        """
        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if authorized:
            headers["Authorization"] = f"JWT {self._raw_jwt}"

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                if method == Elmax.HttpMethod.GET:
                    response = await client.get(str(url), headers=headers, params=data)
                elif method == Elmax.HttpMethod.POST:
                    response = await client.post(str(url), headers=headers, json=data)
                else:
                    raise ValueError("Invalid/Unhandled method. Expecting GET or POST")

                _LOGGER.debug(
                    "HTTP Request %s %s -> Status code: %d",
                    str(method),
                    url,
                    response.status_code,
                )
                if response.status_code != 200:
                    _LOGGER.error(
                        "Api call failed. Method=%s, Url=%s, Data=%s. Response code=%d. Response content=%s",
                        method,
                        url,
                        str(data),
                        response.status_code,
                        str(response.content),
                    )
                    raise ElmaxApiError(status_code=response.status_code)

                # TODO: the current API version does not return an error description nor an error http
                #  status code for invalid logins. Instead, an empty body is returned. In that case we
                #  assume the login failed due to invalid user/pass combination
                response_content = response.text
                if response_content == '':
                    raise ElmaxBadLoginError()

                return response.json()

        # Wrap any other HTTP/NETWORK error
        except (httpx.ConnectError, httpx.ReadTimeout):
            _LOGGER.exception("An unhandled error occurred while executing API Call.")
            raise ElmaxNetworkError("A network error occurred")

    @property
    def is_authenticated(self) -> bool:
        """
        Specifies whether the client has been granted a JWT which is still valid (not expired)

        Returns:
            bool: True if there is a valid JWT token, False if there's no token or if it is expired
        """
        if self._jwt is None:
            # The user did not login yet
            return False
        if self._jwt.get("exp", 0) <= time.time():
            self._jwt = None
            return False
        return True

    @property
    def token_expiration_time(self) -> int:
        """
        Returns the expiration timestamp of the stored JWT token.

        Returns:
            int: The timestamp of expiration or -1 if no token was present.
        """
        if self._jwt is None:
            return 0
        return self._jwt.get("exp", -1)

    @async_auth
    async def logout(self) -> None:
        """
        Invalidate the current token

        TODO:
            * Check if there is a HTTP API to invalidate the current token
        """
        self._jwt = None

    async def login(self) -> Dict:
        """
        Connects to the API ENDPOINT and returns the access token to be used within the client

        Raises:
            ElmaxBadLoginError: if the login attempt fails due to bad username/password credentials
            ValueError: in case the json response is malformed
        """
        url = URL(BASE_URL) / ENDPOINT_LOGIN
        data = {
            "username": self._username,
            "password": self._password,
        }
        try:
            response_data = await self._request(
                method=Elmax.HttpMethod.POST, url=url, data=data, authorized=False
            )
        except ElmaxApiError as e:
            if e.status_code == 401:
                raise ElmaxBadLoginError()
            raise

        if "token" not in response_data:
            raise ValueError("Missing token parameter in json response")

        jwt_token = response_data["token"]
        if not jwt_token.startswith("JWT "):
            raise ValueError("API did not return JWT token as expected")
        jt = jwt_token.split("JWT ")[1]

        # We do not need to verify the signature as this is usually something the server
        # needs to do. We will just decode it to get information about user/claims.
        # Moreover, since the JWT is obtained over a HTTPS channel, we do not need to verify
        # its integrity/confidentiality as the ssl does this for us
        self._jwt = jwt.decode(
            jt, algorithms=_JWT_ALGS, options={"verify_signature": False}
        )
        self._raw_jwt = (
            jt  # keep an encoded version of the JWT for convenience and performance
        )
        return self._jwt

    @async_auth
    async def list_control_panels(self) -> List[PanelEntry]:
        """
        Lists the control panels available for the given user

        Returns:
            List[PanelEntry]: The list of fetched `ControlPanel` devices discovered via the API
        """
        res = []
        url = URL(BASE_URL) / ENDPOINT_DEVICES

        response_data = await self._request(
            method=Elmax.HttpMethod.GET, url=url, authorized=True
        )
        for response_entry in response_data:
            res.append(PanelEntry.from_api_response(response_entry=response_entry))
        return res

    @async_auth
    async def get_panel_status(self,
                               control_panel_id: str,
                               pin: Optional[str] = "000000") -> PanelStatus:
        """
        Fetches the control panel status.

        Args:
            control_panel_id: Id of the control panel to fetch status from
            pin: security pin (optional)

        Returns: The current status of the control panel

        Raises:
             ElmaxBadPinError: Whenever the provided PIN is incorrect or in any way refused by the server
             ElmaxApiError: in case of underlying api call failure
        """
        url = URL(BASE_URL) / ENDPOINT_DISCOVERY / control_panel_id / str(pin)
        try:
            response_data = await self._request(Elmax.HttpMethod.GET, url=url, authorized=True)
        except ElmaxApiError as e:
            if e.status_code == 403:
                raise ElmaxBadPinError() from e
            else:
                raise

        panel_status = PanelStatus.from_api_response(response_entry=response_data)
        return panel_status

    @async_auth
    async def get_endpoint_status(self, endpoint_id: str) -> EndpointStatus:
        """
        Fetches the panel status only for the given endpoint_id

        Args:
            control_panel_id: Id of the control panel to fetch status from
            endpoint_id: Id of the device to fetch data for

        Returns: The current status of the given endpoint
        """
        url = URL(BASE_URL) / ENDPOINT_STATUS_ENTITY_ID / endpoint_id
        response_data = await self._request(Elmax.HttpMethod.GET, url=url, authorized=True)
        status = EndpointStatus.from_api_response(response_entry=response_data)
        return status

    @async_auth
    async def execute_command(self,
                              endpoint_id: str,
                              command: Union[Command, str],
                              extra_payload: Dict = None,
                              retry_attempts: int = 3) -> Optional[Dict]:
        """
        Executes a command against the given endpoint
        Args:
            endpoint_id: EndpointID against which the command should be issued
            command: Command to issue. Can either be a string or a `Command` enum value
            extra_payload: Dictionary of extra payload to be issued to the endpoint
            retry_attempts: Maximum retry attempts in case of 422 error (panel busy)

        Returns: Json response data, if any, returned from the API
        """
        if isinstance(command, Command):
            cmd_str = str(command.value)
        elif isinstance(command, str):
            cmd_str = command
        else:
            raise ValueError("Invalid/unsupported command")

        if extra_payload is not None and not isinstance(extra_payload, dict):
            raise ValueError("The extra_payload parameter must be a dictionary")

        url = URL(BASE_URL) / ENDPOINT_ENTITY_ID_COMMAND / endpoint_id / cmd_str
        retry_attempt = 0
        while retry_attempt < retry_attempts:
            try:
                response_data = await self._request(Elmax.HttpMethod.POST, url=url, authorized=True, data=extra_payload)
                _LOGGER.debug(response_data)
                return response_data
            except ElmaxApiError as e:
                if e.status_code == 422:
                    retry_attempt += 1
                    _LOGGER.error("Panel is busy. Command will be retried in a moment.")
                    await asyncio.sleep(BUSY_WAIT_INTERVAL)
                else:
                    raise
        raise ElmaxPanelBusyError()

    def get_authenticated_username(self) -> Optional[str]:
        """
        Returns the username associated to the current JWT token, if any.
        In case the user is not authenticated, returns None
        """
        if self._jwt is None:
            return None
        return self._jwt.get("email")
                
    class HttpMethod(Enum):
        """Enumerative helper for supported HTTP methods of the Elmax API"""

        GET = "get"
        POST = "post"
