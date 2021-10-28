# coding: utf-8

"""
    Data Repository API

    This document defines the REST API for Data Repository. **Status: design in progress** There are four top-level endpoints (besides some used by swagger):  * /swagger-ui.html - generated by swagger: swagger API page that provides this documentation and a live UI for      submitting REST requests  * /status - provides the operational status of the service  * /api    - is the authenticated and authorized Data Repository API  * /ga4gh/drs/v1 - is a transcription of the Data Repository Service API  The overall API (/api) currently supports two interfaces:  * Repository - a general and default interface for initial setup, managing ingest and repository metadata  * Resource - an interface for managing billing accounts and resources  The API endpoints are organized by interface. Each interface is separately versioned. ## Notes on Naming All of the reference items are suffixed with \"Model\". Those names are used as the class names in the generated Java code. It is helpful to distinguish these model classes from other related classes, like the DAO classes and the operation classes. ## Editing and debugging I have found it best to edit this file directly to make changes and then use the swagger-editor to validate. The errors out of swagger-codegen are not that helpful. In the swagger-editor, it gives you nice errors and links to the place in the YAML where the errors are. But... the swagger-editor has been a bit of a pain for me to run. I tried the online website and was not able to load my YAML. Instead, I run it locally in a docker container, like this: ``` docker pull swaggerapi/swagger-editor docker run -p 9090:8080 swaggerapi/swagger-editor ``` Then navigate to localhost:9090 in your browser. I have not been able to get the file upload to work. It is a bit of a PITA, but I copy-paste the source code, replacing what is in the editor. Then make any fixes. Then copy-paste the resulting, valid file back into our source code. Not elegant, but easier than playing detective with the swagger-codegen errors. This might be something about my browser or environment, so give it a try yourself and see how it goes. ## Merging the DRS standard swagger into this swagger ## The merging is done in three sections:  1. Merging the security definitions into our security definitions  2. This section of paths. We make all paths explicit (prefixed with /ga4gh/drs/v1)     All standard DRS definitions and parameters are prefixed with 'DRS' to separate them     from our native definitions and parameters. We remove the x-swagger-router-controller lines.  3. A separate part of the definitions section for the DRS definitions  NOTE: the code here does not relect the DRS spec anymore. See DR-409.   # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import data_repo_client
from data_repo_client.models.dataset_model import DatasetModel  # noqa: E501
from data_repo_client.rest import ApiException

class TestDatasetModel(unittest.TestCase):
    """DatasetModel unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test DatasetModel
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = data_repo_client.models.dataset_model.DatasetModel()  # noqa: E501
        if include_optional :
            return DatasetModel(
                id = '0', 
                name = 'a', 
                description = '0', 
                default_profile_id = '0', 
                data_project = '0', 
                default_snapshot_id = '0', 
                schema = data_repo_client.models.dataset_specification_model.DatasetSpecificationModel(
                    tables = [
                        data_repo_client.models.table_model.TableModel(
                            name = 'a', 
                            columns = [
                                data_repo_client.models.column_model.ColumnModel(
                                    name = 'a', 
                                    datatype = 'boolean', 
                                    array_of = True, )
                                ], 
                            primary_key = [
                                'a'
                                ], 
                            partition_mode = 'none', 
                            date_partition_options = data_repo_client.models.date_partition_options_model.DatePartitionOptionsModel(
                                column = 'a', ), 
                            int_partition_options = data_repo_client.models.int_partition_options_model.IntPartitionOptionsModel(
                                column = 'a', 
                                min = 56, 
                                max = 56, 
                                interval = 56, ), 
                            row_count = 56, )
                        ], 
                    relationships = [
                        data_repo_client.models.relationship_model.RelationshipModel(
                            name = '0', 
                            from = data_repo_client.models.relationship_term_model.RelationshipTermModel(
                                table = 'a', 
                                column = 'a', ), 
                            to = data_repo_client.models.relationship_term_model.RelationshipTermModel(
                                table = 'a', 
                                column = 'a', ), )
                        ], 
                    assets = [
                        data_repo_client.models.asset_model.AssetModel(
                            name = '0', 
                            tables = [
                                data_repo_client.models.asset_table_model.AssetTableModel(
                                    name = 'a', 
                                    columns = [
                                        'a'
                                        ], )
                                ], 
                            root_table = 'a', 
                            root_column = 'a', 
                            follow = [
                                'a'
                                ], )
                        ], ), 
                created_date = '0', 
                storage = [
                    data_repo_client.models.storage_resource_model.StorageResourceModel(
                        region = '0', 
                        cloud_resource = '0', 
                        cloud_platform = 'gcp', )
                    ], 
                access_information = data_repo_client.models.access_info_model.AccessInfoModel(
                    big_query = data_repo_client.models.access_info_big_query_model.AccessInfoBigQueryModel(
                        dataset_name = '0', 
                        dataset_id = '0', 
                        project_id = '0', 
                        link = '0', 
                        tables = [
                            data_repo_client.models.access_info_big_query_model_table.AccessInfoBigQueryModelTable(
                                name = '0', 
                                id = '0', 
                                qualified_name = '0', 
                                link = '0', 
                                sample_query = '0', )
                            ], ), 
                    parquet = data_repo_client.models.access_info_parquet_model.AccessInfoParquetModel(
                        dataset_name = '0', 
                        dataset_id = '0', 
                        storage_account_id = '0', 
                        signed_url = '0', 
                        tables = [
                            data_repo_client.models.access_info_parquet_model_table.AccessInfoParquetModelTable(
                                name = '0', 
                                id = '0', 
                                signed_url = '0', 
                                sample_query = '0', )
                            ], ), )
            )
        else :
            return DatasetModel(
        )

    def testDatasetModel(self):
        """Test DatasetModel"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
