import json

import jst


def test_array_with_atomics():
    input_data = {"items": {"type": "integer"}, "type": "array"}
    expected_data = {"items": {"type": "long"}, "type": "array"}
    assert json.loads(jst.convert_avro(json.dumps(input_data))) == expected_data


def test_array_with_complex():
    input_data = {
        "items": {"properties": {"field_1": {"type": "string"}, "field_2": {"type": "integer"}}, "type": "object"},
        "type": "array",
    }
    expected_data = {
        "items": {
            "fields": [
                {"default": None, "name": "field_1", "type": [{"type": "null"}, {"type": "string"}]},
                {"default": None, "name": "field_2", "type": [{"type": "null"}, {"type": "long"}]},
            ],
            "name": "list",
            "namespace": "root",
            "type": "record",
        },
        "type": "array",
    }
    assert json.loads(jst.convert_avro(json.dumps(input_data))) == expected_data
