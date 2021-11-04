from intentBox.parsers.template import IntentExtractor
from intentBox.utils import LOG, normalize, get_utterance_remainder
from adapt.intent import IntentBuilder
from adapt.engine import IntentDeterminationEngine


class AdaptExtractor(IntentExtractor):
    keyword_based = True
    regex_entity_support = True

    def __init__(self, normalize=False, regex_boost=0.3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.normalize = normalize
        self.engine = IntentDeterminationEngine()
        self.regex_boost = regex_boost

    def register_entity(self, entity_name, samples=None):
        samples = samples or [entity_name]
        for kw in samples:
            self.engine.register_entity(kw, entity_name)
        super().register_entity(entity_name, samples)

    def register_regex_entity(self, entity_name, samples):
        super().register_regex_entity(entity_name, samples)
        if isinstance(samples, str):
            samples = [samples]
        for s in samples:
            self.engine.register_regex_entity(s)

    def register_regex_intent(self, intent_name, samples):
        self.register_regex_entity(intent_name + "_adapt_rx", samples)
        self.register_intent(intent_name, [intent_name + "_adapt_rx"])

    def register_intent(self, intent_name, samples=None,
                        optional_samples=None, rx_samples=None):
        """

        :param intent_name: intent_name
        :param samples: list of required registered entities (names)
        :param optional_samples: list of optional registered samples (names)
        :return:
        """
        super().register_intent(intent_name, samples)
        if not samples:
            samples = [intent_name]
            self.register_entity(intent_name, samples)
        optional_samples = optional_samples or []

        # structure intent
        intent = IntentBuilder(intent_name)
        for kw in samples:
            intent.require(kw)
        for kw in optional_samples:
            intent.optionally(kw)
        self.engine.register_intent_parser(intent.build())
        return intent

    def calc_intent(self, utterance):
        LOG.debug("Calc_intent was just run.")
        utterance = utterance.strip()
        if self.normalize:
            utterance = normalize(utterance, self.lang, True)
        for intent in self.engine.determine_intent(utterance, 100,
                                                   include_tags=True,
                                                   context_manager=self.context_manager):
            if intent and intent.get('confidence') > 0:
                intent.pop("target")
                matches = {k: v for k, v in intent.items() if
                           k not in ["intent_type", "confidence", "__tags__"]}
                intent["entities"] = {}
                for k in matches:
                    intent["entities"][k] = intent.pop(k)
                intent["conf"] = intent.pop("confidence")
                intent["utterance"] = utterance
                intent["intent_engine"] = "adapt"

                remainder = get_utterance_remainder(
                    utterance, samples=[v for v in matches.values()])
                intent["utterance_remainder"] = remainder

                # HACK adapt is notorious for handling regex poorly
                # we really need to artificially boost its confidence or
                # nothing will match
                if any(k in matches for k in self.regexes):
                    intent["conf"] += self.regex_boost

                return intent
        return {"conf": 0, "intent_type": "unknown", "entities": {},
                "utterance_remainder": utterance,
                "utterance": utterance, "intent_engine": "adapt"}

    def calc_intents(self, utterance):
        print("Calc_intents was just run.")
        LOG.debug("Calc_intents was just run.")
        bucket = {}
        for ut in self.segmenter.segment(utterance):
            intent = self.calc_intent(ut)
            if intent["conf"] < self.CONFIDENCE_FLOOR_VALUE:
                bucket[ut] = None
            else:
                bucket[ut] = intent
        return bucket

    def calc_intents_list(self, utterance):
        print("Calc_intents_list was just run.")
        LOG.debug("Calc_intents_list was just run.")
        utterance = utterance.strip()  # spaces should not mess with exact matches
        bucket = {}
        for ut in self.segmenter.segment(utterance):

            if self.normalize:
                ut = normalize(ut, self.lang, True)
            bucket[ut] = []
            for intent in self.engine.determine_intent(ut, 100,
                                                       include_tags=True,
                                                       context_manager=self.context_manager):
                if intent:
                    intent.pop("target")
                    matches = {k: v for k, v in intent.items() if
                               k not in ["intent_type", "confidence",
                                         "__tags__"]}
                    intent["entities"] = {}
                    for k in matches:
                        intent["entities"][k] = intent.pop(k)
                    intent["conf"] = intent.pop("confidence")
                    intent["utterance"] = ut
                    intent["intent_engine"] = "adapt"
                    remainder = get_utterance_remainder(
                        utterance, samples=[v for v in matches.values()])
                    intent["utterance_remainder"] = remainder
                    if intent["conf"] >= self.CONFIDENCE_FLOOR_VALUE:
                        bucket[ut] += [intent]

        return bucket

    def intent_scores(self, utterance):
        utterance = utterance.strip()  # spaces should not mess with exact matches
        bucket = []
        for intent in self.engine.determine_intent(utterance, 100,
                                                   include_tags=True,
                                                   context_manager=self.context_manager):
            if intent:
                intent.pop("target")
                matches = {k: v for k, v in intent.items() if
                           k not in ["intent_type", "confidence", "__tags__"]}
                intent["entities"] = {}
                for k in matches:
                    intent["entities"][k] = intent.pop(k)
                intent["conf"] = intent.pop("confidence")
                intent["intent_engine"] = "adapt"
                intent["utterance"] = utterance

                remainder = get_utterance_remainder(
                    utterance, samples=[v for v in matches.values()])
                intent["utterance_remainder"] = remainder
                bucket += [intent]
        return bucket

    def intent_remainder(self, utterance, _prev=""):
        utterance = utterance.strip()  # spaces should not mess with exact matches
        if self.normalize:
            utterance = normalize(utterance, self.lang, True)
        return IntentExtractor.intent_remainder(self, utterance)

    def intents_remainder(self, utterance):
        """
        segment utterance and for each chunk recursively check for intents in utterance remainer

        :param utterance:
        :return:
        """
        utterance = utterance.strip()  # spaces should not mess with exact matches
        bucket = {}
        for utterance in self.segmenter.segment(utterance):
            if self.normalize:
                utterance = normalize(utterance, self.lang, True)
            bucket[utterance] = self.intent_remainder(utterance)
        return bucket

    def segment(self, text):
        if self.normalize:
            text = normalize(text, self.lang, True)
        return self.segment(text)

    def detach_intent(self, intent_name):
        LOG.debug("detaching adapt intent: " + intent_name)
        new_parsers = [
            p for p in self.engine.intent_parsers if p.name != intent_name]
        self.engine.intent_parsers = new_parsers

    def detach_skill(self, skill_id):
        LOG.debug("detaching adapt skill: " + skill_id)
        new_parsers = [
            p.name for p in self.engine.intent_parsers if
            p.name.startswith(skill_id)]
        for intent_name in new_parsers:
            self.detach_intent(intent_name)

    def manifest(self):
        # TODO vocab, skill ids, intent_data
        return {
            "intent_names": [p.name for p in self.engine.intent_parsers]
        }


if __name__ == "__main__":
    from pprint import pprint

    intents = AdaptExtractor()

    weather = ["weather"]
    hello = ["hey", "hello", "hi", "greetings"]
    name = ["name is"]
    joke = ["joke"]
    play = ["play"]
    say = ["say", "tell"]
    music = ["music", "jazz", "metal", "rock"]
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

    intents.register_intent("weather", ["weather"], ["say"])
    intents.register_intent("hello", ["hello"])
    intents.register_intent("name", ["name"])
    intents.register_intent("joke", ["joke"], ["say"])
    intents.register_intent("lights_on", ["lights", "on"])
    intents.register_intent("lights_off", ["lights", "off"])
    intents.register_intent("door_open", ["door", "on"])
    intents.register_intent("door_close", ["door", "off"])
    intents.register_intent("play_music", ["play", "music"])

    sentences = [
        "tell me a joke and say hello",
        "turn off the lights, open the door",
        "nice work! get me a beer",
        "Call mom tell her hello",
        "tell me a joke and the weather",
        "turn on the lights close the door",
        "close the door turn off the lights",
        "tell me a joke order some pizza",  # fail
        "close the pod bay doors play some music"  # fail
    ]

    print("CALCULATE SINGLE INTENT")
    for sent in sentences:
        print("UTTERANCE:", sent)
        pprint(intents.calc_intent(sent))
        print("_______________________________")

    print("CALCULATE MAIN AND SECONDARY INTENTS")
    for sent in sentences:
        print("UTTERANCE:", sent)
        pprint(intents.intent_remainder(sent))
        print("_______________________________")

    print("SEGMENT AND CALCULATE MAIN AND SECONDARY INTENTS")
    for sent in sentences:
        print("UTTERANCE:", sent)
        pprint(intents.intents_remainder(sent))
        print("_______________________________")

    print("SEGMENT AND CALCULATE ALL INTENTS")
    for sent in sentences:
        print("UTTERANCE:", sent)
        pprint(intents.calc_intents_list(sent))
        print("_______________________________")
