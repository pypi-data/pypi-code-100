from intentBox.parsers.nebulento_extract import NebulentoExtractor
from intentBox.parsers.template import IntentExtractor
from intentBox.utils import LOG, resolve_resource_file


class IntentBox(IntentExtractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engines_config = self.config.get("engines") or {}
        # TODO plugin system for arbitrary base engines
        self.engines = {"nebulento": None, "adapt": None, "padacioso": None,
                        "padaos": None, "padatious": None, "palavreado": None}
        self.engine_weights = {"nebulento": 0.75, "adapt": 1.0,
                               "padacioso": 0.9,
                               "padaos": 1.0, "padatious": 0.8,
                               "palavreado": 0.8}
        self._load_engines()

    def _load_engines(self):
        nebulento_config = self.engines_config.get("nebulento") or {}
        if nebulento_config.get("enabled", True):
            self.engines["nebulento"] = NebulentoExtractor(
                config=nebulento_config)
            self.engine_weights["nebulento"] = nebulento_config.get("weight",
                                                                    0.7)

        adapt_config = self.engines_config.get("adapt") or {}
        if adapt_config.get("enabled", True):
            from intentBox.parsers.adapt_extract import AdaptExtractor
            self.engines["adapt"] = AdaptExtractor(config=adapt_config)
            self.engine_weights["adapt"] = adapt_config.get("weight", 1.0)

        palavreado_config = self.engines_config.get("palavreado") or {}
        if palavreado_config.get("enabled", False):
            from intentBox.parsers.palavreado_extract import \
                PalavreadoExtractor
            self.engines["palavreado"] = PalavreadoExtractor(
                config=palavreado_config)
            self.engine_weights["palavreado"] = adapt_config.get("weight", 0.8)

        padaos_config = self.engines_config.get("padaos") or {}
        if padaos_config.get("enabled", False):
            from intentBox.parsers.padaos_extract import PadaosExtractor
            self.engines["padaos"] = PadaosExtractor(config=padaos_config)
            self.engine_weights["padaos"] = padaos_config.get("weight", 1.0)

        padacioso_config = self.engines_config.get("padacioso") or {}
        if padacioso_config.get("enabled", True):
            from intentBox.parsers.padacioso_extract import PadaciosoExtractor
            self.engines["padacioso"] = PadaciosoExtractor(
                config=padacioso_config)
            self.engine_weights["padacioso"] = padacioso_config.get("weight",
                                                                    0.9)

        padatious_config = self.engines_config.get("padatious") or {}
        if padatious_config.get("enabled", False):
            from intentBox.parsers.padatious_extract import PadatiousExtractor
            self.engines["padatious"] = PadatiousExtractor(
                config=padatious_config)
            self.engine_weights["padatious"] = padatious_config.get("weight",
                                                                    0.95)

    # intentBox interface
    def register_intent(self, intent_name, samples=None):
        for parser, engine in self.engines.items():
            if not engine or engine.keyword_based:
                continue
            self.engines[parser].register_intent(intent_name, samples)

    def register_intent_from_file(self, intent_name, file_name):
        with open(file_name) as f:
            samples = [l.strip() for l in f.readlines() if
                       l.strip() and not l.startswith(
                           "#") and not l.startswith("//")]
        if file_name.endswith(".voc") or file_name.endswith(".entity"):
            self.register_keyword_intent(intent_name, samples)
        elif file_name.endswith(".rx"):
            self.register_regex_intent(intent_name, samples)
        else:
            self.register_intent(intent_name, samples)

    def register_entity(self, entity_name, samples=None):
        for parser, engine in self.engines.items():
            if not engine:
                continue
            self.engines[parser].register_entity(entity_name, samples)

    def register_regex_entity(self, entity_name, samples):
        for parser, engine in self.engines.items():
            if not engine or not engine.regex_entity_support:
                continue
            self.engines[parser].register_regex_entity(entity_name,
                                                       samples)

    def register_entity_from_file(self, entity_name, file_name):
        with open(file_name) as f:
            samples = [l.strip() for l in f.readlines() if
                       l.strip() and not l.startswith(
                           "#") and not l.startswith("//")]
        if file_name.endswith(".rx"):
            self.register_regex_entity(entity_name, samples)
        else:
            self.register_entity(entity_name, samples)

    def register_regex_entity_from_file(self, entity_name, file_name):
        with open(file_name) as f:
            samples = [l.strip() for l in f.readlines() if
                       l.strip() and not l.startswith(
                           "#") and not l.startswith("//")]
        self.register_regex_entity(entity_name, samples)

    def register_keyword_intent(self, intent_name, samples=None,
                                optional_samples=None):
        LOG.info("Registering keyword intent: " + intent_name)
        for parser, engine in self.engines.items():
            if not engine or not engine.keyword_based:
                continue
            self.engines[parser].register_intent(intent_name,
                                                 samples,
                                                 optional_samples)

    def register_keyword_intent_from_file(self, intent_name, file_name):
        LOG.info("Registering keyword intent file: " + file_name)
        with open(file_name) as f:
            samples = [l.strip() for l in f.readlines() if
                       l.strip() and not l.startswith(
                           "#") and not l.startswith("//")]
        self.register_keyword_intent(intent_name, samples)

    def register_regex_intent(self, intent_name, samples=None):
        self.register_regex_entity(intent_name, samples)
        for parser, engine in self.engines.items():
            if not engine or not engine.regex_entity_support:
                continue
            self.engines[parser].register_regex_intent(intent_name,
                                                       samples)

    def register_regex_intent_from_file(self, intent_name, file_name):
        with open(file_name) as f:
            samples = [l.strip() for l in f.readlines() if
                       l.strip() and not l.startswith(
                           "#") and not l.startswith("//")]
        self.register_regex_intent(intent_name, samples)

    def enable_automatic_training(self):
        for k, v in self.engines.items():
            if v:
                self.engines[k].auto_train = True

    def disable_automatic_training(self):
        for k, v in self.engines.items():
            if v:
                self.engines[k].auto_train = True

    def train(self, *args, **kwargs):
        # in case engines need a training step this might be called after
        # everything loaded, avoids the need to train on every intent
        for k, v in self.engines.items():
            if v:
                self.engines[k].train(*args, **kwargs)
        return True

    def detach_intent(self, intent_name):
        super().detach_intent(intent_name)
        for k, v in self.engines.items():
            if v:
                self.engines[k].detach_intent(intent_name)

    def detach_skill(self, skill_id):
        super().detach_skill(skill_id)
        for k, v in self.engines.items():
            if v:
                self.engines[k].detach_skill(skill_id)

    # context handling
    def add_context(self, entity):
        for k in self.engines:
            self.engines[k].context_manager.inject_context(entity)

    def remove_context(self, context):
        for k in self.engines:
            self.engines[k].context_manager.remove_context(context)

    def clear_context(self):
        """ Clears all keywords from context """
        for k in self.engines:
            self.engines[k].context_manager.clear_context()

    # intent handling
    def calc_intent(self, utterance):
        utterance = utterance.strip().lower()
        # best intent
        intents = []
        for parser, engine in self.engines.items():
            if engine:
                intent = engine.calc_intent(utterance)
                LOG.debug(f"{parser} match: {intent}")
                intents.append(intent)
        intents = self.normalize_intent_scores(intents)
        intents = [i for i in intents if i["conf"] >= self.CONFIDENCE_FLOOR_VALUE]
        if not intents:
            return None
        return sorted(intents, key=lambda k: k["conf"], reverse=True)[0]

    def normalize_intent_scores(self, intents):
        for idx, intent in enumerate(intents):
            # weight down based on intent parser used
            weight = self.engine_weights[intent["intent_engine"]]
            intents[idx]["conf"] = intents[idx]["conf"] * weight
            # weight down based on length of utterance remainder
            utt = intent.get("utterance") or " "
            rem = intent.get("utterance_remainder") or utt
            ratio = len(rem) / len(utt)
            ratio = ratio * 0.1
            intents[idx]["conf"] = max(0, intents[idx]["conf"] - ratio)
        return intents

    def calc_intents(self, utterance):
        utterance = utterance.strip().lower()
        # segment + best intent per chunk
        bucket = {}
        for ut in self.segmenter.segment(utterance):
            bucket[ut] = self.calc_intent(ut)
        return bucket

    def calc_intents_list(self, utterance):
        utterance = utterance.strip().lower()
        intents = []
        for parser in self.engines:
            if not self.engines[parser]:
                continue
            intents += self.engines[parser].calc_intents_list(utterance)
        return intents

    def intent_scores(self, utterance):
        utterance = utterance.strip().lower()
        intents = []
        for parser in self.engines:
            if not self.engines[parser]:
                continue
            intents += self.engines[parser].intent_scores(utterance)
        return intents

    # engine specific interfaces
    ## Adapt
    def register_adapt_intent(self, intent_name, samples=None,
                              optional_samples=None):
        LOG.info("Registering adapt intent: " + intent_name)
        optional_samples = optional_samples or []
        if self.engines["adapt"]:
            self.engines["adapt"].register_intent(intent_name, samples,
                                                  optional_samples)

    def register_adapt_intent_from_file(self, intent_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering adapt intent file: " + file_name)
        self.register_adapt_entity_from_file(intent_name, file_name)
        self.register_adapt_intent(intent_name)

    def register_adapt_entity(self, entity_name, samples=None):
        LOG.info("Registering adapt entity: " + entity_name)
        if self.engines["adapt"]:
            self.engines["adapt"].register_entity(entity_name, samples)

    def register_adapt_entity_from_file(self, entity_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering adapt entity file: " + file_name)
        with open(file_name) as f:
            samples = [l.strip() for l in f.readlines() if
                       l.strip() and not l.startswith(
                           "#") and not l.startswith("//")]
        self.register_adapt_entity(entity_name, samples)

    def register_adapt_regex_entity(self, entity_name, regex_str):
        LOG.info("Registering adapt regex: " + regex_str)
        if self.engines["adapt"]:
            self.engines["adapt"].register_regex_entity(entity_name, regex_str)

    def register_adapt_regex_from_file(self, entity_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering adapt regex file: " + file_name)
        with open(file_name) as f:
            samples = [l.strip() for l in f.readlines() if
                       l.strip() and not l.startswith(
                           "#") and not l.startswith("//")]
        self.register_adapt_regex_entity(entity_name, samples)

    ## Palavreado
    def register_palavreado_intent(self, intent_name, samples=None,
                                   optional_samples=None):
        LOG.info("Registering palavreado intent: " + intent_name)
        optional_samples = optional_samples or []
        if self.engines["palavreado"]:
            self.engines["palavreado"].register_intent(intent_name, samples,
                                                       optional_samples)

    def register_palavreado_intent_from_file(self, intent_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering palavreado intent file: " + file_name)
        if self.engines["palavreado"]:
            with open(file_name) as f:
                samples = [l.strip() for l in f.readlines() if
                           l.strip() and not l.startswith(
                               "#") and not l.startswith("//")]
            self.engines["palavreado"].register_intent(intent_name, samples)

    def register_palavreado_entity(self, entity_name, samples=None):
        LOG.info("Registering palavreado entity: " + entity_name)
        if self.engines["palavreado"]:
            self.engines["palavreado"].register_entity(entity_name, samples)

    def register_palavreado_entity_from_file(self, entity_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering palavreado entity file: " + file_name)
        with open(file_name) as f:
            samples = [l.strip() for l in f.readlines() if
                       l.strip() and not l.startswith(
                           "#") and not l.startswith("//")]
        self.register_palavreado_entity(entity_name, samples)

    def register_palavreado_regex_entity(self, entity_name, regex_str):
        LOG.info("Registering palavreado regex: " + regex_str)
        self.engines["palavreado"].register_regex_entity(entity_name,
                                                         regex_str)

    def register_palavreado_regex_from_file(self, entity_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering palavreado regex file: " + file_name)
        with open(file_name) as f:
            samples = [l.strip() for l in f.readlines() if
                       l.strip() and not l.startswith(
                           "#") and not l.startswith("//")]
        self.register_palavreado_regex_entity(entity_name, samples)

    ## Padatious
    def register_padatious_intent(self, intent_name, samples=None):
        LOG.info("Registering padatious intent: " + intent_name)
        self.engines["padatious"].register_intent(intent_name, samples)

    def register_padatious_intent_from_file(self, intent_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering padatious intent file: " + file_name)
        self.engines["padatious"].register_intent_from_file(intent_name,
                                                            file_name)

    def register_padatious_entity(self, entity_name, samples=None):
        LOG.info("Registering padatious entity: " + entity_name)
        self.engines["padatious"].register_entity(entity_name, samples)

    def register_padatious_entity_from_file(self, entity_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering padatious entity file: " + file_name)
        try:
            self.engines["padatious"].register_entity_from_file(entity_name,
                                                                file_name)
        except Exception as e:
            LOG.error("Could not register file: " + file_name)

    ## Padaos
    def register_padaos_intent(self, intent_name, samples=None):
        LOG.info("Registering padaos intent: " + intent_name)
        self.engines["padaos"].register_intent(intent_name, samples)

    def register_padaos_intent_from_file(self, intent_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering padaos intent file: " + file_name)
        self.engines["padaos"].register_intent_from_file(intent_name,
                                                         file_name)

    def register_padaos_entity(self, entity_name, samples=None):
        LOG.info("Registering padaos entity: " + entity_name)
        self.engines["padaos"].register_entity(entity_name, samples)

    def register_padaos_entity_from_file(self, entity_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering padaos entity file: " + file_name)
        try:
            self.engines["padaos"].register_entity_from_file(entity_name,
                                                             file_name)
        except Exception as e:
            LOG.error("Could not register file: " + file_name)

    ## Padacioso
    def register_padacioso_intent(self, intent_name, samples=None):
        LOG.info("Registering padacioso intent: " + intent_name)
        self.engines["padacioso"].register_intent(intent_name, samples)

    def register_padacioso_intent_from_file(self, intent_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering padacioso intent file: " + file_name)
        self.engines["padacioso"].register_intent_from_file(intent_name,
                                                            file_name)

    def register_padacioso_entity(self, entity_name, samples=None):
        LOG.info("Registering padacioso entity: " + entity_name)
        self.engines["padacioso"].register_entity(entity_name, samples)

    def register_padacioso_entity_from_file(self, entity_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering padacioso entity file: " + file_name)
        try:
            self.engines["padacioso"].register_entity_from_file(entity_name,
                                                                file_name)
        except Exception as e:
            LOG.error("Could not register file: " + file_name)

    ## nebulento
    def register_nebulento_intent(self, intent_name, samples=None):
        LOG.info("Registering nebulento intent: " + intent_name)
        self.engines["nebulento"].register_intent(intent_name, samples)

    def register_nebulento_intent_from_file(self, intent_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering nebulento intent file: " + file_name)
        self.engines["nebulento"].register_intent_from_file(intent_name,
                                                            file_name)

    def register_nebulento_entity(self, entity_name, samples=None):
        LOG.info("Registering nebulento entity: " + entity_name)
        self.engines["nebulento"].register_entity(entity_name, samples)

    def register_nebulento_entity_from_file(self, entity_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering nebulento entity file: " + file_name)
        try:
            self.engines["nebulento"].register_entity_from_file(entity_name,
                                                                file_name)
        except Exception as e:
            LOG.error("Could not register file: " + file_name)
