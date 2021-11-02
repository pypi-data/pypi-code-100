"""
Origin Request handler
======================

Operations
----------

- If a client sends a ``GET`` request for a URI that **ends with a slash** (i.e. ``/foo/``) then the handler will transform the request to include the directory's index file (i.e. ``/foo/index.html``).
- If a client sends a ``GET`` request for a URI that **does not end with a slash** and the final item in the path **does not contain a period** (i.e. ``/foo/bar``) then a redirect is returned to the client to try again with a slash (i.e. ``/foo/bar/``)
- ...otherwise, the request is passed unmodified to the origin.

Basic usage
-----------

Create your Lambda function script with this single line:

.. code-block:: python

    from cff.origin_request import handler

Advanced usage
--------------

To configure the handler, run :meth:`configure` with a :class:`.Configuration` instance. For example:

.. code-block:: python

    from cff.origin_request import Configuration, configure, handler

    configure(Configuration(...))
"""

from dataclasses import dataclass
from typing import Any, Optional, Union

from cff.models import Header, LambdaEvent, Request, Response, ResponseHeaders


@dataclass
class Configuration:
    index: str = "index.html"
    """Document to serve when a directory is requested."""


_config = Configuration()


def configure(config: Configuration) -> None:
    """Configure the Origin Request handler."""

    global _config
    _config = config


def handler(
    event: LambdaEvent,
    context: Optional[Any] = None,
) -> Union[Request, Response]:
    """Handler."""
    request = event["Records"][0]["cf"]["request"]

    if request["method"] != "GET":
        # We care only about GETs:
        return request

    uri = request["uri"]

    if uri.endswith("/"):
        # The client requested a directory so we'll request its index file:
        request["uri"] = f"{uri}{_config.index}"
        return request

    uri_parts = uri.split("/")
    leaf = uri_parts[-1]

    if "." in leaf:
        # The client requested a file so we'll pass the request as-is:
        return request

    # The client requested a directory but omitted the trailing slash. We'll ask
    # them to try again with the slash:
    return Response(
        headers=ResponseHeaders(
            location=[
                Header(
                    key="Location",
                    value=f"{uri}/",
                ),
            ]
        ),
        status=301,
    )
