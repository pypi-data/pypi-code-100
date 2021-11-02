import json

import jst


def test_array_with_atomics():
    input_data = {"items": {"type": "integer"}, "type": "array"}
    expected_data = [{"mode": "REPEATED", "name": "root", "type": "INT64"}]
    assert json.loads(jst.convert_bq(json.dumps(input_data))) == expected_data


def test_array_with_complex():
    input_data = {
        "items": {"properties": {"field_1": {"type": "string"}, "field_2": {"type": "integer"}}, "type": "object"},
        "type": "array",
    }
    expected_data = [
        {
            "fields": [
                {"mode": "NULLABLE", "name": "field_1", "type": "STRING"},
                {"mode": "NULLABLE", "name": "field_2", "type": "INT64"},
            ],
            "mode": "REPEATED",
            "name": "root",
            "type": "RECORD",
        }
    ]
    assert json.loads(jst.convert_bq(json.dumps(input_data))) == expected_data