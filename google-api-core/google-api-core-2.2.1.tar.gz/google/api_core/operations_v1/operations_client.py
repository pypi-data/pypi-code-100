# Copyright 2017 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A client for the google.longrunning.operations meta-API.

This is a client that deals with long-running operations that follow the
pattern outlined by the `Google API Style Guide`_.

When an API method normally takes long time to complete, it can be designed to
return ``Operation`` to the client, and the client can use this interface to
receive the real response asynchronously by polling the operation resource to
receive the response.

It is not a separate service, but rather an interface implemented by a larger
service. The protocol-level definition is available at
`google/longrunning/operations.proto`_. Typically, this will be constructed
automatically by another client class to deal with operations.

.. _Google API Style Guide:
    https://cloud.google.com/apis/design/design_pattern
    s#long_running_operations
.. _google/longrunning/operations.proto:
    https://github.com/googleapis/googleapis/blob/master/google/longrunning
    /operations.proto
"""

import functools

from google.api_core import gapic_v1
from google.api_core import page_iterator
from google.api_core.operations_v1 import operations_client_config
from google.longrunning import operations_pb2


class OperationsClient(object):
    """Client for interacting with long-running operations within a service.

    Args:
        channel (grpc.Channel): The gRPC channel associated with the service
            that implements the ``google.longrunning.operations`` interface.
        client_config (dict):
            A dictionary of call options for each method. If not specified
            the default configuration is used.
    """

    def __init__(self, channel, client_config=operations_client_config.config):
        # Create the gRPC client stub.
        self.operations_stub = operations_pb2.OperationsStub(channel)

        # Create all wrapped methods using the interface configuration.
        # The interface config contains all of the default settings for retry
        # and timeout for each RPC method.
        interfaces = client_config["interfaces"]
        interface_config = interfaces["google.longrunning.Operations"]
        method_configs = gapic_v1.config.parse_method_configs(interface_config)

        self._get_operation = gapic_v1.method.wrap_method(
            self.operations_stub.GetOperation,
            default_retry=method_configs["GetOperation"].retry,
            default_timeout=method_configs["GetOperation"].timeout,
        )

        self._list_operations = gapic_v1.method.wrap_method(
            self.operations_stub.ListOperations,
            default_retry=method_configs["ListOperations"].retry,
            default_timeout=method_configs["ListOperations"].timeout,
        )

        self._cancel_operation = gapic_v1.method.wrap_method(
            self.operations_stub.CancelOperation,
            default_retry=method_configs["CancelOperation"].retry,
            default_timeout=method_configs["CancelOperation"].timeout,
        )

        self._delete_operation = gapic_v1.method.wrap_method(
            self.operations_stub.DeleteOperation,
            default_retry=method_configs["DeleteOperation"].retry,
            default_timeout=method_configs["DeleteOperation"].timeout,
        )

    # Service calls
    def get_operation(
        self,
        name,
        retry=gapic_v1.method.DEFAULT,
        timeout=gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """Gets the latest state of a long-running operation.

        Clients can use this method to poll the operation result at intervals
        as recommended by the API service.

        Example:
            >>> from google.api_core import operations_v1
            >>> api = operations_v1.OperationsClient()
            >>> name = ''
            >>> response = api.get_operation(name)

        Args:
            name (str): The name of the operation resource.
            retry (google.api_core.retry.Retry): The retry strategy to use
                when invoking the RPC. If unspecified, the default retry from
                the client configuration will be used. If ``None``, then this
                method will not retry the RPC at all.
            timeout (float): The amount of time in seconds to wait for the RPC
                to complete. Note that if ``retry`` is used, this timeout
                applies to each individual attempt and the overall time it
                takes for this method to complete may be longer. If
                unspecified, the the default timeout in the client
                configuration is used. If ``None``, then the RPC method will
                not time out.
            metadata (Optional[List[Tuple[str, str]]]):
                Additional gRPC metadata.

        Returns:
            google.longrunning.operations_pb2.Operation: The state of the
                operation.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If an error occurred
                while invoking the RPC, the appropriate ``GoogleAPICallError``
                subclass will be raised.
        """
        request = operations_pb2.GetOperationRequest(name=name)

        # Add routing header
        metadata = metadata or []
        metadata.append(gapic_v1.routing_header.to_grpc_metadata({"name": name}))

        return self._get_operation(
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_operations(
        self,
        name,
        filter_,
        retry=gapic_v1.method.DEFAULT,
        timeout=gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists operations that match the specified filter in the request.

        Example:
            >>> from google.api_core import operations_v1
            >>> api = operations_v1.OperationsClient()
            >>> name = ''
            >>>
            >>> # Iterate over all results
            >>> for operation in api.list_operations(name):
            >>>   # process operation
            >>>   pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> iter = api.list_operations(name)
            >>> for page in iter.pages:
            >>>   for operation in page:
            >>>     # process operation
            >>>     pass

        Args:
            name (str): The name of the operation collection.
            filter_ (str): The standard list filter.
            retry (google.api_core.retry.Retry): The retry strategy to use
                when invoking the RPC. If unspecified, the default retry from
                the client configuration will be used. If ``None``, then this
                method will not retry the RPC at all.
            timeout (float): The amount of time in seconds to wait for the RPC
                to complete. Note that if ``retry`` is used, this timeout
                applies to each individual attempt and the overall time it
                takes for this method to complete may be longer. If
                unspecified, the the default timeout in the client
                configuration is used. If ``None``, then the RPC method will
                not time out.
            metadata (Optional[List[Tuple[str, str]]]): Additional gRPC
                metadata.

        Returns:
            google.api_core.page_iterator.Iterator: An iterator that yields
                :class:`google.longrunning.operations_pb2.Operation` instances.

        Raises:
            google.api_core.exceptions.MethodNotImplemented: If the server
                does not support this method. Services are not required to
                implement this method.
            google.api_core.exceptions.GoogleAPICallError: If an error occurred
                while invoking the RPC, the appropriate ``GoogleAPICallError``
                subclass will be raised.
        """
        # Create the request object.
        request = operations_pb2.ListOperationsRequest(name=name, filter=filter_)

        # Add routing header
        metadata = metadata or []
        metadata.append(gapic_v1.routing_header.to_grpc_metadata({"name": name}))

        # Create the method used to fetch pages
        method = functools.partial(
            self._list_operations, retry=retry, timeout=timeout, metadata=metadata
        )

        iterator = page_iterator.GRPCIterator(
            client=None,
            method=method,
            request=request,
            items_field="operations",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )

        return iterator

    def cancel_operation(
        self,
        name,
        retry=gapic_v1.method.DEFAULT,
        timeout=gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """Starts asynchronous cancellation on a long-running operation.

        The server makes a best effort to cancel the operation, but success is
        not guaranteed. Clients can use :meth:`get_operation` or service-
        specific methods to check whether the cancellation succeeded or whether
        the operation completed despite cancellation. On successful
        cancellation, the operation is not deleted; instead, it becomes an
        operation with an ``Operation.error`` value with a
        ``google.rpc.Status.code`` of ``1``, corresponding to
        ``Code.CANCELLED``.

        Example:
            >>> from google.api_core import operations_v1
            >>> api = operations_v1.OperationsClient()
            >>> name = ''
            >>> api.cancel_operation(name)

        Args:
            name (str): The name of the operation resource to be cancelled.
            retry (google.api_core.retry.Retry): The retry strategy to use
                when invoking the RPC. If unspecified, the default retry from
                the client configuration will be used. If ``None``, then this
                method will not retry the RPC at all.
            timeout (float): The amount of time in seconds to wait for the RPC
                to complete. Note that if ``retry`` is used, this timeout
                applies to each individual attempt and the overall time it
                takes for this method to complete may be longer. If
                unspecified, the the default timeout in the client
                configuration is used. If ``None``, then the RPC method will
                not time out.
            metadata (Optional[List[Tuple[str, str]]]): Additional gRPC
                metadata.

        Raises:
            google.api_core.exceptions.MethodNotImplemented: If the server
                does not support this method. Services are not required to
                implement this method.
            google.api_core.exceptions.GoogleAPICallError: If an error occurred
                while invoking the RPC, the appropriate ``GoogleAPICallError``
                subclass will be raised.
        """
        # Create the request object.
        request = operations_pb2.CancelOperationRequest(name=name)

        # Add routing header
        metadata = metadata or []
        metadata.append(gapic_v1.routing_header.to_grpc_metadata({"name": name}))

        self._cancel_operation(request, retry=retry, timeout=timeout, metadata=metadata)

    def delete_operation(
        self,
        name,
        retry=gapic_v1.method.DEFAULT,
        timeout=gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """Deletes a long-running operation.

        This method indicates that the client is no longer interested in the
        operation result. It does not cancel the operation.

        Example:
            >>> from google.api_core import operations_v1
            >>> api = operations_v1.OperationsClient()
            >>> name = ''
            >>> api.delete_operation(name)

        Args:
            name (str): The name of the operation resource to be deleted.
            retry (google.api_core.retry.Retry): The retry strategy to use
                when invoking the RPC. If unspecified, the default retry from
                the client configuration will be used. If ``None``, then this
                method will not retry the RPC at all.
            timeout (float): The amount of time in seconds to wait for the RPC
                to complete. Note that if ``retry`` is used, this timeout
                applies to each individual attempt and the overall time it
                takes for this method to complete may be longer. If
                unspecified, the the default timeout in the client
                configuration is used. If ``None``, then the RPC method will
                not time out.
            metadata (Optional[List[Tuple[str, str]]]): Additional gRPC
                metadata.

        Raises:
            google.api_core.exceptions.MethodNotImplemented: If the server
                does not support this method. Services are not required to
                implement this method.
            google.api_core.exceptions.GoogleAPICallError: If an error occurred
                while invoking the RPC, the appropriate ``GoogleAPICallError``
                subclass will be raised.
        """
        # Create the request object.
        request = operations_pb2.DeleteOperationRequest(name=name)

        # Add routing header
        metadata = metadata or []
        metadata.append(gapic_v1.routing_header.to_grpc_metadata({"name": name}))

        self._delete_operation(request, retry=retry, timeout=timeout, metadata=metadata)
