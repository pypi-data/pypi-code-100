"""SDK for building singer-compliant taps."""

from singer_sdk.streams.core import Stream
from singer_sdk.streams.graphql import GraphQLStream
from singer_sdk.streams.rest import RESTStream

__all__ = [
    "Stream",
    "RESTStream",
    "GraphQLStream",
]
