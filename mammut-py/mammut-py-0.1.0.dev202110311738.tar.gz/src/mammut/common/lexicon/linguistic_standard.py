from collections import namedtuple, defaultdict
from mammut.common.storage.storage_manager import StorageManager
from mammut.common.lexicon.feature import FeatureDescriptor
import mammut.common.lexicon.dictionary
from mammut.common.lexicon.pos import POSdescriptor
from mammut.common.lexicon.mammut_brat_configuration import (
    MammutBratConfiguration,
)
from mammut.common.lexicon.functional import FunctionalLemmaDescriptor
from mammut.common.lexicon.non_functional import NonFunctionalLemmaDescriptor
from mammut.common.lexicon.inflection_rule import InflectionRule
import pandas as pd

InVocabulary = namedtuple(
    "InVocabulary",
    [
        "value",
        "list",
        "description",
        "details",
        "base_value",
        "base_list",
        "base_description",
    ],
)


class LinguisticStandard:
    REGIONAL_SETTINGS_LEMMA_LIST_COLUMN_NAME = "regional-settings-lemma-list"
    REGIONAL_SETTINGS_DEFINITION_LIST_COLUMN_NAME = (
        "regional-settings-definition-list"
    )
    WORD_TYPE_LIST_COLUMN_NAME = "word-type-list"

    FEATURE_CLASS_GROUP_COLUMN_NAME = "feature-class-group"
    FEATURE_CLASS_COLUMN_NAME = "feature-class"
    FEATURE_NAME_COLUMN_NAME = "feature-name"
    FEATURE_ID_COLUMN_NAME = "feature-id"
    POS_TAGS_COLUMN_NAME = "pos-tags"
    DOCUMENTATION_LINK_COLUMN_NAME = "documentation-link"
    STATISTICS_LINK_COLUMN_NAME = "statistics-link"

    SOURCE_ID_COLUMN_NAME = "source-id"
    SOURCE_URL_PATTERN_COLUMN_NAME = "source-url-pattern"
    HTML_WRAPPER_COLUMN_NAME = "html-wrapper"
    REGIONAL_SETTINGS_COLUMN_NAME = "regional-settings"

    DEFAULT_START_CELL = "A1"
    DEFAULT_START_COLUMN = "A"
    DEFAULT_START_ROW = "1"
    DEFAULT_END_CELL = "M"

    def __init__(
        self,
        spreadsheet_id: str,
        base_sheet_title: str,
        dict_sources_sheet_title: str,
        pos_sheet_title: str,
        features_sheet_title: str,
        dimensiones_sheet_title: str,
        functionals_sheet_title: str,
        non_functionals_sheet_title: str,
        tokenizer,
        primes_sheet_title,
        synonym_sheet_title: str,
    ):
        self.valid = True
        self.errors = []
        self.spreadsheet_id = spreadsheet_id
        self.base_sheet_title = base_sheet_title
        self.dict_sources_sheet_title = dict_sources_sheet_title
        self.pos_sheet_title = pos_sheet_title
        self.features_sheet_title = features_sheet_title
        self.dimensiones_sheet_title = dimensiones_sheet_title
        self.functionals_sheet_title = functionals_sheet_title
        self.non_functionals_sheet_title = non_functionals_sheet_title
        self.tokenizer = tokenizer
        self.primes_sheet_title = primes_sheet_title
        self.synonym_sheet_title = synonym_sheet_title
        self.regional_settings_lemma_list = []
        self.regional_settings_definition_list = []
        self.word_type_list = []
        self.pos_descriptor_list = {}
        self.pos_descriptor_classes = defaultdict(list)
        self.pos_annotation_shifts = defaultdict(list)
        self.feature_descriptor_list = {}
        self.feature_descriptor_by_pos_tag = {}
        self.all_feature_descriptor_by_pos_tag = defaultdict(list)
        self.dimensiones_descriptor_list = {}
        self.morpheme_paradigms = {}
        self.misspelling_paradigms = {}
        self.feature_paradigms = {}
        self.external_dictionary_sources = {}
        # Contains FunctionalLemmaDescriptor indexed by lemma, regional setting and pos concatanated by "-"
        self.functionals = {}
        self.functionals_implicit = {}
        self.functionals_by_regional_settings_lemma = {}
        self.functionals_by_regional_settings_lemma_implicit = {}
        self.undefined_functionals = {}
        self.non_functionals = {}
        self.base_range_name = (
            self.base_sheet_title + "!" + LinguisticStandard.DEFAULT_START_CELL
        )
        self.pos_range_name = (
            self.pos_sheet_title + "!" + LinguisticStandard.DEFAULT_START_CELL
        )
        # Load dimensions of annotation.
        self.dimensiones_range_name = (
                self.dimensiones_sheet_title
                + "!"
                + LinguisticStandard.DEFAULT_START_CELL
        )
        self.storage_manager = StorageManager()
        self.load_base_dataframe()
        self.load_features_dataframe()
        self.load_dictionary_dataframe()
        self.load_pos_dataframe()
        self.load_dimensions_dataframe()
        self.load_functionals_dataframe()
        self.load_non_functionals_dataframe()
        self.working_dictionary = None

    def load_base_dataframe(self):
        self.base_data_frame = self.storage_manager.get_spreadsheet_as_dataframe(
            self.spreadsheet_id,
            self.base_sheet_title,
            self.DEFAULT_START_COLUMN,
            self.DEFAULT_START_ROW,
            self.DEFAULT_END_CELL,
        )

        if self.base_data_frame is not None:
            for rsl in self.base_data_frame[
                LinguisticStandard.REGIONAL_SETTINGS_LEMMA_LIST_COLUMN_NAME
            ]:
                self.regional_settings_lemma_list.append(rsl)
            for rsd in self.base_data_frame[
                LinguisticStandard.REGIONAL_SETTINGS_DEFINITION_LIST_COLUMN_NAME
            ]:
                self.regional_settings_definition_list.append(rsd)
            for wt in self.base_data_frame[
                LinguisticStandard.WORD_TYPE_LIST_COLUMN_NAME
            ]:
                self.word_type_list.append(wt)
        else:
            self.valid = False
            self.errors.append(f"The base sheet is not present.")
        self.features_range_name = (
                self.features_sheet_title
                + "!"
                + LinguisticStandard.DEFAULT_START_CELL
        )

    def load_features_dataframe(self):
        self.features_data_frame = self.storage_manager.get_spreadsheet_as_dataframe(
            self.spreadsheet_id,
            self.features_sheet_title,
            LinguisticStandard.DEFAULT_START_COLUMN,
            LinguisticStandard.DEFAULT_START_ROW,
            LinguisticStandard.DEFAULT_END_CELL,
        )

        if self.features_data_frame is not None:
            for r in self.features_data_frame.iterrows():
                fet_desc = FeatureDescriptor(
                    r[1][LinguisticStandard.FEATURE_CLASS_GROUP_COLUMN_NAME],
                    r[1][LinguisticStandard.FEATURE_CLASS_COLUMN_NAME],
                    r[1][LinguisticStandard.FEATURE_NAME_COLUMN_NAME],
                    r[1][LinguisticStandard.FEATURE_ID_COLUMN_NAME],
                    r[1][LinguisticStandard.POS_TAGS_COLUMN_NAME],
                    r[1][LinguisticStandard.DOCUMENTATION_LINK_COLUMN_NAME],
                    r[1][LinguisticStandard.STATISTICS_LINK_COLUMN_NAME],
                    self,
                )
                self.feature_descriptor_list[fet_desc.feature_id] = fet_desc
        else:
            self.valid = False
            self.errors.append(f"The features sheet is not present.")
        self.dict_sources_range_name = (
                self.dict_sources_sheet_title
                + "!"
                + LinguisticStandard.DEFAULT_START_CELL
        )

    def load_dictionary_dataframe(self):
        self.dict_sources_data_frame = self.storage_manager.get_spreadsheet_as_dataframe(
            self.spreadsheet_id,
            self.dict_sources_sheet_title,
            LinguisticStandard.DEFAULT_START_COLUMN,
            LinguisticStandard.DEFAULT_START_ROW,
            LinguisticStandard.DEFAULT_END_CELL,
        )

        if self.dict_sources_data_frame is not None:
            for r in self.dict_sources_data_frame.iterrows():
                ext_dic = mammut.common.lexicon.dictionary.ExternalDictionarySource(
                    r[1][LinguisticStandard.SOURCE_ID_COLUMN_NAME],
                    r[1][LinguisticStandard.SOURCE_URL_PATTERN_COLUMN_NAME],
                    r[1][LinguisticStandard.HTML_WRAPPER_COLUMN_NAME],
                    r[1][LinguisticStandard.REGIONAL_SETTINGS_COLUMN_NAME],
                    self,
                )
                self.external_dictionary_sources[ext_dic.source_id] = ext_dic
        else:
            self.valid = False
            self.errors.append(
                f"The dicttionary external sources sheet is not present."
            )

    def load_pos_dataframe(self):
        self.pos_data_frame = self.storage_manager.get_spreadsheet_as_dataframe(
            self.spreadsheet_id,
            self.pos_sheet_title,
            LinguisticStandard.DEFAULT_START_COLUMN,
            LinguisticStandard.DEFAULT_START_ROW,
            LinguisticStandard.DEFAULT_END_CELL,
        )

        if self.pos_data_frame is not None:
            for r in self.pos_data_frame.iterrows():
                pos_desc = POSdescriptor(
                    r[1][POSdescriptor.POS_CLASS_GROUP_COLUMN_NAME],
                    r[1][POSdescriptor.POS_CLASS_COLUMN_NAME],
                    r[1][POSdescriptor.POS_NAME_COLUMN_NAME],
                    r[1][POSdescriptor.POS_ID_COLUMN_NAME],
                    r[1][POSdescriptor.POS_TYPE_COLUMN_NAME],
                    r[1][POSdescriptor.MORPHEME_PARADIGMS_COLUMN_NAME],
                    r[1][POSdescriptor.MISSPELLING_PARADIGMS_COLUMN_NAME],
                    r[1][POSdescriptor.FEATURES_COLUMN_NAME],
                    r[1][POSdescriptor.REGIONAL_SETTINGS_COLUMN_NAME],
                    r[1][POSdescriptor.ARC_COLUMN_NAME],
                    r[1][POSdescriptor.POS_ABBREVIATION],
                    r[1][POSdescriptor.POS_SHIFTS],
                    self,
                )
                self.morpheme_paradigms[
                    pos_desc.id
                ] = pos_desc.morpheme_paradigms
                self.misspelling_paradigms[
                    pos_desc.id
                ] = pos_desc.misspelling_paradigms
                self.feature_paradigms[
                    pos_desc.id
                ] = pos_desc.feature_paradigms
                self.pos_descriptor_list[pos_desc.id] = pos_desc
                self.pos_descriptor_classes[pos_desc.pos_class].append(
                    pos_desc
                )
            for posd in self.pos_descriptor_list.values():
                posd.set_pos_references(self.pos_descriptor_list)
                self.pos_annotation_shifts[posd.id].append(posd.id)
            for posd in self.pos_descriptor_list.values():
                for pds_id in posd.pos_shifts_ids:
                    if posd.id not in self.pos_annotation_shifts[pds_id]:
                        self.pos_annotation_shifts[pds_id].append(posd.id)
        else:
            self.valid = False
            self.errors.append(f"The pos-tags sheet is not present.")
        for fd in self.feature_descriptor_list.values():
            for pt_id in fd.pos_tags:
                f_list = []
                if pt_id in self.feature_descriptor_by_pos_tag:
                    f_list = self.feature_descriptor_by_pos_tag[pt_id]
                else:
                    self.feature_descriptor_by_pos_tag[pt_id] = f_list
                pt = self.pos_descriptor_list[pt_id]
                for morpheme_paradigm in pt.morpheme_paradigms.values():
                    if (
                            fd.feature_class
                            not in morpheme_paradigm.feature_classes
                    ):
                        f_list.append(fd)
                self.all_feature_descriptor_by_pos_tag[pt_id].append(fd)

    def load_dimensions_dataframe(self):
        self.dimensiones_data_frame = self.storage_manager.get_spreadsheet_as_dataframe(
            self.spreadsheet_id,
            self.dimensiones_sheet_title,
            LinguisticStandard.DEFAULT_START_COLUMN,
            LinguisticStandard.DEFAULT_START_ROW,
            LinguisticStandard.DEFAULT_END_CELL,
        )

        if self.dimensiones_data_frame is not None:
            for r in self.dimensiones_data_frame.iterrows():
                func = MammutBratConfiguration(
                    r[1][
                        MammutBratConfiguration.DIMENSION_CLASS_GROUP_COLUMN_NAME
                    ],
                    r[1][MammutBratConfiguration.DIMENSION_CLASS_COLUMN_NAME],
                    r[1][MammutBratConfiguration.DIMENSION_COLUMN_NAME],
                    self,
                )
                self.dimensiones_descriptor_list[func.dimension_class] = func
        else:
            self.valid = False
            self.errors.append(f"The dimensiones sheet is not present.")

    def load_functionals_dataframe(self):
        # Load functional lemmas.
        self.functionals_range_name = (
                self.functionals_sheet_title
                + "!"
                + FunctionalLemmaDescriptor.DEFAULT_START_CELL
        )
        self.functionals_data_frame = self.storage_manager.get_spreadsheet_as_dataframe(
            self.spreadsheet_id,
            self.functionals_sheet_title,
            FunctionalLemmaDescriptor.DEFAULT_START_COLUMN,
            FunctionalLemmaDescriptor.DEFAULT_START_ROW,
            FunctionalLemmaDescriptor.DEFAULT_END_CELL,
        )

        if self.functionals_data_frame is not None:
            if (
                    FunctionalLemmaDescriptor.HIDE_COLUMN_NAME
                    in self.functionals_data_frame
            ):
                self.functionals_data_frame = self.functionals_data_frame[
                    self.functionals_data_frame[
                        FunctionalLemmaDescriptor.HIDE_COLUMN_NAME
                    ]
                    == ""
                    ]
            for r in self.functionals_data_frame.iterrows():
                func = FunctionalLemmaDescriptor(r[1], self)
                if func.is_explicit():
                    self.functionals[func.id] = func
                    functionals_by_lemma = {}
                    if (
                            func.regional_settings_lemma
                            in self.functionals_by_regional_settings_lemma
                    ):
                        functionals_by_lemma = self.functionals_by_regional_settings_lemma[
                            func.regional_settings_lemma
                        ]
                    else:
                        self.functionals_by_regional_settings_lemma[
                            func.regional_settings_lemma
                        ] = functionals_by_lemma
                    if func.lemma in functionals_by_lemma:
                        functionals_by_lemma[func.lemma].append(func)
                    else:
                        functionals_by_lemma[func.lemma] = [func]
                else:
                    self.functionals_implicit[
                        func.implicit_condition_id
                    ] = func
                    functionals_by_implicit_condition_id = {}
                    if (
                            func.regional_settings_lemma
                            in self.functionals_by_regional_settings_lemma_implicit
                    ):
                        functionals_by_implicit_condition_id = self.functionals_by_regional_settings_lemma_implicit[
                            func.regional_settings_lemma
                        ]
                    else:
                        self.functionals_by_regional_settings_lemma_implicit[
                            func.regional_settings_lemma
                        ] = functionals_by_implicit_condition_id
                    if (
                            func.implicit_condition_id
                            in functionals_by_implicit_condition_id
                    ):
                        functionals_by_implicit_condition_id[
                            func.implicit_condition_id
                        ].append(func)
                    else:
                        functionals_by_implicit_condition_id[
                            func.implicit_condition_id
                        ] = [func]
                if not func.valid:
                    self.valid = False
                    self.errors = self.errors + func.errors
                if func.undefined:
                    if (
                            func.regional_settings_lemma
                            in self.undefined_functionals
                    ):
                        self.undefined_functionals[
                            func.regional_settings_lemma
                        ].append(func)
                    else:
                        self.undefined_functionals[
                            func.regional_settings_lemma
                        ] = [func]
        else:
            self.valid = False
            self.errors.append(f"The functionals sheet is not present.")

    def load_non_functionals_dataframe(self):
        # Load non-functional lemmas.
        from mammut.common.lexicon.dictionary import Dictionary
        self.non_functionals_range_name = (
                self.non_functionals_sheet_title
                + "!"
                + FunctionalLemmaDescriptor.DEFAULT_START_CELL
        )
        self.non_functionals_data_frame = self.storage_manager.get_spreadsheet_as_dataframe(
            self.spreadsheet_id,
            self.non_functionals_sheet_title,
            FunctionalLemmaDescriptor.DEFAULT_START_COLUMN,
            FunctionalLemmaDescriptor.DEFAULT_START_ROW,
            NonFunctionalLemmaDescriptor.DEFAULT_END_CELL,
        )

        if self.non_functionals_data_frame is not None:
            non_functionals_data_frame_parts = []
            for i in range(0, self.non_functionals_data_frame.shape[1], 4):
                df_part = self.non_functionals_data_frame.iloc[:, i: i + 4]
                df_part = df_part.loc[
                          lambda df: df[FunctionalLemmaDescriptor.LEMMA_COLUMN_NAME]
                                     != "",
                          :,
                          ]
                non_functionals_data_frame_parts.append(df_part)
            self.non_functionals_data_frame = pd.concat(
                non_functionals_data_frame_parts
            )
            if (
                    NonFunctionalLemmaDescriptor.HIDE_COLUMN_NAME
                    in self.non_functionals_data_frame
            ):
                self.non_functionals_data_frame = self.non_functionals_data_frame[
                    self.non_functionals_data_frame[
                        NonFunctionalLemmaDescriptor.HIDE_COLUMN_NAME
                    ]
                    == ""
                    ]
            for r in self.non_functionals_data_frame.iterrows():
                nfunc = NonFunctionalLemmaDescriptor(r[1], self)
                if nfunc.regional_settings_lemma in self.non_functionals:
                    if (
                            nfunc.lemma
                            in self.non_functionals[nfunc.regional_settings_lemma]
                    ):
                        self.non_functionals[nfunc.regional_settings_lemma][
                            nfunc.lemma
                        ].append(nfunc.pos_paradigm)
                    else:
                        self.non_functionals[nfunc.regional_settings_lemma][
                            nfunc.lemma
                        ] = [nfunc.pos_paradigm]
                else:
                    self.non_functionals[nfunc.regional_settings_lemma] = {
                        nfunc.lemma: [nfunc.pos_paradigm]
                    }
        else:
            self.valid = False
            self.errors.append(f"The functionals sheet is not present.")
        self.base_dictionary = Dictionary(
            self.spreadsheet_id,
            self.primes_sheet_title,
            self.synonym_sheet_title,
            self.tokenizer,
            self,
            True,
        )

    def get_morpheme_paradigms(self, postag_value_id, regional_settings: str):
        res1 = []
        res2 = []
        if regional_settings not in self.morpheme_paradigms[postag_value_id]:
            regional_settings = ""
        if regional_settings in self.morpheme_paradigms[postag_value_id]:
            res1 = list(
                map(
                    lambda p: p.word_model,
                    filter(
                        lambda p: not p.hidden,
                        self.morpheme_paradigms[postag_value_id][
                            regional_settings
                        ].producers.values(),
                    ),
                )
            )
            res2 = list(
                map(
                    lambda p: p,
                    filter(
                        lambda p: not p.hidden,
                        self.morpheme_paradigms[postag_value_id][
                            regional_settings
                        ].producers.values(),
                    ),
                )
            )
        return res1, res2

    def get_misspelling_paradigms(
        self, postag_value_id, regional_settings: str
    ):
        res = []
        if (
            regional_settings
            not in self.misspelling_paradigms[postag_value_id]
        ):
            regional_settings = ""
        if regional_settings in self.misspelling_paradigms[postag_value_id]:
            res = list(
                map(
                    lambda p: p.word_model,
                    filter(
                        lambda p: not p.hidden,
                        self.misspelling_paradigms[postag_value_id][
                            regional_settings
                        ].producers.values(),
                    ),
                )
            )
        return res

    def get_feature_paradigms(self, postag_value_id, regional_settings: str):
        res = []
        if regional_settings not in self.feature_paradigms[postag_value_id]:
            regional_settings = ""
        if regional_settings in self.feature_paradigms[postag_value_id]:
            res = list(
                map(
                    lambda p: p.word_model,
                    filter(
                        lambda p: not p.hidden,
                        self.feature_paradigms[postag_value_id][
                            regional_settings
                        ].producers.values(),
                    ),
                )
            )
        return res

    def get_morphemes(
        self, pos_id: str, word_model: str, lemma: str, regional_settings: str
    ):
        ret = []
        lemma = lemma.lower()
        if pos_id in self.morpheme_paradigms:
            if regional_settings in self.morpheme_paradigms[pos_id]:
                pos_parad = self.morpheme_paradigms[pos_id][
                    regional_settings
                ].producers
                if word_model in pos_parad:
                    ret = pos_parad[word_model].apply(lemma)
        if len(ret) == 0:
            ret.append(
                InflectionRule.Morpheme(lemma, [], regional_settings, [], [])
            )
        return ret

    def get_misspelling(
        self, pos_id: str, word_model: str, lemma: str, regional_settings: str
    ):
        ret = []
        lemma = lemma.lower()
        if pos_id in self.misspelling_paradigms:
            pos_parad = self.misspelling_paradigms[pos_id][
                regional_settings
            ].producers
            if word_model in pos_parad:
                ret = pos_parad[word_model].apply(lemma)
        return ret

    def get_other_inflections(
        self, pos_id: str, word_model: str, lemma: str, regional_settings: str
    ):
        ret = []
        lemma = lemma.lower()
        if pos_id in self.feature_paradigms:
            pos_parad = self.feature_paradigms[pos_id][
                regional_settings
            ].producers
            if word_model in pos_parad:
                ret = pos_parad[word_model].apply(lemma)
        return ret

    def get_annotation_dimension_class(self, dimension):
        return self.dimensiones_descriptor_list[dimension]

    def get_functional_lemma_descriptor(
        self, lemma: str, regional_settings_lemma: str, pos_paradigm: str
    ):
        f_id = FunctionalLemmaDescriptor.build_id(
            lemma, regional_settings_lemma, pos_paradigm
        )
        res = None
        if f_id in self.functionals:
            res = self.functionals[f_id]
        return res

    def get_implicit_functional_lemma_descriptor(
        self,
        feature_class: str,
        feature_id: str,
        feature_pos: str,
        regional_settings_lemma: str,
    ):
        f_id = FunctionalLemmaDescriptor.build_implicit_condition_id(
            feature_class, feature_id, feature_pos, regional_settings_lemma
        )
        res = None
        if f_id in self.functionals_implicit:
            res = self.functionals_implicit[f_id]
        return res

    def has_functionals_by_lemma_regional_settings(
        self, lemma: str, regional_settings_lemma: str
    ):
        return (
            regional_settings_lemma
            in self.functionals_by_regional_settings_lemma
            and lemma
            in self.functionals_by_regional_settings_lemma[
                regional_settings_lemma
            ]
        )

    def get_functionals_lemma_for_regional_settings(
        self, regional_settings_lemma: str
    ):
        return list(
            self.functionals_by_regional_settings_lemma[
                regional_settings_lemma
            ].keys()
        )

    def get_undefined_functionals(self, regional_settings_lemma: str):
        if regional_settings_lemma in self.undefined_functionals:
            return self.undefined_functionals[regional_settings_lemma]
        else:
            return []

    def set_working_dictionary(self, working_dictionary):
        self.working_dictionary = working_dictionary

    def is_in_vocabulary(
        self, text: str, regional_settings: str, knowledge_graph=None
    ):
        tokenize_res = self.tokenizer.tokenize_out_of_stats(
            text, regional_settings, knowledge_graph
        )
        res_base = []
        res = (
            tokenize_res.unknowns
            + tokenize_res.invalid_variables
            + tokenize_res.invalid_images
            + tokenize_res.invalid_verbs
        )
        for w in tokenize_res.words:
            # A word is out of vocabulary if is not in non_functionals, not in functionals, not in the working dictionary (including the synonyms), and not in the base dictionary (including the synonyms).
            if (
                w not in self.non_functionals[regional_settings]
                and not self.has_functionals_by_lemma_regional_settings(
                    w, regional_settings
                )
                and not self.base_dictionary.contains_morpheme(w)
                and not self.base_dictionary.contains_synonym(w)
                and not self.working_dictionary.contains_morpheme(w)
                and not self.working_dictionary.contains_synonym(w)
            ):
                res.append(w)
            if self.base_dictionary.contains_morpheme(w):
                res_base.append(w)
        desc = (
            "OVR: " + str(len(res)) + "/" + str(len(tokenize_res.words))
        )  # Out of Vocabulary Ratio
        base_desc = (
            "SPR: " + str(len(res_base)) + "/" + str(len(tokenize_res.words))
        )  # Semantic Primes Ratio
        res_details = [
            "[{0} | {1:.2f}]".format(
                w,
                self.tokenizer.stats[
                    regional_settings
                ].get_word_lexical_relevance_index(w, False),
            )
            for w in res
        ]
        details = " <> ".join(res_details)
        return InVocabulary(
            len(res) == 0,
            res,
            desc,
            details,
            len(res_base) == len(tokenize_res.words),
            res_base,
            base_desc,
        )
