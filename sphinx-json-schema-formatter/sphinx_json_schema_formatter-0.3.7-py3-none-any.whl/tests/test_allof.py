from unittest import TestCase

from sphinx_json_schema_formatter.mergers import merge


class AllOfTestCase(TestCase):
    def test_merge_properties(self):
        base = {
            "required": ["A"],
            "properties": {
                "A": {"type": "string", "enum": ["x", "y"]},
                "B": {"type": "string"},
            },
        }

        to_merge = {
            "required": ["C"],
            "properties": {
                "A": {"type": "string", "enum": ["x"]},
                "C": {"type": "string"},
            },
        }

        merge(base, to_merge, "allOf")

        self.assertDictEqual(
            base,
            {
                "required": ["A", "C"],
                "properties": {
                    "A": {"type": "string", "enum": ["x"]},
                    "B": {"type": "string"},
                    "C": {"type": "string"},
                },
            },
        )
