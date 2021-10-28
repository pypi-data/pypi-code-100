# coding: utf-8

# flake8: noqa
"""
    Data Repository API

    This document defines the REST API for Data Repository. **Status: design in progress** There are four top-level endpoints (besides some used by swagger):  * /swagger-ui.html - generated by swagger: swagger API page that provides this documentation and a live UI for      submitting REST requests  * /status - provides the operational status of the service  * /api    - is the authenticated and authorized Data Repository API  * /ga4gh/drs/v1 - is a transcription of the Data Repository Service API  The overall API (/api) currently supports two interfaces:  * Repository - a general and default interface for initial setup, managing ingest and repository metadata  * Resource - an interface for managing billing accounts and resources  The API endpoints are organized by interface. Each interface is separately versioned. ## Notes on Naming All of the reference items are suffixed with \"Model\". Those names are used as the class names in the generated Java code. It is helpful to distinguish these model classes from other related classes, like the DAO classes and the operation classes. ## Editing and debugging I have found it best to edit this file directly to make changes and then use the swagger-editor to validate. The errors out of swagger-codegen are not that helpful. In the swagger-editor, it gives you nice errors and links to the place in the YAML where the errors are. But... the swagger-editor has been a bit of a pain for me to run. I tried the online website and was not able to load my YAML. Instead, I run it locally in a docker container, like this: ``` docker pull swaggerapi/swagger-editor docker run -p 9090:8080 swaggerapi/swagger-editor ``` Then navigate to localhost:9090 in your browser. I have not been able to get the file upload to work. It is a bit of a PITA, but I copy-paste the source code, replacing what is in the editor. Then make any fixes. Then copy-paste the resulting, valid file back into our source code. Not elegant, but easier than playing detective with the swagger-codegen errors. This might be something about my browser or environment, so give it a try yourself and see how it goes. ## Merging the DRS standard swagger into this swagger ## The merging is done in three sections:  1. Merging the security definitions into our security definitions  2. This section of paths. We make all paths explicit (prefixed with /ga4gh/drs/v1)     All standard DRS definitions and parameters are prefixed with 'DRS' to separate them     from our native definitions and parameters. We remove the x-swagger-router-controller lines.  3. A separate part of the definitions section for the DRS definitions  NOTE: the code here does not relect the DRS spec anymore. See DR-409.   # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

# import models into model package
from data_repo_client.models.access_info_big_query_model import AccessInfoBigQueryModel
from data_repo_client.models.access_info_big_query_model_table import AccessInfoBigQueryModelTable
from data_repo_client.models.access_info_model import AccessInfoModel
from data_repo_client.models.access_info_parquet_model import AccessInfoParquetModel
from data_repo_client.models.access_info_parquet_model_table import AccessInfoParquetModelTable
from data_repo_client.models.asset_model import AssetModel
from data_repo_client.models.asset_table_model import AssetTableModel
from data_repo_client.models.billing_profile_model import BillingProfileModel
from data_repo_client.models.billing_profile_request_model import BillingProfileRequestModel
from data_repo_client.models.billing_profile_update_model import BillingProfileUpdateModel
from data_repo_client.models.bulk_load_array_request_model import BulkLoadArrayRequestModel
from data_repo_client.models.bulk_load_array_result_model import BulkLoadArrayResultModel
from data_repo_client.models.bulk_load_file_model import BulkLoadFileModel
from data_repo_client.models.bulk_load_file_result_model import BulkLoadFileResultModel
from data_repo_client.models.bulk_load_file_state import BulkLoadFileState
from data_repo_client.models.bulk_load_history_model import BulkLoadHistoryModel
from data_repo_client.models.bulk_load_history_model_list import BulkLoadHistoryModelList
from data_repo_client.models.bulk_load_request_model import BulkLoadRequestModel
from data_repo_client.models.bulk_load_result_model import BulkLoadResultModel
from data_repo_client.models.cloud_platform import CloudPlatform
from data_repo_client.models.column_model import ColumnModel
from data_repo_client.models.config_enable_model import ConfigEnableModel
from data_repo_client.models.config_fault_counted_model import ConfigFaultCountedModel
from data_repo_client.models.config_fault_model import ConfigFaultModel
from data_repo_client.models.config_group_model import ConfigGroupModel
from data_repo_client.models.config_list_model import ConfigListModel
from data_repo_client.models.config_model import ConfigModel
from data_repo_client.models.config_parameter_model import ConfigParameterModel
from data_repo_client.models.drs_access_method import DRSAccessMethod
from data_repo_client.models.drs_access_url import DRSAccessURL
from data_repo_client.models.drs_checksum import DRSChecksum
from data_repo_client.models.drs_contents_object import DRSContentsObject
from data_repo_client.models.drs_error import DRSError
from data_repo_client.models.drs_object import DRSObject
from data_repo_client.models.drs_service_info import DRSServiceInfo
from data_repo_client.models.data_deletion_gcs_file_model import DataDeletionGcsFileModel
from data_repo_client.models.data_deletion_request import DataDeletionRequest
from data_repo_client.models.data_deletion_table_model import DataDeletionTableModel
from data_repo_client.models.dataset_model import DatasetModel
from data_repo_client.models.dataset_request_access_include_model import DatasetRequestAccessIncludeModel
from data_repo_client.models.dataset_request_model import DatasetRequestModel
from data_repo_client.models.dataset_specification_model import DatasetSpecificationModel
from data_repo_client.models.dataset_summary_model import DatasetSummaryModel
from data_repo_client.models.date_partition_options_model import DatePartitionOptionsModel
from data_repo_client.models.delete_response_model import DeleteResponseModel
from data_repo_client.models.directory_detail_model import DirectoryDetailModel
from data_repo_client.models.enumerate_billing_profile_model import EnumerateBillingProfileModel
from data_repo_client.models.enumerate_dataset_model import EnumerateDatasetModel
from data_repo_client.models.enumerate_snapshot_model import EnumerateSnapshotModel
from data_repo_client.models.enumerate_sort_by_param import EnumerateSortByParam
from data_repo_client.models.error_model import ErrorModel
from data_repo_client.models.file_detail_model import FileDetailModel
from data_repo_client.models.file_load_model import FileLoadModel
from data_repo_client.models.file_model import FileModel
from data_repo_client.models.file_model_type import FileModelType
from data_repo_client.models.ingest_request_model import IngestRequestModel
from data_repo_client.models.ingest_response_model import IngestResponseModel
from data_repo_client.models.int_partition_options_model import IntPartitionOptionsModel
from data_repo_client.models.job_model import JobModel
from data_repo_client.models.policy_member_request import PolicyMemberRequest
from data_repo_client.models.policy_model import PolicyModel
from data_repo_client.models.policy_response import PolicyResponse
from data_repo_client.models.relationship_model import RelationshipModel
from data_repo_client.models.relationship_term_model import RelationshipTermModel
from data_repo_client.models.repository_configuration_model import RepositoryConfigurationModel
from data_repo_client.models.repository_status_model import RepositoryStatusModel
from data_repo_client.models.repository_status_model_systems import RepositoryStatusModelSystems
from data_repo_client.models.search_index_model import SearchIndexModel
from data_repo_client.models.search_index_request import SearchIndexRequest
from data_repo_client.models.search_metadata_model import SearchMetadataModel
from data_repo_client.models.search_query_request import SearchQueryRequest
from data_repo_client.models.search_query_result_model import SearchQueryResultModel
from data_repo_client.models.snapshot_model import SnapshotModel
from data_repo_client.models.snapshot_request_access_include_model import SnapshotRequestAccessIncludeModel
from data_repo_client.models.snapshot_request_asset_model import SnapshotRequestAssetModel
from data_repo_client.models.snapshot_request_contents_model import SnapshotRequestContentsModel
from data_repo_client.models.snapshot_request_model import SnapshotRequestModel
from data_repo_client.models.snapshot_request_query_model import SnapshotRequestQueryModel
from data_repo_client.models.snapshot_request_row_id_model import SnapshotRequestRowIdModel
from data_repo_client.models.snapshot_request_row_id_table_model import SnapshotRequestRowIdTableModel
from data_repo_client.models.snapshot_source_model import SnapshotSourceModel
from data_repo_client.models.snapshot_summary_model import SnapshotSummaryModel
from data_repo_client.models.sql_sort_direction import SqlSortDirection
from data_repo_client.models.storage_resource_model import StorageResourceModel
from data_repo_client.models.table_data_type import TableDataType
from data_repo_client.models.table_model import TableModel
from data_repo_client.models.upgrade_model import UpgradeModel
from data_repo_client.models.upgrade_response_model import UpgradeResponseModel
from data_repo_client.models.user_status_info import UserStatusInfo
