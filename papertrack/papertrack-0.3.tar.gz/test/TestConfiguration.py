import unittest 

from papertrack.core import  Configuration, Field

class TestConfiguration(unittest.TestCase):
    def test__empty_configuration_created(self):
        config = Configuration()
        self.assertIsInstance(config, Configuration)
    
    def test_given_empty_configuration_returns_default_state_list(self):
        config = Configuration()
        self.assertListEqual(config.get_document_states(), ["READY", "READING", "DONE"])
    
    def test_given_document_states_returns_document_states(self):
        config = Configuration({
            "states": {
                "A": {
                    "B": "Transition to B"
                },
                "B": {
                    "A": "go back to A"
                }
            }
        })
        self.assertListEqual(config.get_document_states(), ["A", "B"])
    def test_given_document_states_returns_document_state_transitions(self):
        config = Configuration({
            "states": {
                "A": {
                    "B": "Transition to B"
                },
                "B": {
                    "A": "go back to A"
                }
            }
        })
        self.assertListEqual(config.get_document_state_transitions("A"), [("B", "Transition to B")])
    
    def test_given_empty_configuration_sreturns_state_transitions_for_default(self):
        config = Configuration()
        self.assertListEqual(config.get_document_state_transitions("READY"), [
            ("READING", "Start reading")
        ])
        self.assertListEqual(config.get_document_state_transitions("READING"), [
            ("DONE", "Finish reading"),
            ("READY", "Bring back to to-read state")
        ])
        self.assertRaises(ValueError, lambda: config.get_document_state_transitions("AAA"))
    
    def test_given_empty_configuration_default_document_state_is_ready(self):
        config = Configuration()
        self.assertEqual(config.get_default_document_state(), "READY")
    
    def test_given_custom_configuration_default_document_state_is_obtained(self):
        config = Configuration({
            "states": {
                "A": {},
                "B": {}
            },
            "default_state": "A"
        })
        self.assertEqual(config.get_default_document_state(), "A")
    def test_given_custom_configuration_and_nonexistant_default_state_throws_value_error(self):
        config = Configuration({
            "states": {
                "A": {},
                "B": {}
            },
            "default_state": "C"
        })
        self.assertRaises(ValueError, lambda: config.get_default_document_state())
    
    def test_given_empty_configuration_default_storage_location_is_given(self):
        config = Configuration()
        self.assertIsInstance(config.get_storage_location(), str)
    
    def test_given_custom_configuration_gives_correct_storage_location(self):
        config = Configuration({
            "storage_location": "/my/storage/"
        })
        self.assertEqual(config.get_storage_location(), "/my/storage/")
    
    def test_get_fields(self):
        config = Configuration({
            "fields": {
                "A": {
                    "categories": ["A1", "A2"]
                },
                "B": {
                    "categories": ["B1", "B2"],
                    "default": "B2"
                }
            }
        })
        self.assertListEqual(config.get_fields(), [
            Field(name="A", categories = ["A1", "A2"], default_category="A1"),
            Field(name="B", categories = ["B1", "B2"], default_category="B2"),
        ])