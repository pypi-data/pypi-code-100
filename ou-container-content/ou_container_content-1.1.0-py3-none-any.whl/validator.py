"""Configuration validator for the OU Container Content config.yaml."""
from cerberus import Validator
from typing import Union


def null_to_list(value):
    """Coerce None values to an empty list."""
    if value is None:
        return []
    return value


schema = {
    'paths': {
        'type': 'list',
        'required': False,
        'schema': {
            'type': 'dict',
            'schema': {
                'source': {
                    'type': 'string',
                    'required': True,
                    'empty': False
                },
                'target': {
                    'type': 'string',
                    'required': True,
                    'empty': False
                },
                'overwrite': {
                    'type': 'string',
                    'required': True,
                    'allowed': ['always', 'never', 'if-unchanged']
                }
            }
        },
        'coerce': null_to_list
    },
    'scripts': {
        'type': 'dict',
        'required': False,
        'schema': {
            'startup': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'cmd': {
                            'type': 'string',
                            'required': True,
                            'empty': False
                        }
                    }
                },
                'coerce': null_to_list
            },
            'shutdown': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'cmd': {
                            'type': 'string',
                            'required': True,
                            'empty': False
                        }
                    }
                },
                'coerce': null_to_list
            }
        }
    },
    'services': {
        'type': 'list',
        'required': False,
        'schema': {
            'type': 'string',
            'empty': False
        },
        'coerce': null_to_list
    }
}


def validate_settings(settings: dict) -> Union[dict, bool]:
    """Validate the configuration settings against the configuration schema.

    :param settings: The settings parsed from the configuration file
    :type settings: dict
    :return: The validated and normalised settings if they are valid, otherwise ``False``
    :rtype: boolean or dict
    """
    validator = Validator(schema)
    if settings is None:
        return {}
    elif validator.validate(settings):
        return validator.document
    else:
        error_list = []

        def walk_error_tree(err, path):
            if isinstance(err, dict):
                for key, value in err.items():
                    walk_error_tree(value, path + (str(key), ))
            elif isinstance(err, list):
                for sub_err in err:
                    walk_error_tree(sub_err, path)
            else:
                error_list.append(f'{".".join(path)}: {err}')

        walk_error_tree(validator.errors, ())
        return error_list
