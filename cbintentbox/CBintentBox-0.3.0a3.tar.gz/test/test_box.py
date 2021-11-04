import unittest
from intentBox import IntentBox, IntentDeterminationStrategy


class TestDefaults(unittest.TestCase):
    def setUp(self) -> None:
        intents = IntentBox()

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

    def test_defaults(self):
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


class TestAll(unittest.TestCase):
    def setUp(self) -> None:
        config = {
            "engines": {"nebulento": {"enabled": True},
                        "adapt": {"enabled": True},
                        "palavreado": {"enabled": True},
                        "padacioso": {"enabled": True},
                        "padaos": {"enabled": True},
                        "padatious": {"enabled": True}}
        }
        intents = IntentBox(config=config,
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

        intents.register_keyword_intent("weather", ["weather"])
        intents.register_keyword_intent("hello", ["hello"])
        intents.register_keyword_intent("name", ["name"])
        intents.register_keyword_intent("joke", ["joke"], ["say"])
        intents.register_keyword_intent("lights_on", ["lights", "on"])
        intents.register_keyword_intent("lights_off", ["lights", "off"])
        intents.register_keyword_intent("door_open", ["door", "on"])
        intents.register_keyword_intent("door_close", ["door", "off"])
        intents.register_keyword_intent("play_music", ["play", "music"])

        self.intents = intents

    def test_all(self):
        def test_intents(utterance, expected_intents):
            res = self.intents.calc(utterance)
            self.assertEqual(set([i["intent_type"] for i in res
                                  if i["conf"] > 0.5]),
                             set(expected_intents))

        test_intents("turn off the lights, open the door",
                     {'door_open', 'lights_off'})
        test_intents("Call mom and tell her hello",
                     {'call_person', 'hello'})
        test_intents("tell me a joke and the weather",
                     {'weather', 'joke'})
        test_intents("close the pod bay doors play some music",
                     {'door_close', 'play_music'})
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
                     {'padatious', 'nebulento', 'palavreado'})
        test_engines("tell me a joke and the weather",
                     {'adapt'})
        test_engines("turn on the lights close the door",
                     {'palavreado', 'adapt'})
        test_engines("close the pod bay doors play some music",
                     {'adapt', 'palavreado'})
        test_engines("play the music satan and friends",
                     {'adapt'})
        test_engines(
            "tell me a joke and order some pizza and turn on the lights and close the door and play some songs",
            {'adapt'})


class TestPadatious(unittest.TestCase):
    def setUp(self) -> None:
        config = {
            "engines": {"nebulento": {"enabled": False},
                        "adapt": {"enabled": False},
                        "palavreado": {"enabled": False},
                        "padacioso": {"enabled": False},
                        "padaos": {"enabled": False},
                        "padatious": {"enabled": True}}
        }
        intents = IntentBox(config=config,
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

        intents.register_keyword_intent("weather", ["weather"])
        intents.register_keyword_intent("hello", ["hello"])
        intents.register_keyword_intent("name", ["name"])
        intents.register_keyword_intent("joke", ["joke"], ["say"])
        intents.register_keyword_intent("lights_on", ["lights", "on"])
        intents.register_keyword_intent("lights_off", ["lights", "off"])
        intents.register_keyword_intent("door_open", ["door", "on"])
        intents.register_keyword_intent("door_close", ["door", "off"])
        intents.register_keyword_intent("play_music", ["play", "music"])

        self.intents = intents

    def test_all(self):
        def test_intents(utterance, expected_intents):
            res = self.intents.calc(utterance)
            self.assertEqual(set([i["intent_type"] for i in res]),
                             set(expected_intents))

        test_intents("turn off the lights, open the door",
                     {'lights_off'})
        test_intents("Call mom and tell her hello",
                     {'call_person'})
        test_intents("tell me a joke and the weather",
                     {'joke'})
        test_intents("turn on the lights close the door",
                     {})
        test_intents("close the pod bay doors play some music", {})
        test_intents("play the music satan and friends",
                     {})
        test_intents(
            "tell me a joke and order some pizza and turn on the lights and close the door and play some songs",
            {'play_music', 'joke', 'lights_on'})

    def test_engines(self):
        def test_engines(utterance, expected_engines):
            res = self.intents.calc(utterance)
            self.assertEqual(set([i["intent_engine"] for i in res]),
                             set(expected_engines))

        test_engines("turn off the lights, open the door",
                     {'padatious'})
        test_engines("Call mom and tell her hello",
                     {'padatious'})
        test_engines("tell me a joke and the weather",
                     {'padatious'})
        test_engines("turn on the lights close the door", {})
        test_engines("close the pod bay doors play some music", {})
        test_engines("play the music satan and friends", {})
        test_engines(
            "tell me a joke and order some pizza and turn on the lights and close the door and play some songs",
            {'padatious'})


class TestPadaos(unittest.TestCase):
    def setUp(self) -> None:
        config = {
            "engines": {"nebulento": {"enabled": False},
                        "adapt": {"enabled": False},
                        "palavreado": {"enabled": False},
                        "padacioso": {"enabled": False},
                        "padaos": {"enabled": True},
                        "padatious": {"enabled": False}}
        }
        intents = IntentBox(config=config,
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

        intents.register_keyword_intent("weather", ["weather"])
        intents.register_keyword_intent("hello", ["hello"])
        intents.register_keyword_intent("name", ["name"])
        intents.register_keyword_intent("joke", ["joke"], ["say"])
        intents.register_keyword_intent("lights_on", ["lights", "on"])
        intents.register_keyword_intent("lights_off", ["lights", "off"])
        intents.register_keyword_intent("door_open", ["door", "on"])
        intents.register_keyword_intent("door_close", ["door", "off"])
        intents.register_keyword_intent("play_music", ["play", "music"])

        self.intents = intents

    def test_all(self):
        def test_intents(utterance, expected_intents):
            res = self.intents.calc(utterance)
            self.assertEqual(set([i["intent_type"] for i in res]),
                             set(expected_intents))

        test_intents("turn off the lights, open the door",
                     {'lights_off'})
        test_intents("Call mom and tell her hello",
                     {'call_person'})
        test_intents("tell me a joke and the weather",
                     {'joke'})
        test_intents("turn on the lights close the door",
                     {})
        test_intents("close the pod bay doors play some music", {})
        test_intents("play the music satan and friends",
                     {})
        test_intents(
            "tell me a joke and order some pizza and turn on the lights and close the door and play some songs",
            {'play_music', 'joke', 'lights_on'})

    def test_engines(self):
        def test_engines(utterance, expected_engines):
            res = self.intents.calc(utterance)
            self.assertEqual(set([i["intent_engine"] for i in res]),
                             set(expected_engines))

        test_engines("turn off the lights, open the door",
                     {'padaos'})
        test_engines("Call mom and tell her hello",
                     {'padaos'})
        test_engines("tell me a joke and the weather",
                     {'padaos'})
        test_engines("turn on the lights close the door", {})
        test_engines("close the pod bay doors play some music", {})
        test_engines("play the music satan and friends", {})
        test_engines(
            "tell me a joke and order some pizza and turn on the lights and close the door and play some songs",
            {'padaos'})


class TestPadacioso(unittest.TestCase):
    def setUp(self) -> None:
        config = {
            "engines": {"nebulento": {"enabled": False},
                        "adapt": {"enabled": False},
                        "palavreado": {"enabled": False},
                        "padacioso": {"enabled": True},
                        "padaos": {"enabled": False},
                        "padatious": {"enabled": False}}
        }
        intents = IntentBox(config=config,
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

        intents.register_keyword_intent("weather", ["weather"])
        intents.register_keyword_intent("hello", ["hello"])
        intents.register_keyword_intent("name", ["name"])
        intents.register_keyword_intent("joke", ["joke"], ["say"])
        intents.register_keyword_intent("lights_on", ["lights", "on"])
        intents.register_keyword_intent("lights_off", ["lights", "off"])
        intents.register_keyword_intent("door_open", ["door", "on"])
        intents.register_keyword_intent("door_close", ["door", "off"])
        intents.register_keyword_intent("play_music", ["play", "music"])

        self.intents = intents

    def test_all(self):
        def test_intents(utterance, expected_intents):
            res = self.intents.calc(utterance)
            self.assertEqual(set([i["intent_type"] for i in res]),
                             set(expected_intents))

        test_intents("turn off the lights, open the door",
                     {'lights_off'})
        test_intents("Call mom and tell her hello",
                     {'call_person'})
        test_intents("tell me a joke and the weather",
                     {'joke'})
        test_intents("turn on the lights close the door",
                     {})
        test_intents("close the pod bay doors play some music", {})
        test_intents("play the music satan and friends",
                     {})
        test_intents(
            "tell me a joke and order some pizza and turn on the lights and close the door and play some songs",
            {'play_music', 'joke', 'lights_on'})

    def test_engines(self):
        def test_engines(utterance, expected_engines):
            res = self.intents.calc(utterance)
            self.assertEqual(set([i["intent_engine"] for i in res]),
                             set(expected_engines))

        test_engines("turn off the lights, open the door",
                     {'padacioso'})
        test_engines("Call mom and tell her hello",
                     {'padacioso'})
        test_engines("tell me a joke and the weather",
                     {'padacioso'})
        test_engines("turn on the lights close the door", {})
        test_engines("close the pod bay doors play some music", {})
        test_engines("play the music satan and friends", {})
        test_engines(
            "tell me a joke and order some pizza and turn on the lights and close the door and play some songs",
            {'padacioso'})


class TestPalavreado(unittest.TestCase):
    def setUp(self) -> None:
        config = {
            "engines": {"nebulento": {"enabled": False},
                        "adapt": {"enabled": False},
                        "palavreado": {"enabled": True},
                        "padacioso": {"enabled": False},
                        "padaos": {"enabled": False},
                        "padatious": {"enabled": False}}
        }
        intents = IntentBox(config=config,
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

        intents.register_keyword_intent("weather", ["weather"])
        intents.register_keyword_intent("hello", ["hello"])
        intents.register_keyword_intent("name", ["name"])
        intents.register_keyword_intent("joke", ["joke"], ["say"])
        intents.register_keyword_intent("lights_on", ["lights", "on"])
        intents.register_keyword_intent("lights_off", ["lights", "off"])
        intents.register_keyword_intent("door_open", ["door", "on"])
        intents.register_keyword_intent("door_close", ["door", "off"])
        intents.register_keyword_intent("play_music", ["play", "music"])

        self.intents = intents

    def test_all(self):
        def test_intents(utterance, expected_intents):
            res = self.intents.calc(utterance)
            self.assertEqual(set([i["intent_type"] for i in res]),
                             set(expected_intents))

        test_intents("turn off the lights, open the door",
                     {'door_open', 'lights_off'})
        test_intents("Call mom and tell her hello",
                     {'hello'})
        test_intents("tell me a joke and the weather",
                     {'joke', 'weather'})
        test_intents("turn on the lights close the door",
                     {'lights_off', 'door_open'})
        test_intents("close the pod bay doors play some music",
                     {'play_music', 'door_close'})
        test_intents("play the music satan and friends",
                     {'play_music'})
        test_intents(
            "tell me a joke and order some pizza and turn on the lights and close the door and play some songs",
            {'play_music', 'lights_on', 'door_close', 'joke'})

    def test_engines(self):
        def test_engines(utterance, expected_engines):
            res = self.intents.calc(utterance)
            self.assertEqual(set([i["intent_engine"] for i in res]),
                             set(expected_engines))

        test_engines("turn off the lights, open the door",
                     {'palavreado'})
        test_engines("Call mom and tell her hello",
                     {'palavreado'})
        test_engines("tell me a joke and the weather",
                     {'palavreado'})
        test_engines("turn on the lights close the door", {'palavreado'})
        test_engines("close the pod bay doors play some music", {'palavreado'})
        test_engines("play the music satan and friends", {'palavreado'})
        test_engines(
            "tell me a joke and order some pizza and turn on the lights and close the door and play some songs",
            {'palavreado'})


class TestAdapt(unittest.TestCase):
    def setUp(self) -> None:
        config = {
            "engines": {"nebulento": {"enabled": False},
                        "adapt": {"enabled": True},
                        "palavreado": {"enabled": False},
                        "padacioso": {"enabled": False},
                        "padaos": {"enabled": False},
                        "padatious": {"enabled": False}}
        }
        intents = IntentBox(config=config,
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

        intents.register_keyword_intent("weather", ["weather"])
        intents.register_keyword_intent("hello", ["hello"])
        intents.register_keyword_intent("name", ["name"])
        intents.register_keyword_intent("joke", ["joke"], ["say"])
        intents.register_keyword_intent("lights_on", ["lights", "on"])
        intents.register_keyword_intent("lights_off", ["lights", "off"])
        intents.register_keyword_intent("door_open", ["door", "on"])
        intents.register_keyword_intent("door_close", ["door", "off"])
        intents.register_keyword_intent("play_music", ["play", "music"])

        self.intents = intents

    def test_all(self):
        def test_intents(utterance, expected_intents):
            res = self.intents.calc(utterance)
            self.assertEqual(set([i["intent_type"] for i in res]),
                             set(expected_intents))

        test_intents("turn off the lights, open the door",
                     {'door_open', 'lights_off'})
        test_intents("Call mom and tell her hello",
                     {})
        test_intents("tell me a joke and the weather",
                     {'joke', 'weather'})
        test_intents("turn on the lights close the door",
                     {})
        test_intents("close the pod bay doors play some music",
                     {})
        test_intents("play the music satan and friends",
                     {'play_music'})
        test_intents(
            "tell me a joke and order some pizza and turn on the lights and close the door and play some songs",
            {'play_music', 'lights_on', 'door_close', 'joke'})

    def test_engines(self):
        def test_engines(utterance, expected_engines):
            res = self.intents.calc(utterance)
            self.assertEqual(set([i["intent_engine"] for i in res]),
                             set(expected_engines))

        test_engines("turn off the lights, open the door",
                     {'adapt'})
        test_engines("Call mom and tell her hello",
                     {})
        test_engines("tell me a joke and the weather",
                     {'adapt'})
        test_engines("turn on the lights close the door", {})
        test_engines("close the pod bay doors play some music", {})
        test_engines("play the music satan and friends", {'adapt'})
        test_engines(
            "tell me a joke and order some pizza and turn on the lights and close the door and play some songs",
            {'adapt'})


class TestNebulento(unittest.TestCase):
    def setUp(self) -> None:
        config = {
            "engines": {"nebulento": {"enabled": True},
                        "adapt": {"enabled": False},
                        "palavreado": {"enabled": False},
                        "padacioso": {"enabled": False},
                        "padaos": {"enabled": False},
                        "padatious": {"enabled": False}}
        }
        intents = IntentBox(config=config,
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

        intents.register_keyword_intent("weather", ["weather"])
        intents.register_keyword_intent("hello", ["hello"])
        intents.register_keyword_intent("name", ["name"])
        intents.register_keyword_intent("joke", ["joke"], ["say"])
        intents.register_keyword_intent("lights_on", ["lights", "on"])
        intents.register_keyword_intent("lights_off", ["lights", "off"])
        intents.register_keyword_intent("door_open", ["door", "on"])
        intents.register_keyword_intent("door_close", ["door", "off"])
        intents.register_keyword_intent("play_music", ["play", "music"])

        self.intents = intents

    def test_all(self):
        def test_intents(utterance, expected_intents):
            res = self.intents.calc(utterance)
            self.assertEqual(set([i["intent_type"] for i in res]),
                             set(expected_intents))

        test_intents("turn off the lights, open the door",
                     {'lights_off'})
        test_intents("Call mom and tell her hello",
                     {})
        test_intents("tell me a joke and the weather",
                     {'joke', 'weather'})
        test_intents("turn on the lights close the door",
                     {'lights_on'})
        test_intents("close the pod bay doors play some music", {})
        test_intents("play the music satan and friends", {})
        test_intents(
            "tell me a joke and order some pizza and turn on the lights and close the door and play some songs",
            {'lights_on', 'play_music', 'joke'})

    def test_engines(self):
        def test_engines(utterance, expected_engines):
            res = self.intents.calc(utterance)
            self.assertEqual(set([i["intent_engine"] for i in res]),
                             set(expected_engines))

        test_engines("turn off the lights, open the door",
                     {'nebulento'})
        test_engines("Call mom and tell her hello",
                     {})
        test_engines("tell me a joke and the weather",
                     {'nebulento'})
        test_engines("turn on the lights close the door",
                     {'nebulento'})
        test_engines("close the pod bay doors play some music", {})
        test_engines("play the music satan and friends", {})
        test_engines(
            "tell me a joke and order some pizza and turn on the lights and close the door and play some songs",
            {"nebulento"})
