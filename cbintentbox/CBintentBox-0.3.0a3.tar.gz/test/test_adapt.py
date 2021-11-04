import unittest
from intentBox.parsers.adapt_extract import AdaptExtractor


class TestIntents(unittest.TestCase):
    def setUp(self) -> None:
        self.intents = AdaptExtractor()

        # keyword based intents
        weather = ["weather"]
        hello = ["hey", "hello", "hi", "greetings"]
        name = ["name is"]
        joke = ["joke"]
        play = ["play"]
        say = ["say", "tell"]
        music = ["music", "jazz", "metal", "rock", "songs"]
        door = ["door", "doors"]
        light = ["light", "lights"]
        on = ["activate", "on", "engage", "open"]
        off = ["deactivate", "off", "disengage", "close"]

        self.intents.register_entity("weather", weather)
        self.intents.register_entity("hello", hello)
        self.intents.register_entity("name", name)
        self.intents.register_entity("joke", joke)
        self.intents.register_entity("door", door)
        self.intents.register_entity("lights", light)
        self.intents.register_entity("on", on)
        self.intents.register_entity("off", off)
        self.intents.register_entity("play", play)
        self.intents.register_entity("music", music)
        self.intents.register_entity("say", say)

        self.intents.register_intent("weather", ["weather"])
        self.intents.register_intent("hello", ["hello"])
        self.intents.register_intent("name", ["name"])
        self.intents.register_intent("joke", ["joke"], ["say"])
        self.intents.register_intent("lights_on", ["lights", "on"])
        self.intents.register_intent("lights_off", ["lights", "off"])
        self.intents.register_intent("door_open", ["door", "on"])
        self.intents.register_intent("door_close", ["door", "off"])
        self.intents.register_intent("play_music", ["play", "music"])

    def test_intent(self):
        def test_intents(utterance, expected_intents):
            res = self.intents.calc(utterance)
            self.assertEqual(set([i["intent_type"] for i in res
                                  if i["intent_type"] != 'unknown']),
                             set(expected_intents))

        test_intents("turn off the lights, open the door",
                     {'door_open', 'lights_off'})
        test_intents("Call mom and tell her hello",
                     {'hello'})
        test_intents("tell me a joke and the weather",
                     {'weather', 'joke'})
        test_intents("turn on the lights close the door",
                     {'door_close', 'lights_on'})
        test_intents("close the pod bay doors play some music",
                     {'play_music', 'door_close'})
        test_intents("play the music satan and friends",
                     {'play_music'})
        test_intents(
            "tell me a joke and order some pizza and turn on the lights and close the door and play some songs",
            {'lights_on', 'joke', 'door_close', 'play_music'})
