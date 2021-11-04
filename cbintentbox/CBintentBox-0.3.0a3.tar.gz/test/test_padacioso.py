import unittest
from intentBox.parsers.padacioso_extract import PadaciosoExtractor


class TestIntents(unittest.TestCase):
    def setUp(self) -> None:
        self.intents = PadaciosoExtractor()

        weather = ["weather"]
        hello = ["hey", "hello", "hi", "greetings"]
        name = ["my name is {name}"]
        joke = ["tell me a joke", "i want a joke", "say a joke", "tell joke"]
        lights_on = ["turn on the lights", "lights on", "turn lights on",
                     "turn the lights on"]
        lights_off = ["turn off the lights", "lights off", "turn lights off",
                      "turn the lights off"]
        door_on = ["open the door", "open door", "open the doors"]
        door_off = ["close the door", "close door", "close the doors"]
        music = ["play music", "play some songs", "play heavy metal",
                 "play some jazz", "play rock", "play some music"]
        pizza = ["order pizza", "get pizza", "buy pizza"]
        call = ["call {person}", "phone {person}"]
        greet_person = ["say hello to {person}", "tell {person} hello",
                        "tell {person} i said hello"]

        self.intents.register_intent("weather", weather)
        self.intents.register_intent("hello", hello)
        self.intents.register_intent("name", name)
        self.intents.register_intent("joke", joke)
        self.intents.register_intent("lights_on", lights_on)
        self.intents.register_intent("lights_off", lights_off)
        self.intents.register_intent("door_open", door_on)
        self.intents.register_intent("door_close", door_off)
        self.intents.register_intent("play_music", music)
        self.intents.register_intent("pizza", pizza)
        self.intents.register_intent("greet_person", greet_person)
        self.intents.register_intent("call_person", call)

    def test_engine(self):
        def test_intents(utterance, expected_intents):
            res = self.intents.calc(utterance)
            self.assertEqual(set([i["intent_type"] for i in res
                                  if i["conf"] >= 0.5]),
                             set(expected_intents))

        test_intents("tell me a joke and say hello",
                     {'joke'})
        test_intents("nice work! get me a beer", {})
        test_intents("turn off the lights, open the door",
                     {'door_open', 'lights_off'})
        test_intents("Call mom and tell her hello",
                     {'greet_person', 'call_person'})
        test_intents("tell me a joke and the weather",
                     {'joke'})
        test_intents("turn on the lights close the door", {})
        test_intents("close the pod bay doors play some music", {})
        test_intents("play the music satan and friends",   {})
        test_intents(
            "tell me a joke and order some pizza and turn on the lights and close the door and play some songs",
            {'lights_on', 'joke', 'door_close', 'play_music'})
