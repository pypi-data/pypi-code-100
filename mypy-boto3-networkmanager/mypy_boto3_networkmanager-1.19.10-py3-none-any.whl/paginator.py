"""
Type annotations for networkmanager service client paginators.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators.html)

Usage::

    ```python
    import boto3

    from mypy_boto3_networkmanager import NetworkManagerClient
    from mypy_boto3_networkmanager.paginator import (
        DescribeGlobalNetworksPaginator,
        GetConnectionsPaginator,
        GetCustomerGatewayAssociationsPaginator,
        GetDevicesPaginator,
        GetLinkAssociationsPaginator,
        GetLinksPaginator,
        GetNetworkResourceCountsPaginator,
        GetNetworkResourceRelationshipsPaginator,
        GetNetworkResourcesPaginator,
        GetNetworkTelemetryPaginator,
        GetSitesPaginator,
        GetTransitGatewayConnectPeerAssociationsPaginator,
        GetTransitGatewayRegistrationsPaginator,
    )

    client: NetworkManagerClient = boto3.client("networkmanager")

    describe_global_networks_paginator: DescribeGlobalNetworksPaginator = client.get_paginator("describe_global_networks")
    get_connections_paginator: GetConnectionsPaginator = client.get_paginator("get_connections")
    get_customer_gateway_associations_paginator: GetCustomerGatewayAssociationsPaginator = client.get_paginator("get_customer_gateway_associations")
    get_devices_paginator: GetDevicesPaginator = client.get_paginator("get_devices")
    get_link_associations_paginator: GetLinkAssociationsPaginator = client.get_paginator("get_link_associations")
    get_links_paginator: GetLinksPaginator = client.get_paginator("get_links")
    get_network_resource_counts_paginator: GetNetworkResourceCountsPaginator = client.get_paginator("get_network_resource_counts")
    get_network_resource_relationships_paginator: GetNetworkResourceRelationshipsPaginator = client.get_paginator("get_network_resource_relationships")
    get_network_resources_paginator: GetNetworkResourcesPaginator = client.get_paginator("get_network_resources")
    get_network_telemetry_paginator: GetNetworkTelemetryPaginator = client.get_paginator("get_network_telemetry")
    get_sites_paginator: GetSitesPaginator = client.get_paginator("get_sites")
    get_transit_gateway_connect_peer_associations_paginator: GetTransitGatewayConnectPeerAssociationsPaginator = client.get_paginator("get_transit_gateway_connect_peer_associations")
    get_transit_gateway_registrations_paginator: GetTransitGatewayRegistrationsPaginator = client.get_paginator("get_transit_gateway_registrations")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    DescribeGlobalNetworksResponseTypeDef,
    GetConnectionsResponseTypeDef,
    GetCustomerGatewayAssociationsResponseTypeDef,
    GetDevicesResponseTypeDef,
    GetLinkAssociationsResponseTypeDef,
    GetLinksResponseTypeDef,
    GetNetworkResourceCountsResponseTypeDef,
    GetNetworkResourceRelationshipsResponseTypeDef,
    GetNetworkResourcesResponseTypeDef,
    GetNetworkTelemetryResponseTypeDef,
    GetSitesResponseTypeDef,
    GetTransitGatewayConnectPeerAssociationsResponseTypeDef,
    GetTransitGatewayRegistrationsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "DescribeGlobalNetworksPaginator",
    "GetConnectionsPaginator",
    "GetCustomerGatewayAssociationsPaginator",
    "GetDevicesPaginator",
    "GetLinkAssociationsPaginator",
    "GetLinksPaginator",
    "GetNetworkResourceCountsPaginator",
    "GetNetworkResourceRelationshipsPaginator",
    "GetNetworkResourcesPaginator",
    "GetNetworkTelemetryPaginator",
    "GetSitesPaginator",
    "GetTransitGatewayConnectPeerAssociationsPaginator",
    "GetTransitGatewayRegistrationsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeGlobalNetworksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/networkmanager.html#NetworkManager.Paginator.DescribeGlobalNetworks)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators.html#describeglobalnetworkspaginator)
    """

    def paginate(
        self,
        *,
        GlobalNetworkIds: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeGlobalNetworksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/networkmanager.html#NetworkManager.Paginator.DescribeGlobalNetworks.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators.html#describeglobalnetworkspaginator)
        """


class GetConnectionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/networkmanager.html#NetworkManager.Paginator.GetConnections)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators.html#getconnectionspaginator)
    """

    def paginate(
        self,
        *,
        GlobalNetworkId: str,
        ConnectionIds: Sequence[str] = ...,
        DeviceId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetConnectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/networkmanager.html#NetworkManager.Paginator.GetConnections.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators.html#getconnectionspaginator)
        """


class GetCustomerGatewayAssociationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/networkmanager.html#NetworkManager.Paginator.GetCustomerGatewayAssociations)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators.html#getcustomergatewayassociationspaginator)
    """

    def paginate(
        self,
        *,
        GlobalNetworkId: str,
        CustomerGatewayArns: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetCustomerGatewayAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/networkmanager.html#NetworkManager.Paginator.GetCustomerGatewayAssociations.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators.html#getcustomergatewayassociationspaginator)
        """


class GetDevicesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/networkmanager.html#NetworkManager.Paginator.GetDevices)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators.html#getdevicespaginator)
    """

    def paginate(
        self,
        *,
        GlobalNetworkId: str,
        DeviceIds: Sequence[str] = ...,
        SiteId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/networkmanager.html#NetworkManager.Paginator.GetDevices.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators.html#getdevicespaginator)
        """


class GetLinkAssociationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/networkmanager.html#NetworkManager.Paginator.GetLinkAssociations)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators.html#getlinkassociationspaginator)
    """

    def paginate(
        self,
        *,
        GlobalNetworkId: str,
        DeviceId: str = ...,
        LinkId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetLinkAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/networkmanager.html#NetworkManager.Paginator.GetLinkAssociations.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators.html#getlinkassociationspaginator)
        """


class GetLinksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/networkmanager.html#NetworkManager.Paginator.GetLinks)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators.html#getlinkspaginator)
    """

    def paginate(
        self,
        *,
        GlobalNetworkId: str,
        LinkIds: Sequence[str] = ...,
        SiteId: str = ...,
        Type: str = ...,
        Provider: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetLinksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/networkmanager.html#NetworkManager.Paginator.GetLinks.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators.html#getlinkspaginator)
        """


class GetNetworkResourceCountsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/networkmanager.html#NetworkManager.Paginator.GetNetworkResourceCounts)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators.html#getnetworkresourcecountspaginator)
    """

    def paginate(
        self,
        *,
        GlobalNetworkId: str,
        ResourceType: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetNetworkResourceCountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/networkmanager.html#NetworkManager.Paginator.GetNetworkResourceCounts.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators.html#getnetworkresourcecountspaginator)
        """


class GetNetworkResourceRelationshipsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/networkmanager.html#NetworkManager.Paginator.GetNetworkResourceRelationships)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators.html#getnetworkresourcerelationshipspaginator)
    """

    def paginate(
        self,
        *,
        GlobalNetworkId: str,
        RegisteredGatewayArn: str = ...,
        AwsRegion: str = ...,
        AccountId: str = ...,
        ResourceType: str = ...,
        ResourceArn: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetNetworkResourceRelationshipsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/networkmanager.html#NetworkManager.Paginator.GetNetworkResourceRelationships.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators.html#getnetworkresourcerelationshipspaginator)
        """


class GetNetworkResourcesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/networkmanager.html#NetworkManager.Paginator.GetNetworkResources)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators.html#getnetworkresourcespaginator)
    """

    def paginate(
        self,
        *,
        GlobalNetworkId: str,
        RegisteredGatewayArn: str = ...,
        AwsRegion: str = ...,
        AccountId: str = ...,
        ResourceType: str = ...,
        ResourceArn: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetNetworkResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/networkmanager.html#NetworkManager.Paginator.GetNetworkResources.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators.html#getnetworkresourcespaginator)
        """


class GetNetworkTelemetryPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/networkmanager.html#NetworkManager.Paginator.GetNetworkTelemetry)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators.html#getnetworktelemetrypaginator)
    """

    def paginate(
        self,
        *,
        GlobalNetworkId: str,
        RegisteredGatewayArn: str = ...,
        AwsRegion: str = ...,
        AccountId: str = ...,
        ResourceType: str = ...,
        ResourceArn: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetNetworkTelemetryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/networkmanager.html#NetworkManager.Paginator.GetNetworkTelemetry.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators.html#getnetworktelemetrypaginator)
        """


class GetSitesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/networkmanager.html#NetworkManager.Paginator.GetSites)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators.html#getsitespaginator)
    """

    def paginate(
        self,
        *,
        GlobalNetworkId: str,
        SiteIds: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetSitesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/networkmanager.html#NetworkManager.Paginator.GetSites.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators.html#getsitespaginator)
        """


class GetTransitGatewayConnectPeerAssociationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/networkmanager.html#NetworkManager.Paginator.GetTransitGatewayConnectPeerAssociations)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators.html#gettransitgatewayconnectpeerassociationspaginator)
    """

    def paginate(
        self,
        *,
        GlobalNetworkId: str,
        TransitGatewayConnectPeerArns: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetTransitGatewayConnectPeerAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/networkmanager.html#NetworkManager.Paginator.GetTransitGatewayConnectPeerAssociations.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators.html#gettransitgatewayconnectpeerassociationspaginator)
        """


class GetTransitGatewayRegistrationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/networkmanager.html#NetworkManager.Paginator.GetTransitGatewayRegistrations)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators.html#gettransitgatewayregistrationspaginator)
    """

    def paginate(
        self,
        *,
        GlobalNetworkId: str,
        TransitGatewayArns: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetTransitGatewayRegistrationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/networkmanager.html#NetworkManager.Paginator.GetTransitGatewayRegistrations.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_networkmanager/paginators.html#gettransitgatewayregistrationspaginator)
        """
