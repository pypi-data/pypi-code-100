import re
from mammut.common.lexicon.inflection_rule import InflectionRule
from mammut.common.storage.storage_manager import StorageManager


class ParadigmProducer:
    REUSE_PARADIGM_CMD_NAME_REGEX = re.compile(
        f"^<({InflectionRule.PARADIGM_NAME_REGEX_STR}\:)?{InflectionRule.PARADIGM_NAME_REGEX_STR}>$"
    )

    def __init__(
        self, word_model: str, grammar: str, hidden: bool, descriptions: {}, group
    ):
        from mammut.common.lexicon.pos import POSdescriptor
        self.word_model = word_model
        self.grammar = grammar
        self.hidden = hidden
        self.descriptions = descriptions
        self.group = group
        self.inflection_rules = []
        for rr in self.grammar.split("|"):
            rrs = rr.strip()
            if ParadigmProducer.REUSE_PARADIGM_CMD_NAME_REGEX.match(rrs) != None:
                name_parts = rrs.strip("<>").split(":")
                word_model_to_reuse = ""
                group_to_look = None
                if len(name_parts) == 1:
                    word_model_to_reuse = name_parts[0]
                    group_to_look = self.group
                else:
                    word_model_to_reuse = name_parts[1]
                    group_to_look = POSdescriptor.SHEETS_LOADED[name_parts[0]]
                rules_to_reuse = group_to_look.producers[
                    word_model_to_reuse
                ].inflection_rules
                self.inflection_rules = self.inflection_rules + rules_to_reuse
            else:
                self.inflection_rules.append(InflectionRule(rrs, self))

    def apply(self, lemma: str) -> []:
        res = []
        for r in self.inflection_rules:
            res.append(r.apply(lemma))
        return res


class ParadigmProducerGroup:
    DEFAULT_START_CELL = "A1"
    DEFAULT_START_COLUMN = "A"
    DEFAULT_START_ROW = "1"
    DEFAULT_END_CELL = "L503"
    DEFAULT_END_COLUMN = "L"
    storage_manager = StorageManager()
    WORD_MODEL_COLUMN_NAME = "word-model"
    GRAMMAR_COLUMN_NAME = "grammar"
    HIDDEN_COLUMN_NAME = "hidden"
    DESCRIPTION_COLUMN_NAME_PREFIX = "description-"

    def __init__(self, sheet_title: str, standard, regional_setting):
        self.sheet_title = sheet_title
        self.standard = standard
        self.regional_setting = regional_setting
        self.producers = {}
        self.feature_classes = []
        if self.sheet_title:
            self.range_name = (
                self.sheet_title + "!" + ParadigmProducerGroup.DEFAULT_START_CELL
            )
            self.data_frame = self.storage_manager.get_spreadsheet_as_dataframe(
                self.standard.spreadsheet_id,
                self.sheet_title,
                self.DEFAULT_START_COLUMN,
                self.DEFAULT_START_ROW,
                self.DEFAULT_END_COLUMN,
            )
            if self.data_frame is not None:
                desc_col_names = []
                for dc in self.data_frame.keys():
                    if dc.startswith(
                        ParadigmProducerGroup.DESCRIPTION_COLUMN_NAME_PREFIX
                    ):
                        desc_col_names.append(dc)
                        desc_name = dc[
                            len(ParadigmProducerGroup.DESCRIPTION_COLUMN_NAME_PREFIX):
                        ]
                        self.feature_classes.append(desc_name)
                for r in self.data_frame.iterrows():
                    descriptions = {}
                    for dc in desc_col_names:
                        desc_name = dc[
                            len(ParadigmProducerGroup.DESCRIPTION_COLUMN_NAME_PREFIX):
                        ]
                        descriptions[desc_name] = r[1][dc]
                    par_prod = ParadigmProducer(
                        r[1][ParadigmProducerGroup.WORD_MODEL_COLUMN_NAME],
                        r[1][ParadigmProducerGroup.GRAMMAR_COLUMN_NAME],
                        r[1][ParadigmProducerGroup.HIDDEN_COLUMN_NAME],
                        descriptions,
                        self,
                    )
                    self.producers[par_prod.word_model] = par_prod

    def get_producers(self):
        return filter(lambda p: not p.hidden, self.producers.keys())
