import json
import jsonschema

msg = {'rtdh_timestamp': 1636143202.716094, 'rtdh_message_id': '97a5a22c-490a-4aaa-9156-d4a544ea6095', 'event': {'type': 'CONSTRUCTION', 'source': {'id': '1245', 'last_updated_timestamp': 1636164481}, 'geometry': [[-84.1238971, 37.1686478], [-84.1238971, 37.1686478], [-84.145861, 37.1913], [
    -84.145861, 37.1913], [-84.157105, 37.201197], [-84.167033, 37.206079], [-84.204074, 37.21931]], 'header': {'description': '19-1245: Roadwork between MP 40 and MP 48', 'start_timestamp': 1623204901, 'end_timestamp': None}, 'detail': {'road_name': 'I-75 N', 'road_number': 'I-75 N', 'direction': 'northbound'}}}

schema = json.loads("""
    {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "properties": {
        "event": {
            "properties": {
                "detail": {
                    "properties": {
                        "direction": {
                            "type": ["string", "null"]
                        },
                        "road_name": {
                            "type": "string"
                        },
                        "road_number": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "road_name",
                        "road_number",
                        "direction"
                    ],
                    "type": "object"
                },
                "geometry": {
                    "items": [
                        {
                            "items": [
                                {
                                    "type": "number"
                                },
                                {
                                    "type": "number"
                                }
                            ],
                            "type": "array"
                        },
                        {
                            "items": [
                                {
                                    "type": "number"
                                },
                                {
                                    "type": "number"
                                }
                            ],
                            "type": "array"
                        },
                        {
                            "items": [
                                {
                                    "type": "number"
                                },
                                {
                                    "type": "number"
                                }
                            ],
                            "type": "array"
                        },
                        {
                            "items": [
                                {
                                    "type": "number"
                                },
                                {
                                    "type": "number"
                                }
                            ],
                            "type": "array"
                        },
                        {
                            "items": [
                                {
                                    "type": "number"
                                },
                                {
                                    "type": "number"
                                }
                            ],
                            "type": "array"
                        }
                    ],
                    "type": "array"
                },
                "header": {
                    "properties": {
                        "description": {
                            "type": "string"
                        },
                        "end_timestamp": {
                            "type": ["integer", "null"]
                        },
                        "start_timestamp": {
                            "type": "integer"
                        }
                    },
                    "required": [
                        "description",
                        "start_timestamp",
                        "end_timestamp"
                    ],
                    "type": "object"
                },
                "source": {
                    "properties": {
                        "id": {
                            "type": "integer"
                        },
                        "last_updated_timestamp": {
                            "type": "integer"
                        }
                    },
                    "required": [
                        "id",
                        "last_updated_timestamp"
                    ],
                    "type": "object"
                },
                "type": {
                    "type": "string"
                }
            },
            "required": [
                "type",
                "source",
                "geometry",
                "header",
                "detail"
            ],
            "type": "object"
        },
        "rtdh_message_id": {
            "type": "string"
        },
        "rtdh_timestamp": {
            "type": "number"
        }
    },
    "required": [
        "rtdh_timestamp",
        "rtdh_message_id",
        "event"
    ],
    "type": "object"
}
""")

jsonschema.validate(msg, schema)
