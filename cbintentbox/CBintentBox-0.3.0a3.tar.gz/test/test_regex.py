import unittest
from intentBox import IntentBox


class TestAll(unittest.TestCase):
    def setUp(self) -> None:
        config = {
            "engines": {"adapt": {"enabled": True},
                        "palavreado": {"enabled": True}}
        }
        intents = IntentBox(config=config)

        intents.register_regex_entity("Location",
                                      [r'\b(at|in|for) (?P<Location>.*)'])
        intents.register_entity("time", ["time", "hours", "hour"])
        intents.register_keyword_intent("time_in_location",
                                        ["time", "Location"])

        self.intents = intents

    def test_all(self):
        def test_intents(utterance, expected_intents):
            res = self.intents.calc(utterance)
            self.assertEqual(set([i["intent_type"] for i in res]),
                             set(expected_intents))
        test_intents('what time is it in London',
                     {'time_in_location'})

