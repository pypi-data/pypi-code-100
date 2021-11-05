schema1 = {'type': 'string'}


schema2 = {'type': 'integer'}


schema3 = {
    '$id': 'py-obj:jsonschema_pyref.examples.schema3',
    'type': 'object',
    'properties': {
        'foo': {'$ref': '#/$defs/foo'}
    },
    'additionalProperties': False,
    '$defs': {
        'foo': {'type': 'string'}
    }
}


schema4 = {
    '$id': 'py-obj:jsonschema_pyref.examples.schema4',
    'type': 'object',
    'properties': {
        'foo': {'$ref': 'py-obj:jsonschema_pyref.examples.schema3'},
        'bar': {'$ref': '#/$defs/bar'}
    },
    'additionalProperties': False,
    '$defs': {
        'bar': {'type': 'integer'}
    }
}
