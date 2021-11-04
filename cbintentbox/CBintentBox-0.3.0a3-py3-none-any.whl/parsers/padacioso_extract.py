from intentBox.parsers.template import IntentExtractor
from padacioso import IntentContainer
from intentBox.utils import LOG, get_utterance_remainder


class PadaciosoExtractor(IntentExtractor):
    keyword_based = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = IntentContainer()
        self.registered_intents = []

    def detach_intent(self, intent_name):
        if intent_name in self.registered_intents:
            LOG.debug("Detaching padacioso intent: " + intent_name)
            self.container.remove_intent(intent_name)
            self.registered_intents.remove(intent_name)

    def detach_skill(self, skill_id):
        LOG.debug("Detaching padacioso skill: " + str(skill_id))
        remove_list = [i for i in self.registered_intents if skill_id in i]
        for i in remove_list:
            self.detach_intent(i)

    def register_entity(self, entity_name, samples=None):
        samples = samples or [entity_name]
        self.container.add_entity(entity_name, samples)

    def register_intent(self, intent_name, samples=None):
        samples = samples or [intent_name]
        if intent_name not in self._intent_samples:
            self._intent_samples[intent_name] = samples
        else:
            self._intent_samples[intent_name] += samples
        self.container.add_intent(intent_name, samples)
        self.registered_intents.append(intent_name)

    def register_entity_from_file(self, entity_name, file_name):
        with open(file_name) as f:
            samples = f.read().split("\n")
        self.register_entity(entity_name, samples)

    def register_intent_from_file(self, intent_name, file_name):
        with open(file_name) as f:
            samples = f.read().split("\n")
        self.register_intent(intent_name, samples)

    def calc_intent(self, utterance, min_conf=0.5):
        utterance = utterance.strip().lower()
        intent = self.container.calc_intent(utterance)
        if intent["name"]:
            remainder = get_utterance_remainder(
                utterance, samples=self.intent_samples[intent["name"]])
            intent["intent_engine"] = "padacioso"
            intent["intent_type"] = intent.pop("name")
            intent["utterance"] = utterance
            intent["utterance_remainder"] = remainder
            entity_text = "".join(v for v in intent["entities"].values())
            if len(intent["entities"]):
                ratio = len(entity_text) / len(utterance) / len(intent["entities"])
            else:
                ratio = len(entity_text) / len(utterance)
            ratio += 0.01
            ratio = ratio / len(self.segmenter.segment(utterance))
            intent["conf"] = 1 - ratio
            return intent
        return {'conf': 0,
                'intent_type': 'unknown',
                'entities': {},
                'utterance': utterance,
                'utterance_remainder': utterance,
                'intent_engine': 'padacioso'}

    def intent_scores(self, utterance):
        utterance = utterance.strip().lower()
        intents = []
        bucket = self.calc_intents(utterance)
        for utt in bucket:
            intent = bucket[utt]
            if not intent:
                continue
            intents.append(intent)
        return intents

    def calc_intents(self, utterance, min_conf=0.5):
        utterance = utterance.strip().lower()
        bucket = {}
        for ut in self.segmenter.segment(utterance):
            intent = self.calc_intent(ut)
            bucket[ut] = intent
        return bucket

    def calc_intents_list(self, utterance):
        utterance = utterance.strip().lower()
        bucket = {}
        for ut in self.segmenter.segment(utterance):
            bucket[ut] = self.filter_intents(ut)
        return bucket

    def manifest(self):
        # TODO vocab, skill ids, intent_data
        return {
            "intent_names": self.registered_intents
        }
