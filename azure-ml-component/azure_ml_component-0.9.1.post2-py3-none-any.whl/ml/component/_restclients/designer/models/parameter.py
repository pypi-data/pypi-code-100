# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class Parameter(Model):
    """Parameter.

    :param name:
    :type name: str
    :param documentation:
    :type documentation: str
    :param default_value:
    :type default_value: str
    :param is_optional:
    :type is_optional: bool
    :param min_max_rules:
    :type min_max_rules: list[~designer.models.MinMaxParameterRule]
    :param enum_rules:
    :type enum_rules: list[~designer.models.EnumParameterRule]
    :param type: Possible values include: 'Int', 'Double', 'Bool', 'String',
     'Undefined'
    :type type: str or ~designer.models.ParameterType
    :param label:
    :type label: str
    :param group_names:
    :type group_names: list[str]
    :param argument_name:
    :type argument_name: str
    """

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'documentation': {'key': 'documentation', 'type': 'str'},
        'default_value': {'key': 'defaultValue', 'type': 'str'},
        'is_optional': {'key': 'isOptional', 'type': 'bool'},
        'min_max_rules': {'key': 'minMaxRules', 'type': '[MinMaxParameterRule]'},
        'enum_rules': {'key': 'enumRules', 'type': '[EnumParameterRule]'},
        'type': {'key': 'type', 'type': 'str'},
        'label': {'key': 'label', 'type': 'str'},
        'group_names': {'key': 'groupNames', 'type': '[str]'},
        'argument_name': {'key': 'argumentName', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(Parameter, self).__init__(**kwargs)
        self.name = kwargs.get('name', None)
        self.documentation = kwargs.get('documentation', None)
        self.default_value = kwargs.get('default_value', None)
        self.is_optional = kwargs.get('is_optional', None)
        self.min_max_rules = kwargs.get('min_max_rules', None)
        self.enum_rules = kwargs.get('enum_rules', None)
        self.type = kwargs.get('type', None)
        self.label = kwargs.get('label', None)
        self.group_names = kwargs.get('group_names', None)
        self.argument_name = kwargs.get('argument_name', None)
