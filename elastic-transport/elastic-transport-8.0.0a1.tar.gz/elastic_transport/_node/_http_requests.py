#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

import gzip
import ssl
import time
import warnings
from typing import Any, Optional, Tuple, Union

import urllib3  # type: ignore[import]

from .._compat import warn_stacklevel
from .._exceptions import ConnectionError, ConnectionTimeout, SecurityWarning, TlsError
from .._models import ApiResponseMeta, HttpHeaders, NodeConfig
from ..client_utils import DEFAULT, DefaultType, client_meta_version
from ._base import (
    BUILTIN_EXCEPTIONS,
    RERAISE_EXCEPTIONS,
    BaseNode,
    ssl_context_from_node_config,
)

try:
    import requests
    from requests.adapters import HTTPAdapter

    _REQUESTS_AVAILABLE = True
    _REQUESTS_META_VERSION = client_meta_version(requests.__version__)

    # Use our custom HTTPSConnectionPool for chain cert fingerprint support.
    try:
        from ._urllib3_chain_certs import HTTPSConnectionPool
    except (ImportError, AttributeError):
        HTTPSConnectionPool = urllib3.HTTPSConnectionPool  # type: ignore[misc]

    class _ElasticHTTPAdapter(HTTPAdapter):
        def __init__(self, node_config: NodeConfig, **kwargs: Any) -> None:
            self._node_config = node_config
            super().__init__(**kwargs)

        def init_poolmanager(
            self,
            connections: Any,
            maxsize: int,
            block: bool = False,
            **pool_kwargs: Any,
        ) -> None:

            if self._node_config.scheme == "https":
                ssl_context = ssl_context_from_node_config(self._node_config)
                pool_kwargs.setdefault("ssl_context", ssl_context)

            if self._node_config.ssl_assert_fingerprint:
                pool_kwargs.setdefault(
                    "assert_fingerprint", self._node_config.ssl_assert_fingerprint
                )

            super().init_poolmanager(connections, maxsize, block=block, **pool_kwargs)  # type: ignore [no-untyped-call]
            self.poolmanager.pool_classes_by_scheme["https"] = HTTPSConnectionPool


except ImportError:  # pragma: nocover
    _REQUESTS_AVAILABLE = False
    _REQUESTS_META_VERSION = ""


class RequestsHttpNode(BaseNode):
    """Synchronous node using the ``requests`` library communicating via HTTP"""

    _CLIENT_META_HTTP_CLIENT = ("rq", _REQUESTS_META_VERSION)

    def __init__(self, config: NodeConfig):
        if not _REQUESTS_AVAILABLE:  # pragma: nocover
            raise ValueError(
                "You must have 'requests' installed to use RequestsHttpNode"
            )

        super().__init__(config)

        # Initialize Session so .headers works before calling super().__init__().
        self.session = requests.Session()
        self.session.headers.clear()  # Empty out all the default session headers
        self.session.verify = config.verify_certs

        # Client certificates
        if config.client_cert:
            if config.client_key:
                self.session.cert = (config.client_cert, config.client_key)
            else:
                self.session.cert = config.client_cert

        if config.ca_certs:
            if not config.verify_certs:
                raise ValueError(
                    "You cannot pass CA certificates when verify_ssl=False."
                )
            self.session.verify = config.ca_certs

        if not config.ssl_show_warn:
            urllib3.disable_warnings()

        if (
            config.scheme == "https"
            and not config.verify_certs
            and config.ssl_show_warn
        ):
            warnings.warn(
                f"Connecting to {self.base_url!r} using TLS with verify_certs=False is insecure",
                stacklevel=warn_stacklevel(),
                category=SecurityWarning,
            )

        # Create and mount custom adapter for constraining number of connections
        adapter = _ElasticHTTPAdapter(
            node_config=config,
            pool_connections=config.connections_per_node,
            pool_maxsize=config.connections_per_node,
            pool_block=True,
        )
        # Preload the HTTPConnectionPool so initialization issues
        # are raised here instead of in perform_request()
        adapter.get_connection(self.base_url)  # type: ignore[no-untyped-call]
        self.session.mount(prefix=f"{self.scheme}://", adapter=adapter)

    def perform_request(
        self,
        method: str,
        target: str,
        body: Optional[bytes] = None,
        headers: Optional[HttpHeaders] = None,
        request_timeout: Union[DefaultType, Optional[float]] = DEFAULT,
    ) -> Tuple[ApiResponseMeta, bytes]:
        url = self.base_url + target
        headers = HttpHeaders(headers or ())

        request_headers = self._headers.copy()
        if headers:
            request_headers.update(headers)

        if body:
            if self._http_compress:
                body = gzip.compress(body)
                request_headers["content-encoding"] = "gzip"
        else:
            body = None

        start = time.time()
        request = requests.Request(
            method=method, headers=request_headers, url=url, data=body
        )
        prepared_request = self.session.prepare_request(request)
        send_kwargs = {
            "timeout": request_timeout
            if request_timeout is not DEFAULT
            else self.config.request_timeout
        }
        send_kwargs.update(
            self.session.merge_environment_settings(  # type: ignore[no-untyped-call]
                prepared_request.url, {}, None, None, None
            )
        )
        try:
            response = self.session.send(prepared_request, **send_kwargs)
            data = response.content
            duration = time.time() - start
            response_headers = HttpHeaders(response.headers)

        except RERAISE_EXCEPTIONS:
            raise
        except Exception as e:
            if isinstance(e, requests.Timeout):
                raise ConnectionTimeout(
                    "Connection timed out during request", errors=(e,)
                ) from None
            elif isinstance(e, (ssl.SSLError, requests.exceptions.SSLError)):
                raise TlsError(str(e), errors=(e,)) from None
            elif isinstance(e, BUILTIN_EXCEPTIONS):
                raise
            raise ConnectionError(str(e), errors=(e,)) from None

        return (
            ApiResponseMeta(
                node=self.config,
                duration=duration,
                http_version="1.1",
                status=response.status_code,
                headers=response_headers,
            ),
            data,
        )

    def close(self) -> None:
        """
        Explicitly closes connections
        """
        self.session.close()
