"""
Type annotations for fsx service client.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html)

Usage::

    ```python
    import boto3
    from mypy_boto3_fsx import FSxClient

    client: FSxClient = boto3.client("fsx")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    FileSystemTypeType,
    StorageTypeType,
    StorageVirtualMachineRootVolumeSecurityStyleType,
)
from .paginator import (
    DescribeBackupsPaginator,
    DescribeFileSystemsPaginator,
    ListTagsForResourcePaginator,
)
from .type_defs import (
    AssociateFileSystemAliasesResponseTypeDef,
    CancelDataRepositoryTaskResponseTypeDef,
    CompletionReportTypeDef,
    CopyBackupResponseTypeDef,
    CreateBackupResponseTypeDef,
    CreateDataRepositoryTaskResponseTypeDef,
    CreateFileSystemFromBackupResponseTypeDef,
    CreateFileSystemLustreConfigurationTypeDef,
    CreateFileSystemOntapConfigurationTypeDef,
    CreateFileSystemResponseTypeDef,
    CreateFileSystemWindowsConfigurationTypeDef,
    CreateOntapVolumeConfigurationTypeDef,
    CreateStorageVirtualMachineResponseTypeDef,
    CreateSvmActiveDirectoryConfigurationTypeDef,
    CreateVolumeFromBackupResponseTypeDef,
    CreateVolumeResponseTypeDef,
    DataRepositoryTaskFilterTypeDef,
    DeleteBackupResponseTypeDef,
    DeleteFileSystemLustreConfigurationTypeDef,
    DeleteFileSystemResponseTypeDef,
    DeleteFileSystemWindowsConfigurationTypeDef,
    DeleteStorageVirtualMachineResponseTypeDef,
    DeleteVolumeOntapConfigurationTypeDef,
    DeleteVolumeResponseTypeDef,
    DescribeBackupsResponseTypeDef,
    DescribeDataRepositoryTasksResponseTypeDef,
    DescribeFileSystemAliasesResponseTypeDef,
    DescribeFileSystemsResponseTypeDef,
    DescribeStorageVirtualMachinesResponseTypeDef,
    DescribeVolumesResponseTypeDef,
    DisassociateFileSystemAliasesResponseTypeDef,
    FilterTypeDef,
    ListTagsForResourceResponseTypeDef,
    StorageVirtualMachineFilterTypeDef,
    TagTypeDef,
    UpdateFileSystemLustreConfigurationTypeDef,
    UpdateFileSystemOntapConfigurationTypeDef,
    UpdateFileSystemResponseTypeDef,
    UpdateFileSystemWindowsConfigurationTypeDef,
    UpdateOntapVolumeConfigurationTypeDef,
    UpdateStorageVirtualMachineResponseTypeDef,
    UpdateSvmActiveDirectoryConfigurationTypeDef,
    UpdateVolumeResponseTypeDef,
    VolumeFilterTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("FSxClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ActiveDirectoryError: Type[BotocoreClientError]
    BackupBeingCopied: Type[BotocoreClientError]
    BackupInProgress: Type[BotocoreClientError]
    BackupNotFound: Type[BotocoreClientError]
    BackupRestoring: Type[BotocoreClientError]
    BadRequest: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DataRepositoryTaskEnded: Type[BotocoreClientError]
    DataRepositoryTaskExecuting: Type[BotocoreClientError]
    DataRepositoryTaskNotFound: Type[BotocoreClientError]
    FileSystemNotFound: Type[BotocoreClientError]
    IncompatibleParameterError: Type[BotocoreClientError]
    IncompatibleRegionForMultiAZ: Type[BotocoreClientError]
    InternalServerError: Type[BotocoreClientError]
    InvalidDestinationKmsKey: Type[BotocoreClientError]
    InvalidExportPath: Type[BotocoreClientError]
    InvalidImportPath: Type[BotocoreClientError]
    InvalidNetworkSettings: Type[BotocoreClientError]
    InvalidPerUnitStorageThroughput: Type[BotocoreClientError]
    InvalidRegion: Type[BotocoreClientError]
    InvalidSourceKmsKey: Type[BotocoreClientError]
    MissingFileSystemConfiguration: Type[BotocoreClientError]
    MissingVolumeConfiguration: Type[BotocoreClientError]
    NotServiceResourceError: Type[BotocoreClientError]
    ResourceDoesNotSupportTagging: Type[BotocoreClientError]
    ResourceNotFound: Type[BotocoreClientError]
    ServiceLimitExceeded: Type[BotocoreClientError]
    SourceBackupUnavailable: Type[BotocoreClientError]
    StorageVirtualMachineNotFound: Type[BotocoreClientError]
    UnsupportedOperation: Type[BotocoreClientError]
    VolumeNotFound: Type[BotocoreClientError]


class FSxClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        FSxClient exceptions.
        """

    def associate_file_system_aliases(
        self, *, FileSystemId: str, Aliases: Sequence[str], ClientRequestToken: str = ...
    ) -> AssociateFileSystemAliasesResponseTypeDef:
        """
        Use this action to associate one or more Domain Name Server (DNS) aliases with
        an existing Amazon FSx for Windows File Server file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.associate_file_system_aliases)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#associate_file_system_aliases)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.can_paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#can_paginate)
        """

    def cancel_data_repository_task(
        self, *, TaskId: str
    ) -> CancelDataRepositoryTaskResponseTypeDef:
        """
        Cancels an existing Amazon FSx for Lustre data repository task if that task is
        in either the `PENDING` or `EXECUTING` state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.cancel_data_repository_task)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#cancel_data_repository_task)
        """

    def copy_backup(
        self,
        *,
        SourceBackupId: str,
        ClientRequestToken: str = ...,
        SourceRegion: str = ...,
        KmsKeyId: str = ...,
        CopyTags: bool = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CopyBackupResponseTypeDef:
        """
        Copies an existing backup within the same Amazon Web Services account to another
        Amazon Web Services Region (cross-Region copy) or within the same Amazon Web
        Services Region (in-Region copy).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.copy_backup)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#copy_backup)
        """

    def create_backup(
        self,
        *,
        FileSystemId: str = ...,
        ClientRequestToken: str = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        VolumeId: str = ...
    ) -> CreateBackupResponseTypeDef:
        """
        Creates a backup of an existing Amazon FSx for Windows File Server or Amazon FSx
        for Lustre file system, or of an Amazon FSx for NetApp ONTAP volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.create_backup)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#create_backup)
        """

    def create_data_repository_task(
        self,
        *,
        Type: Literal["EXPORT_TO_REPOSITORY"],
        FileSystemId: str,
        Report: "CompletionReportTypeDef",
        Paths: Sequence[str] = ...,
        ClientRequestToken: str = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateDataRepositoryTaskResponseTypeDef:
        """
        Creates an Amazon FSx for Lustre data repository task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.create_data_repository_task)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#create_data_repository_task)
        """

    def create_file_system(
        self,
        *,
        FileSystemType: FileSystemTypeType,
        StorageCapacity: int,
        SubnetIds: Sequence[str],
        ClientRequestToken: str = ...,
        StorageType: StorageTypeType = ...,
        SecurityGroupIds: Sequence[str] = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        KmsKeyId: str = ...,
        WindowsConfiguration: "CreateFileSystemWindowsConfigurationTypeDef" = ...,
        LustreConfiguration: "CreateFileSystemLustreConfigurationTypeDef" = ...,
        OntapConfiguration: "CreateFileSystemOntapConfigurationTypeDef" = ...,
        FileSystemTypeVersion: str = ...
    ) -> CreateFileSystemResponseTypeDef:
        """
        Creates a new, empty Amazon FSx file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.create_file_system)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#create_file_system)
        """

    def create_file_system_from_backup(
        self,
        *,
        BackupId: str,
        SubnetIds: Sequence[str],
        ClientRequestToken: str = ...,
        SecurityGroupIds: Sequence[str] = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        WindowsConfiguration: "CreateFileSystemWindowsConfigurationTypeDef" = ...,
        LustreConfiguration: "CreateFileSystemLustreConfigurationTypeDef" = ...,
        StorageType: StorageTypeType = ...,
        KmsKeyId: str = ...,
        FileSystemTypeVersion: str = ...
    ) -> CreateFileSystemFromBackupResponseTypeDef:
        """
        Creates a new Amazon FSx for Lustre or Amazon FSx for Windows File Server file
        system from an existing Amazon FSx backup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.create_file_system_from_backup)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#create_file_system_from_backup)
        """

    def create_storage_virtual_machine(
        self,
        *,
        FileSystemId: str,
        Name: str,
        ActiveDirectoryConfiguration: "CreateSvmActiveDirectoryConfigurationTypeDef" = ...,
        ClientRequestToken: str = ...,
        SvmAdminPassword: str = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        RootVolumeSecurityStyle: StorageVirtualMachineRootVolumeSecurityStyleType = ...
    ) -> CreateStorageVirtualMachineResponseTypeDef:
        """
        Creates a storage virtual machine (SVM) for an Amazon FSx for ONTAP file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.create_storage_virtual_machine)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#create_storage_virtual_machine)
        """

    def create_volume(
        self,
        *,
        VolumeType: Literal["ONTAP"],
        Name: str,
        ClientRequestToken: str = ...,
        OntapConfiguration: "CreateOntapVolumeConfigurationTypeDef" = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateVolumeResponseTypeDef:
        """
        Creates an Amazon FSx for NetApp ONTAP storage volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.create_volume)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#create_volume)
        """

    def create_volume_from_backup(
        self,
        *,
        BackupId: str,
        Name: str,
        ClientRequestToken: str = ...,
        OntapConfiguration: "CreateOntapVolumeConfigurationTypeDef" = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateVolumeFromBackupResponseTypeDef:
        """
        Creates a new Amazon FSx for NetApp ONTAP volume from an existing Amazon FSx
        volume backup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.create_volume_from_backup)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#create_volume_from_backup)
        """

    def delete_backup(
        self, *, BackupId: str, ClientRequestToken: str = ...
    ) -> DeleteBackupResponseTypeDef:
        """
        Deletes an Amazon FSx backup, deleting its contents.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.delete_backup)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#delete_backup)
        """

    def delete_file_system(
        self,
        *,
        FileSystemId: str,
        ClientRequestToken: str = ...,
        WindowsConfiguration: "DeleteFileSystemWindowsConfigurationTypeDef" = ...,
        LustreConfiguration: "DeleteFileSystemLustreConfigurationTypeDef" = ...
    ) -> DeleteFileSystemResponseTypeDef:
        """
        Deletes a file system, deleting its contents.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.delete_file_system)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#delete_file_system)
        """

    def delete_storage_virtual_machine(
        self, *, StorageVirtualMachineId: str, ClientRequestToken: str = ...
    ) -> DeleteStorageVirtualMachineResponseTypeDef:
        """
        Deletes an existing Amazon FSx for ONTAP storage virtual machine (SVM).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.delete_storage_virtual_machine)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#delete_storage_virtual_machine)
        """

    def delete_volume(
        self,
        *,
        VolumeId: str,
        ClientRequestToken: str = ...,
        OntapConfiguration: "DeleteVolumeOntapConfigurationTypeDef" = ...
    ) -> DeleteVolumeResponseTypeDef:
        """
        Deletes an Amazon FSx for NetApp ONTAP volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.delete_volume)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#delete_volume)
        """

    def describe_backups(
        self,
        *,
        BackupIds: Sequence[str] = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> DescribeBackupsResponseTypeDef:
        """
        Returns the description of specific Amazon FSx backups, if a `BackupIds` value
        is provided for that backup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.describe_backups)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#describe_backups)
        """

    def describe_data_repository_tasks(
        self,
        *,
        TaskIds: Sequence[str] = ...,
        Filters: Sequence["DataRepositoryTaskFilterTypeDef"] = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> DescribeDataRepositoryTasksResponseTypeDef:
        """
        Returns the description of specific Amazon FSx for Lustre data repository tasks,
        if one or more `TaskIds` values are provided in the request, or if filters are
        used in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.describe_data_repository_tasks)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#describe_data_repository_tasks)
        """

    def describe_file_system_aliases(
        self,
        *,
        FileSystemId: str,
        ClientRequestToken: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> DescribeFileSystemAliasesResponseTypeDef:
        """
        Returns the DNS aliases that are associated with the specified Amazon FSx for
        Windows File Server file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.describe_file_system_aliases)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#describe_file_system_aliases)
        """

    def describe_file_systems(
        self, *, FileSystemIds: Sequence[str] = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeFileSystemsResponseTypeDef:
        """
        Returns the description of specific Amazon FSx file systems, if a
        `FileSystemIds` value is provided for that file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.describe_file_systems)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#describe_file_systems)
        """

    def describe_storage_virtual_machines(
        self,
        *,
        StorageVirtualMachineIds: Sequence[str] = ...,
        Filters: Sequence["StorageVirtualMachineFilterTypeDef"] = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> DescribeStorageVirtualMachinesResponseTypeDef:
        """
        Describes one or more Amazon FSx for NetApp ONTAP storage virtual machines
        (SVMs).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.describe_storage_virtual_machines)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#describe_storage_virtual_machines)
        """

    def describe_volumes(
        self,
        *,
        VolumeIds: Sequence[str] = ...,
        Filters: Sequence["VolumeFilterTypeDef"] = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> DescribeVolumesResponseTypeDef:
        """
        Describes one or more Amazon FSx for NetApp ONTAP volumes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.describe_volumes)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#describe_volumes)
        """

    def disassociate_file_system_aliases(
        self, *, FileSystemId: str, Aliases: Sequence[str], ClientRequestToken: str = ...
    ) -> DisassociateFileSystemAliasesResponseTypeDef:
        """
        Use this action to disassociate, or remove, one or more Domain Name Service
        (DNS) aliases from an Amazon FSx for Windows File Server file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.disassociate_file_system_aliases)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#disassociate_file_system_aliases)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#generate_presigned_url)
        """

    def list_tags_for_resource(
        self, *, ResourceARN: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists tags for an Amazon FSx file systems and backups in the case of Amazon FSx
        for Windows File Server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#list_tags_for_resource)
        """

    def tag_resource(self, *, ResourceARN: str, Tags: Sequence["TagTypeDef"]) -> Dict[str, Any]:
        """
        Tags an Amazon FSx resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.tag_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#tag_resource)
        """

    def untag_resource(self, *, ResourceARN: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        This action removes a tag from an Amazon FSx resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.untag_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#untag_resource)
        """

    def update_file_system(
        self,
        *,
        FileSystemId: str,
        ClientRequestToken: str = ...,
        StorageCapacity: int = ...,
        WindowsConfiguration: "UpdateFileSystemWindowsConfigurationTypeDef" = ...,
        LustreConfiguration: "UpdateFileSystemLustreConfigurationTypeDef" = ...,
        OntapConfiguration: "UpdateFileSystemOntapConfigurationTypeDef" = ...
    ) -> UpdateFileSystemResponseTypeDef:
        """
        Use this operation to update the configuration of an existing Amazon FSx file
        system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.update_file_system)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#update_file_system)
        """

    def update_storage_virtual_machine(
        self,
        *,
        StorageVirtualMachineId: str,
        ActiveDirectoryConfiguration: "UpdateSvmActiveDirectoryConfigurationTypeDef" = ...,
        ClientRequestToken: str = ...,
        SvmAdminPassword: str = ...
    ) -> UpdateStorageVirtualMachineResponseTypeDef:
        """
        Updates an Amazon FSx for ONTAP storage virtual machine (SVM).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.update_storage_virtual_machine)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#update_storage_virtual_machine)
        """

    def update_volume(
        self,
        *,
        VolumeId: str,
        ClientRequestToken: str = ...,
        OntapConfiguration: "UpdateOntapVolumeConfigurationTypeDef" = ...
    ) -> UpdateVolumeResponseTypeDef:
        """
        Updates an Amazon FSx for NetApp ONTAP volume's configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Client.update_volume)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/client.html#update_volume)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_backups"]
    ) -> DescribeBackupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Paginator.DescribeBackups)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators.html#describebackupspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_file_systems"]
    ) -> DescribeFileSystemsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Paginator.DescribeFileSystems)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators.html#describefilesystemspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.11/reference/services/fsx.html#FSx.Paginator.ListTagsForResource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators.html#listtagsforresourcepaginator)
        """
