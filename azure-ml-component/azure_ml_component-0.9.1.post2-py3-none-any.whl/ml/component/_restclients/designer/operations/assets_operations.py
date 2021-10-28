# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.pipeline import ClientRawResponse

from .. import models


class AssetsOperations(object):
    """AssetsOperations operations.

    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An object model deserializer.
    """

    models = models

    def __init__(self, client, config, serializer, deserializer):

        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer

        self.config = config

    def parse_component(
            self, subscription_id, resource_group_name, workspace_name, snapshot_source_zip_file=None, properties=None, custom_headers=None, raw=False, **operation_config):
        """

        :param subscription_id: The Azure Subscription ID.
        :type subscription_id: str
        :param resource_group_name: The Name of the resource group in which
         the workspace is located.
        :type resource_group_name: str
        :param workspace_name: The name of the workspace.
        :type workspace_name: str
        :param snapshot_source_zip_file:
        :type snapshot_source_zip_file: str
        :param properties: ModuleSourceType: string, YamlFile: string,
         DevopsArtifactsZipUrl: string, ContainerSAS: string
        :type properties: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: ParsedAssetMetaInfo or ClientRawResponse if raw=true
        :rtype: ~designer.models.ParsedAssetMetaInfo or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<designer.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.parse_component.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters['Accept'] = 'application/json'
        header_parameters['Content-Type'] = 'multipart/form-data'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct form data
        form_data_content = {
            'SnapshotSourceZipFile': snapshot_source_zip_file,
            'properties': properties,
        }

        # Construct and send request
        request = self._client.post(url, query_parameters, header_parameters, form_content=form_data_content)
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('ParsedAssetMetaInfo', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    parse_component.metadata = {'url': '/studioservice/api/admin/Assets/component/parse'}

    def parse_dataset(
            self, subscription_id, resource_group_name, workspace_name, module_source_type=None, yaml_file=None, snapshot_source_zip_file=None, devops_artifacts_zip_url=None, container_sas=None, custom_headers=None, raw=False, **operation_config):
        """

        :param subscription_id: The Azure Subscription ID.
        :type subscription_id: str
        :param resource_group_name: The Name of the resource group in which
         the workspace is located.
        :type resource_group_name: str
        :param workspace_name: The name of the workspace.
        :type workspace_name: str
        :param module_source_type: Possible values include: 'Unknown',
         'Local', 'GithubFile', 'GithubFolder', 'DevopsArtifactsZip',
         'SerializedModuleInfo'
        :type module_source_type: str or ~designer.models.ModuleSourceType
        :param yaml_file:
        :type yaml_file: str
        :param snapshot_source_zip_file:
        :type snapshot_source_zip_file: str
        :param devops_artifacts_zip_url:
        :type devops_artifacts_zip_url: str
        :param container_sas:
        :type container_sas: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: ParsedAssetMetaInfo or ClientRawResponse if raw=true
        :rtype: ~designer.models.ParsedAssetMetaInfo or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<designer.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.parse_dataset.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters['Accept'] = 'application/json'
        header_parameters['Content-Type'] = 'multipart/form-data'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct form data
        form_data_content = {
            'ModuleSourceType': module_source_type,
            'YamlFile': yaml_file,
            'SnapshotSourceZipFile': snapshot_source_zip_file,
            'DevopsArtifactsZipUrl': devops_artifacts_zip_url,
            'ContainerSAS': container_sas,
        }

        # Construct and send request
        request = self._client.post(url, query_parameters, header_parameters, form_content=form_data_content)
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('ParsedAssetMetaInfo', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    parse_dataset.metadata = {'url': '/studioservice/api/admin/Assets/dataset/parse'}

    def parse_model(
            self, subscription_id, resource_group_name, workspace_name, module_source_type=None, yaml_file=None, snapshot_source_zip_file=None, devops_artifacts_zip_url=None, container_sas=None, custom_headers=None, raw=False, **operation_config):
        """

        :param subscription_id: The Azure Subscription ID.
        :type subscription_id: str
        :param resource_group_name: The Name of the resource group in which
         the workspace is located.
        :type resource_group_name: str
        :param workspace_name: The name of the workspace.
        :type workspace_name: str
        :param module_source_type: Possible values include: 'Unknown',
         'Local', 'GithubFile', 'GithubFolder', 'DevopsArtifactsZip',
         'SerializedModuleInfo'
        :type module_source_type: str or ~designer.models.ModuleSourceType
        :param yaml_file:
        :type yaml_file: str
        :param snapshot_source_zip_file:
        :type snapshot_source_zip_file: str
        :param devops_artifacts_zip_url:
        :type devops_artifacts_zip_url: str
        :param container_sas:
        :type container_sas: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: ParsedAssetMetaInfo or ClientRawResponse if raw=true
        :rtype: ~designer.models.ParsedAssetMetaInfo or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<designer.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.parse_model.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters['Accept'] = 'application/json'
        header_parameters['Content-Type'] = 'multipart/form-data'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct form data
        form_data_content = {
            'ModuleSourceType': module_source_type,
            'YamlFile': yaml_file,
            'SnapshotSourceZipFile': snapshot_source_zip_file,
            'DevopsArtifactsZipUrl': devops_artifacts_zip_url,
            'ContainerSAS': container_sas,
        }

        # Construct and send request
        request = self._client.post(url, query_parameters, header_parameters, form_content=form_data_content)
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('ParsedAssetMetaInfo', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    parse_model.metadata = {'url': '/studioservice/api/admin/Assets/model/parse'}
