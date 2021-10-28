# coding: utf-8

"""
    Data Repository API

    This document defines the REST API for Data Repository. **Status: design in progress** There are four top-level endpoints (besides some used by swagger):  * /swagger-ui.html - generated by swagger: swagger API page that provides this documentation and a live UI for      submitting REST requests  * /status - provides the operational status of the service  * /api    - is the authenticated and authorized Data Repository API  * /ga4gh/drs/v1 - is a transcription of the Data Repository Service API  The overall API (/api) currently supports two interfaces:  * Repository - a general and default interface for initial setup, managing ingest and repository metadata  * Resource - an interface for managing billing accounts and resources  The API endpoints are organized by interface. Each interface is separately versioned. ## Notes on Naming All of the reference items are suffixed with \"Model\". Those names are used as the class names in the generated Java code. It is helpful to distinguish these model classes from other related classes, like the DAO classes and the operation classes. ## Editing and debugging I have found it best to edit this file directly to make changes and then use the swagger-editor to validate. The errors out of swagger-codegen are not that helpful. In the swagger-editor, it gives you nice errors and links to the place in the YAML where the errors are. But... the swagger-editor has been a bit of a pain for me to run. I tried the online website and was not able to load my YAML. Instead, I run it locally in a docker container, like this: ``` docker pull swaggerapi/swagger-editor docker run -p 9090:8080 swaggerapi/swagger-editor ``` Then navigate to localhost:9090 in your browser. I have not been able to get the file upload to work. It is a bit of a PITA, but I copy-paste the source code, replacing what is in the editor. Then make any fixes. Then copy-paste the resulting, valid file back into our source code. Not elegant, but easier than playing detective with the swagger-codegen errors. This might be something about my browser or environment, so give it a try yourself and see how it goes. ## Merging the DRS standard swagger into this swagger ## The merging is done in three sections:  1. Merging the security definitions into our security definitions  2. This section of paths. We make all paths explicit (prefixed with /ga4gh/drs/v1)     All standard DRS definitions and parameters are prefixed with 'DRS' to separate them     from our native definitions and parameters. We remove the x-swagger-router-controller lines.  3. A separate part of the definitions section for the DRS definitions  NOTE: the code here does not relect the DRS spec anymore. See DR-409.   # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from data_repo_client.configuration import Configuration


class AccessInfoParquetModel(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'dataset_name': 'str',
        'dataset_id': 'str',
        'storage_account_id': 'str',
        'signed_url': 'str',
        'tables': 'list[AccessInfoParquetModelTable]'
    }

    attribute_map = {
        'dataset_name': 'datasetName',
        'dataset_id': 'datasetId',
        'storage_account_id': 'storageAccountId',
        'signed_url': 'signedUrl',
        'tables': 'tables'
    }

    def __init__(self, dataset_name=None, dataset_id=None, storage_account_id=None, signed_url=None, tables=None, local_vars_configuration=None):  # noqa: E501
        """AccessInfoParquetModel - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._dataset_name = None
        self._dataset_id = None
        self._storage_account_id = None
        self._signed_url = None
        self._tables = None
        self.discriminator = None

        self.dataset_name = dataset_name
        self.dataset_id = dataset_id
        self.storage_account_id = storage_account_id
        self.signed_url = signed_url
        self.tables = tables

    @property
    def dataset_name(self):
        """Gets the dataset_name of this AccessInfoParquetModel.  # noqa: E501

        Name of the Azure dataset where snapshot or dataset tabular data lives   # noqa: E501

        :return: The dataset_name of this AccessInfoParquetModel.  # noqa: E501
        :rtype: str
        """
        return self._dataset_name

    @dataset_name.setter
    def dataset_name(self, dataset_name):
        """Sets the dataset_name of this AccessInfoParquetModel.

        Name of the Azure dataset where snapshot or dataset tabular data lives   # noqa: E501

        :param dataset_name: The dataset_name of this AccessInfoParquetModel.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and dataset_name is None:  # noqa: E501
            raise ValueError("Invalid value for `dataset_name`, must not be `None`")  # noqa: E501

        self._dataset_name = dataset_name

    @property
    def dataset_id(self):
        """Gets the dataset_id of this AccessInfoParquetModel.  # noqa: E501

        Unique ID of the Azure dataset where snapshot or dataset tabular data lives   # noqa: E501

        :return: The dataset_id of this AccessInfoParquetModel.  # noqa: E501
        :rtype: str
        """
        return self._dataset_id

    @dataset_id.setter
    def dataset_id(self, dataset_id):
        """Sets the dataset_id of this AccessInfoParquetModel.

        Unique ID of the Azure dataset where snapshot or dataset tabular data lives   # noqa: E501

        :param dataset_id: The dataset_id of this AccessInfoParquetModel.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and dataset_id is None:  # noqa: E501
            raise ValueError("Invalid value for `dataset_id`, must not be `None`")  # noqa: E501

        self._dataset_id = dataset_id

    @property
    def storage_account_id(self):
        """Gets the storage_account_id of this AccessInfoParquetModel.  # noqa: E501

        Project id of the project where tabular data in Azure lives   # noqa: E501

        :return: The storage_account_id of this AccessInfoParquetModel.  # noqa: E501
        :rtype: str
        """
        return self._storage_account_id

    @storage_account_id.setter
    def storage_account_id(self, storage_account_id):
        """Sets the storage_account_id of this AccessInfoParquetModel.

        Project id of the project where tabular data in Azure lives   # noqa: E501

        :param storage_account_id: The storage_account_id of this AccessInfoParquetModel.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and storage_account_id is None:  # noqa: E501
            raise ValueError("Invalid value for `storage_account_id`, must not be `None`")  # noqa: E501

        self._storage_account_id = storage_account_id

    @property
    def signed_url(self):
        """Gets the signed_url of this AccessInfoParquetModel.  # noqa: E501

        The link to access the Azure dataset UI in Google Cloud console   # noqa: E501

        :return: The signed_url of this AccessInfoParquetModel.  # noqa: E501
        :rtype: str
        """
        return self._signed_url

    @signed_url.setter
    def signed_url(self, signed_url):
        """Sets the signed_url of this AccessInfoParquetModel.

        The link to access the Azure dataset UI in Google Cloud console   # noqa: E501

        :param signed_url: The signed_url of this AccessInfoParquetModel.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and signed_url is None:  # noqa: E501
            raise ValueError("Invalid value for `signed_url`, must not be `None`")  # noqa: E501

        self._signed_url = signed_url

    @property
    def tables(self):
        """Gets the tables of this AccessInfoParquetModel.  # noqa: E501

        Information on each table in the Azure dataset   # noqa: E501

        :return: The tables of this AccessInfoParquetModel.  # noqa: E501
        :rtype: list[AccessInfoParquetModelTable]
        """
        return self._tables

    @tables.setter
    def tables(self, tables):
        """Sets the tables of this AccessInfoParquetModel.

        Information on each table in the Azure dataset   # noqa: E501

        :param tables: The tables of this AccessInfoParquetModel.  # noqa: E501
        :type: list[AccessInfoParquetModelTable]
        """
        if self.local_vars_configuration.client_side_validation and tables is None:  # noqa: E501
            raise ValueError("Invalid value for `tables`, must not be `None`")  # noqa: E501

        self._tables = tables

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, AccessInfoParquetModel):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AccessInfoParquetModel):
            return True

        return self.to_dict() != other.to_dict()
