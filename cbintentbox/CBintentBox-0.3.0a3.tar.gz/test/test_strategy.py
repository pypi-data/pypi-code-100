import unittest
from intentBox import IntentBox, IntentDeterminationStrategy


class TestSingleIntent(unittest.TestCase):
    def setUp(self) -> None:
        intents = IntentBox(strategy=IntentDeterminationStrategy.SINGLE_INTENT)

        # sample based intents

        weather = ["weather"]
        hello = ["hey", "hello", "hi", "greetings"]
        joke = ["tell me a joke", "i want a joke", "say a joke", "tell joke"]
        lights_on = ["turn on the lights", "lights on", "turn lights on",
                     "turn the lights on"]
        lights_off = ["turn off the lights", "lights off", "turn lights off",
                      "turn the lights off"]
        music = ["play music", "play some songs", "play heavy metal",
                 "play some jazz", "play rock", "play some music"]
        call = ["call {person}", "phone {person}"]

        intents.register_intent("weather", weather)
        intents.register_intent("hello", hello)
        intents.register_intent("joke", joke)
        intents.register_intent("lights_on", lights_on)
        intents.register_intent("lights_off", lights_off)
        intents.register_intent("play_music", music)
        intents.register_intent("call_person", call)

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

        intents.register_entity("weather", weather)
        intents.register_entity("hello", hello)
        intents.register_entity("name", name)
        intents.register_entity("joke", joke)
        intents.register_entity("door", door)
        intents.register_entity("lights", light)
        intents.register_entity("on", on)
        intents.register_entity("off", off)
        intents.register_entity("play", play)
        intents.register_entity("music", music)
        intents.register_entity("say", say)

        intents.register_keyword_intent("weather", ["weather"], ["say"])
        intents.register_keyword_intent("hello", ["hello"])
        intents.register_keyword_intent("name", ["name"])
        intents.register_keyword_intent("joke", ["joke"], ["say"])
        intents.register_keyword_intent("lights_on", ["lights", "on"])
        intents.register_keyword_intent("lights_off", ["lights", "off"])
        intents.register_keyword_intent("door_open", ["door", "on"])
        intents.register_keyword_intent("door_close", ["door", "off"])
        intents.register_keyword_intent("play_music", ["play", "music"])

        self.intents = intents

    def test_single_intent(self):
        def test_intents(utterance, expected_intents):
            res = self.intents.calc(utterance)
            self.assertEqual(set([i["intent_type"] for i in res]),
                             set(expected_intents))

        test_intents("turn off the lights, open the door",
                     {'lights_off'})
        test_intents("Call mom and tell her hello", [])
        test_intents("tell me a joke and the weather",
                     {'weather'})
        test_intents("turn on the lights close the door",
                     {'lights_on'})
        test_intents("close the pod bay doors play some music", {})
        test_intents("play the music satan and friends",
                     {'play_music'})
        test_intents(
            "tell me a joke and order some pizza and turn on the lights and close the door and play some songs",
            {})

    def test_engines(self):
        def test_engines(utterance, expected_engines):
            res = self.intents.calc(utterance)
            self.assertEqual(set([i["intent_engine"] for i in res]),
                             set(expected_engines))

        test_engines("turn off the lights, open the door",
                     {'nebulento'})
        test_engines("Call mom and tell her hello", {})
        test_engines("tell me a joke and the weather",
                     {'adapt'})
        test_engines("turn on the lights close the door",
                     {'nebulento'})
        test_engines("close the pod bay doors play some music", {})
        test_engines("play the music satan and friends",
                     {'adapt'})
        test_engines(
            "tell me a joke and order some pizza and turn on the lights and close the door and play some songs",
            {})


class TestRemainder(unittest.TestCase):
    def setUp(self) -> None:
        intents = IntentBox(
            strategy=IntentDeterminationStrategy.REMAINDER)

        # sample based intents

        weather = ["weather"]
        hello = ["hey", "hello", "hi", "greetings"]
        joke = ["tell me a joke", "i want a joke", "say a joke",
                "tell joke"]
        lights_on = ["turn on the lights", "lights on", "turn lights on",
                     "turn the lights on"]
        lights_off = ["turn off the lights", "lights off",
                      "turn lights off",
                      "turn the lights off"]
        music = ["play music", "play some songs", "play heavy metal",
                 "play some jazz", "play rock", "play some music"]
        call = ["call {person}", "phone {person}"]

        intents.register_intent("weather", weather)
        intents.register_intent("hello", hello)
        intents.register_intent("joke", joke)
        intents.register_intent("lights_on", lights_on)
        intents.register_intent("lights_off", lights_off)
        intents.register_intent("play_music", music)
        intents.register_intent("call_person", call)

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

        intents.register_entity("weather", weather)
        intents.register_entity("hello", hello)
        intents.register_entity("name", name)
        intents.register_entity("joke", joke)
        intents.register_entity("door", door)
        intents.register_entity("lights", light)
        intents.register_entity("on", on)
        intents.register_entity("off", off)
        intents.register_entity("play", play)
        intents.register_entity("music", music)
        intents.register_entity("say", say)

        intents.register_keyword_intent("weather", ["weather"], ["say"])
        intents.register_keyword_intent("hello", ["hello"])
        intents.register_keyword_intent("name", ["name"])
        intents.register_keyword_intent("joke", ["joke"], ["say"])
        intents.register_keyword_intent("lights_on", ["lights", "on"])
        intents.register_keyword_intent("lights_off", ["lights", "off"])
        intents.register_keyword_intent("door_open", ["door", "on"])
        intents.register_keyword_intent("door_close", ["door", "off"])
        intents.register_keyword_intent("play_music", ["play", "music"])

        self.intents = intents

    def test_remainder(self):
        def test_intents(utterance, expected_intents):
            res = self.intents.calc(utterance)
            self.assertEqual(set([i["intent_type"] for i in res]),
                             set(expected_intents))

        test_intents("turn off the lights, open the door",
                     {'door_open', 'lights_off'})
        test_intents("Call mom and tell her hello", [])
        test_intents("tell me a joke and the weather",
                     {'weather', 'joke'})
        test_intents("turn on the lights close the door",
                     {'lights_on', 'door_close'})
        test_intents("close the pod bay doors play some music", {})
        test_intents("play the music satan and friends",
                     {'play_music'})
        test_intents(
            "tell me a joke and order some pizza and turn on the lights and close the door and play some songs",
            {})

    def test_engines(self):
        def test_engines(utterance, expected_engines):
            res = self.intents.calc(utterance)
            self.assertEqual(set([i["intent_engine"] for i in res]),
                             set(expected_engines))

        test_engines("turn off the lights, open the door",
                     {'nebulento', 'adapt'})
        test_engines("Call mom and tell her hello", {})
        test_engines("tell me a joke and the weather",
                     {'adapt'})
        test_engines("turn on the lights close the door",
                     {'adapt', 'nebulento'})
        test_engines("close the pod bay doors play some music", {})
        test_engines("play the music satan and friends",
                     {'adapt'})
        test_engines(
            "tell me a joke and order some pizza and turn on the lights and close the door and play some songs",
            {})


class TestSegment(unittest.TestCase):
    def setUp(self) -> None:
        intents = IntentBox(
            strategy=IntentDeterminationStrategy.SEGMENT)

        # sample based intents

        weather = ["weather"]
        hello = ["hey", "hello", "hi", "greetings"]
        joke = ["tell me a joke", "i want a joke", "say a joke",
                "tell joke"]
        lights_on = ["turn on the lights", "lights on", "turn lights on",
                     "turn the lights on"]
        lights_off = ["turn off the lights", "lights off",
                      "turn lights off",
                      "turn the lights off"]
        music = ["play music", "play some songs", "play heavy metal",
                 "play some jazz", "play rock", "play some music"]
        call = ["call {person}", "phone {person}"]

        intents.register_intent("weather", weather)
        intents.register_intent("hello", hello)
        intents.register_intent("joke", joke)
        intents.register_intent("lights_on", lights_on)
        intents.register_intent("lights_off", lights_off)
        intents.register_intent("play_music", music)
        intents.register_intent("call_person", call)

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

        intents.register_entity("weather", weather)
        intents.register_entity("hello", hello)
        intents.register_entity("name", name)
        intents.register_entity("joke", joke)
        intents.register_entity("door", door)
        intents.register_entity("lights", light)
        intents.register_entity("on", on)
        intents.register_entity("off", off)
        intents.register_entity("play", play)
        intents.register_entity("music", music)
        intents.register_entity("say", say)

        intents.register_keyword_intent("weather", ["weather"], ["say"])
        intents.register_keyword_intent("hello", ["hello"])
        intents.register_keyword_intent("name", ["name"])
        intents.register_keyword_intent("joke", ["joke"], ["say"])
        intents.register_keyword_intent("lights_on", ["lights", "on"])
        intents.register_keyword_intent("lights_off", ["lights", "off"])
        intents.register_keyword_intent("door_open", ["door", "on"])
        intents.register_keyword_intent("door_close", ["door", "off"])
        intents.register_keyword_intent("play_music", ["play", "music"])

        self.intents = intents

    def test_segment(self):
        def test_intents(utterance, expected_intents):
            res = self.intents.calc(utterance)
            self.assertEqual(set([i["intent_type"] for i in res]),
                             set(expected_intents))

        test_intents("turn off the lights, open the door",
                     {'door_open', 'lights_off'})
        test_intents("Call mom and tell her hello",
                     {'call_person'})
        test_intents("tell me a joke and the weather",
                     {'weather', 'joke'})
        test_intents("turn on the lights close the door",
                     {'lights_on'})
        test_intents("close the pod bay doors play some music", {})
        test_intents("play the music satan and friends",
                     {'play_music'})
        test_intents(
            "tell me a joke and order some pizza and turn on the lights and close the door and play some songs",
            {'play_music', 'door_close', 'joke', 'lights_on'})


class TestSegmentRemainder(unittest.TestCase):
    def setUp(self) -> None:
        intents = IntentBox(
            strategy=IntentDeterminationStrategy.SEGMENT_REMAINDER)

        # sample based intents

        weather = ["weather"]
        hello = ["hey", "hello", "hi", "greetings"]
        joke = ["tell me a joke", "i want a joke", "say a joke",
                "tell joke"]
        lights_on = ["turn on the lights", "lights on", "turn lights on",
                     "turn the lights on"]
        lights_off = ["turn off the lights", "lights off",
                      "turn lights off",
                      "turn the lights off"]
        music = ["play music", "play some songs", "play heavy metal",
                 "play some jazz", "play rock", "play some music"]
        call = ["call {person}", "phone {person}"]

        intents.register_intent("weather", weather)
        intents.register_intent("hello", hello)
        intents.register_intent("joke", joke)
        intents.register_intent("lights_on", lights_on)
        intents.register_intent("lights_off", lights_off)
        intents.register_intent("play_music", music)
        intents.register_intent("call_person", call)

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

        intents.register_entity("weather", weather)
        intents.register_entity("hello", hello)
        intents.register_entity("name", name)
        intents.register_entity("joke", joke)
        intents.register_entity("door", door)
        intents.register_entity("lights", light)
        intents.register_entity("on", on)
        intents.register_entity("off", off)
        intents.register_entity("play", play)
        intents.register_entity("music", music)
        intents.register_entity("say", say)

        intents.register_keyword_intent("weather", ["weather"], ["say"])
        intents.register_keyword_intent("hello", ["hello"])
        intents.register_keyword_intent("name", ["name"])
        intents.register_keyword_intent("joke", ["joke"], ["say"])
        intents.register_keyword_intent("lights_on", ["lights", "on"])
        intents.register_keyword_intent("lights_off", ["lights", "off"])
        intents.register_keyword_intent("door_open", ["door", "on"])
        intents.register_keyword_intent("door_close", ["door", "off"])
        intents.register_keyword_intent("play_music", ["play", "music"])

        self.intents = intents

    def test_segment_remainder(self):
        def test_intents(utterance, expected_intents):
            res = self.intents.calc(utterance)
            self.assertEqual(set([i["intent_type"] for i in res]),
                             set(expected_intents))

        test_intents("turn off the lights, open the door",
                     {'door_open', 'lights_off'})
        test_intents("Call mom and tell her hello",
                     {'call_person'})
        test_intents("tell me a joke and the weather",
                     {'weather', 'joke'})
        test_intents("turn on the lights close the door",
                     {'lights_on', 'door_close'})
        test_intents("close the pod bay doors play some music", {})
        test_intents("play the music satan and friends",
                     {'play_music'})
        test_intents(
            "tell me a joke and order some pizza and turn on the lights and close the door and play some songs",
            {'play_music', 'door_close', 'joke', 'lights_on'})

    def test_engines(self):
        def test_engines(utterance, expected_engines):
            res = self.intents.calc(utterance)
            self.assertEqual(set([i["intent_engine"] for i in res]),
                             set(expected_engines))

        test_engines("turn off the lights, open the door",
                     {'adapt'})
        test_engines("Call mom and tell her hello",
                     {'padacioso'})
        test_engines("tell me a joke and the weather",
                     {'adapt'})
        test_engines("turn on the lights close the door",
                     {'nebulento', 'adapt'})
        test_engines("close the pod bay doors play some music", {})
        test_engines("play the music satan and friends",
                     {'adapt'})
        test_engines(
            "tell me a joke and order some pizza and turn on the lights and close the door and play some songs",
            {'adapt'})
