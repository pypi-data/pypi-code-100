# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ModuleDtoWithValidateStatus(Model):
    """ModuleDtoWithValidateStatus.

    :param existing_module_entity:
    :type existing_module_entity: ~designer.models.ModuleEntity
    :param status: Possible values include: 'NewModule', 'NewVersion',
     'Conflict', 'ParseError', 'ProcessRequestError'
    :type status: str or ~designer.models.ModuleInfoFromYamlStatusEnum
    :param status_details:
    :type status_details: str
    :param serialized_module_info:
    :type serialized_module_info: str
    :param namespace:
    :type namespace: str
    :param tags:
    :type tags: list[str]
    :param display_name:
    :type display_name: str
    :param dict_tags:
    :type dict_tags: dict[str, str]
    :param module_name:
    :type module_name: str
    :param entity_status: Possible values include: 'Active', 'Deprecated',
     'Disabled'
    :type entity_status: str or ~designer.models.EntityStatus
    :param created_date:
    :type created_date: datetime
    :param last_modified_date:
    :type last_modified_date: datetime
    :param versions:
    :type versions: list[~designer.models.AzureMLModuleVersionDescriptor]
    :param default_version:
    :type default_version: str
    :param module_scope: Possible values include: 'All', 'Global',
     'Workspace', 'Anonymous', 'Step', 'Draft', 'Feed'
    :type module_scope: str or ~designer.models.ModuleScope
    :param module_version_id:
    :type module_version_id: str
    :param description:
    :type description: str
    :param owner:
    :type owner: str
    :param job_type:
    :type job_type: str
    :param yaml_link:
    :type yaml_link: str
    :param yaml_link_with_commit_sha:
    :type yaml_link_with_commit_sha: str
    :param family_id:
    :type family_id: str
    :param help_document:
    :type help_document: str
    :param codegen_by:
    :type codegen_by: str
    :param entry:
    :type entry: str
    :param os_type:
    :type os_type: str
    :param module_source_type: Possible values include: 'Unknown', 'Local',
     'GithubFile', 'GithubFolder', 'DevopsArtifactsZip', 'SerializedModuleInfo'
    :type module_source_type: str or ~designer.models.ModuleSourceType
    :param registered_by:
    :type registered_by: str
    :param module_version:
    :type module_version: str
    :param is_default_module_version:
    :type is_default_module_version: bool
    :param module_entity:
    :type module_entity: ~designer.models.ModuleEntity
    :param input_types:
    :type input_types: list[str]
    :param output_types:
    :type output_types: list[str]
    :param run_setting_parameters:
    :type run_setting_parameters: list[~designer.models.RunSettingParameter]
    :param require_gpu:
    :type require_gpu: bool
    :param module_python_interface:
    :type module_python_interface: ~designer.models.ModulePythonInterface
    :param snapshot_id:
    :type snapshot_id: str
    :param yaml_str:
    :type yaml_str: str
    :param feed_name:
    :type feed_name: str
    :param system_data:
    :type system_data: ~designer.models.SystemData
    :param arm_id:
    :type arm_id: str
    """

    _attribute_map = {
        'existing_module_entity': {'key': 'existingModuleEntity', 'type': 'ModuleEntity'},
        'status': {'key': 'status', 'type': 'str'},
        'status_details': {'key': 'statusDetails', 'type': 'str'},
        'serialized_module_info': {'key': 'serializedModuleInfo', 'type': 'str'},
        'namespace': {'key': 'namespace', 'type': 'str'},
        'tags': {'key': 'tags', 'type': '[str]'},
        'display_name': {'key': 'displayName', 'type': 'str'},
        'dict_tags': {'key': 'dictTags', 'type': '{str}'},
        'module_name': {'key': 'moduleName', 'type': 'str'},
        'entity_status': {'key': 'entityStatus', 'type': 'str'},
        'created_date': {'key': 'createdDate', 'type': 'iso-8601'},
        'last_modified_date': {'key': 'lastModifiedDate', 'type': 'iso-8601'},
        'versions': {'key': 'versions', 'type': '[AzureMLModuleVersionDescriptor]'},
        'default_version': {'key': 'defaultVersion', 'type': 'str'},
        'module_scope': {'key': 'moduleScope', 'type': 'str'},
        'module_version_id': {'key': 'moduleVersionId', 'type': 'str'},
        'description': {'key': 'description', 'type': 'str'},
        'owner': {'key': 'owner', 'type': 'str'},
        'job_type': {'key': 'jobType', 'type': 'str'},
        'yaml_link': {'key': 'yamlLink', 'type': 'str'},
        'yaml_link_with_commit_sha': {'key': 'yamlLinkWithCommitSha', 'type': 'str'},
        'family_id': {'key': 'familyId', 'type': 'str'},
        'help_document': {'key': 'helpDocument', 'type': 'str'},
        'codegen_by': {'key': 'codegenBy', 'type': 'str'},
        'entry': {'key': 'entry', 'type': 'str'},
        'os_type': {'key': 'osType', 'type': 'str'},
        'module_source_type': {'key': 'moduleSourceType', 'type': 'str'},
        'registered_by': {'key': 'registeredBy', 'type': 'str'},
        'module_version': {'key': 'moduleVersion', 'type': 'str'},
        'is_default_module_version': {'key': 'isDefaultModuleVersion', 'type': 'bool'},
        'module_entity': {'key': 'moduleEntity', 'type': 'ModuleEntity'},
        'input_types': {'key': 'inputTypes', 'type': '[str]'},
        'output_types': {'key': 'outputTypes', 'type': '[str]'},
        'run_setting_parameters': {'key': 'runSettingParameters', 'type': '[RunSettingParameter]'},
        'require_gpu': {'key': 'requireGpu', 'type': 'bool'},
        'module_python_interface': {'key': 'modulePythonInterface', 'type': 'ModulePythonInterface'},
        'snapshot_id': {'key': 'snapshotId', 'type': 'str'},
        'yaml_str': {'key': 'yamlStr', 'type': 'str'},
        'feed_name': {'key': 'feedName', 'type': 'str'},
        'system_data': {'key': 'systemData', 'type': 'SystemData'},
        'arm_id': {'key': 'armId', 'type': 'str'},
    }

    def __init__(self, *, existing_module_entity=None, status=None, status_details: str=None, serialized_module_info: str=None, namespace: str=None, tags=None, display_name: str=None, dict_tags=None, module_name: str=None, entity_status=None, created_date=None, last_modified_date=None, versions=None, default_version: str=None, module_scope=None, module_version_id: str=None, description: str=None, owner: str=None, job_type: str=None, yaml_link: str=None, yaml_link_with_commit_sha: str=None, family_id: str=None, help_document: str=None, codegen_by: str=None, entry: str=None, os_type: str=None, module_source_type=None, registered_by: str=None, module_version: str=None, is_default_module_version: bool=None, module_entity=None, input_types=None, output_types=None, run_setting_parameters=None, require_gpu: bool=None, module_python_interface=None, snapshot_id: str=None, yaml_str: str=None, feed_name: str=None, system_data=None, arm_id: str=None, **kwargs) -> None:
        super(ModuleDtoWithValidateStatus, self).__init__(**kwargs)
        self.existing_module_entity = existing_module_entity
        self.status = status
        self.status_details = status_details
        self.serialized_module_info = serialized_module_info
        self.namespace = namespace
        self.tags = tags
        self.display_name = display_name
        self.dict_tags = dict_tags
        self.module_name = module_name
        self.entity_status = entity_status
        self.created_date = created_date
        self.last_modified_date = last_modified_date
        self.versions = versions
        self.default_version = default_version
        self.module_scope = module_scope
        self.module_version_id = module_version_id
        self.description = description
        self.owner = owner
        self.job_type = job_type
        self.yaml_link = yaml_link
        self.yaml_link_with_commit_sha = yaml_link_with_commit_sha
        self.family_id = family_id
        self.help_document = help_document
        self.codegen_by = codegen_by
        self.entry = entry
        self.os_type = os_type
        self.module_source_type = module_source_type
        self.registered_by = registered_by
        self.module_version = module_version
        self.is_default_module_version = is_default_module_version
        self.module_entity = module_entity
        self.input_types = input_types
        self.output_types = output_types
        self.run_setting_parameters = run_setting_parameters
        self.require_gpu = require_gpu
        self.module_python_interface = module_python_interface
        self.snapshot_id = snapshot_id
        self.yaml_str = yaml_str
        self.feed_name = feed_name
        self.system_data = system_data
        self.arm_id = arm_id
