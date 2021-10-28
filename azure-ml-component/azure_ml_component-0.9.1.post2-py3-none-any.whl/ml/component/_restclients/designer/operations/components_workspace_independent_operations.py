# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.pipeline import ClientRawResponse

from .. import models


class ComponentsWorkspaceIndependentOperations(object):
    """ComponentsWorkspaceIndependentOperations operations.

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

    def get_component_run_setting_parameters_mapping(
            self, run_setting_type="Released", custom_headers=None, raw=False, **operation_config):
        """

        :param run_setting_type: Possible values include: 'Released',
         'Testing', 'Legacy', 'All', 'Default', 'Full'
        :type run_setting_type: str or ~designer.models.ModuleRunSettingTypes
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: dict or ClientRawResponse if raw=true
        :rtype: dict[str, list[~designer.models.RunSettingParameter]] or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<designer.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.get_component_run_setting_parameters_mapping.metadata['url']

        # Construct parameters
        query_parameters = {}
        if run_setting_type is not None:
            query_parameters['runSettingType'] = self._serialize.query("run_setting_type", run_setting_type, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Accept'] = 'application/json'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters, header_parameters)
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('{[RunSettingParameter]}', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    get_component_run_setting_parameters_mapping.metadata = {'url': '/component/v1.0/admin/RunSettingParametersMapping'}
