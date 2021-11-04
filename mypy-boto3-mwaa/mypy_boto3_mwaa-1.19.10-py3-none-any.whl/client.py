"""
Type annotations for mwaa service client.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_mwaa/client.html)

Usage::

    ```python
    import boto3
    from mypy_boto3_mwaa import MWAAClient

    client: MWAAClient = boto3.client("mwaa")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

from .literals import WebserverAccessModeType
from .paginator import ListEnvironmentsPaginator
from .type_defs import (
    CreateCliTokenResponseTypeDef,
    CreateEnvironmentOutputTypeDef,
    CreateWebLoginTokenResponseTypeDef,
    GetEnvironmentOutputTypeDef,
    ListEnvironmentsOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    LoggingConfigurationInputTypeDef,
    MetricDatumTypeDef,
    NetworkConfigurationTypeDef,
    UpdateEnvironmentOutputTypeDef,
    UpdateNetworkConfigurationInputTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("MWAAClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class MWAAClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/mwaa.html#MWAA.Client)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_mwaa/client.html)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MWAAClient exceptions.
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/mwaa.html#MWAA.Client.can_paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_mwaa/client.html#can_paginate)
        """

    def create_cli_token(self, *, Name: str) -> CreateCliTokenResponseTypeDef:
        """
        Create a CLI token to use Airflow CLI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/mwaa.html#MWAA.Client.create_cli_token)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_mwaa/client.html#create_cli_token)
        """

    def create_environment(
        self,
        *,
        DagS3Path: str,
        ExecutionRoleArn: str,
        Name: str,
        NetworkConfiguration: "NetworkConfigurationTypeDef",
        SourceBucketArn: str,
        AirflowConfigurationOptions: Mapping[str, str] = ...,
        AirflowVersion: str = ...,
        EnvironmentClass: str = ...,
        KmsKey: str = ...,
        LoggingConfiguration: "LoggingConfigurationInputTypeDef" = ...,
        MaxWorkers: int = ...,
        MinWorkers: int = ...,
        PluginsS3ObjectVersion: str = ...,
        PluginsS3Path: str = ...,
        RequirementsS3ObjectVersion: str = ...,
        RequirementsS3Path: str = ...,
        Schedulers: int = ...,
        Tags: Mapping[str, str] = ...,
        WebserverAccessMode: WebserverAccessModeType = ...,
        WeeklyMaintenanceWindowStart: str = ...
    ) -> CreateEnvironmentOutputTypeDef:
        """
        Creates an Amazon Managed Workflows for Apache Airflow (MWAA) environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/mwaa.html#MWAA.Client.create_environment)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_mwaa/client.html#create_environment)
        """

    def create_web_login_token(self, *, Name: str) -> CreateWebLoginTokenResponseTypeDef:
        """
        Create a JWT token to be used to login to Airflow Web UI with claims based
        Authentication.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/mwaa.html#MWAA.Client.create_web_login_token)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_mwaa/client.html#create_web_login_token)
        """

    def delete_environment(self, *, Name: str) -> Dict[str, Any]:
        """
        Deletes an Amazon Managed Workflows for Apache Airflow (MWAA) environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/mwaa.html#MWAA.Client.delete_environment)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_mwaa/client.html#delete_environment)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/mwaa.html#MWAA.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_mwaa/client.html#generate_presigned_url)
        """

    def get_environment(self, *, Name: str) -> GetEnvironmentOutputTypeDef:
        """
        Retrieves the details of an Amazon Managed Workflows for Apache Airflow (MWAA)
        environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/mwaa.html#MWAA.Client.get_environment)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_mwaa/client.html#get_environment)
        """

    def list_environments(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListEnvironmentsOutputTypeDef:
        """
        Lists the Amazon Managed Workflows for Apache Airflow (MWAA) environments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/mwaa.html#MWAA.Client.list_environments)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_mwaa/client.html#list_environments)
        """

    def list_tags_for_resource(self, *, ResourceArn: str) -> ListTagsForResourceOutputTypeDef:
        """
        Lists the key-value tag pairs associated to the Amazon Managed Workflows for
        Apache Airflow (MWAA) environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/mwaa.html#MWAA.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_mwaa/client.html#list_tags_for_resource)
        """

    def publish_metrics(
        self, *, EnvironmentName: str, MetricData: Sequence["MetricDatumTypeDef"]
    ) -> Dict[str, Any]:
        """
        An operation for publishing metrics from the customers to the Ops plane.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/mwaa.html#MWAA.Client.publish_metrics)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_mwaa/client.html#publish_metrics)
        """

    def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Associates key-value tag pairs to your Amazon Managed Workflows for Apache
        Airflow (MWAA) environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/mwaa.html#MWAA.Client.tag_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_mwaa/client.html#tag_resource)
        """

    def untag_resource(self, *, ResourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes key-value tag pairs associated to your Amazon Managed Workflows for
        Apache Airflow (MWAA) environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/mwaa.html#MWAA.Client.untag_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_mwaa/client.html#untag_resource)
        """

    def update_environment(
        self,
        *,
        Name: str,
        AirflowConfigurationOptions: Mapping[str, str] = ...,
        AirflowVersion: str = ...,
        DagS3Path: str = ...,
        EnvironmentClass: str = ...,
        ExecutionRoleArn: str = ...,
        LoggingConfiguration: "LoggingConfigurationInputTypeDef" = ...,
        MaxWorkers: int = ...,
        MinWorkers: int = ...,
        NetworkConfiguration: "UpdateNetworkConfigurationInputTypeDef" = ...,
        PluginsS3ObjectVersion: str = ...,
        PluginsS3Path: str = ...,
        RequirementsS3ObjectVersion: str = ...,
        RequirementsS3Path: str = ...,
        Schedulers: int = ...,
        SourceBucketArn: str = ...,
        WebserverAccessMode: WebserverAccessModeType = ...,
        WeeklyMaintenanceWindowStart: str = ...
    ) -> UpdateEnvironmentOutputTypeDef:
        """
        Updates an Amazon Managed Workflows for Apache Airflow (MWAA) environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/mwaa.html#MWAA.Client.update_environment)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_mwaa/client.html#update_environment)
        """

    def get_paginator(
        self, operation_name: Literal["list_environments"]
    ) -> ListEnvironmentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.10/reference/services/mwaa.html#MWAA.Paginator.ListEnvironments)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_mwaa/paginators.html#listenvironmentspaginator)
        """
