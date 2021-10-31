from collections import namedtuple
import mammut
from mammut.common.constants import DictionaryTable
from mammut.common.basic_tokenizer import BasicTokenizer
from mammut.common.storage.storage_manager import StorageManager
from mammut.common.indexer import DefinitionIndexer
import sys
import pandas as pd


class ExternalDictionarySource:
    def __init__(
        self,
        source_id: str,
        source_url_pattern: str,
        html_wrapper: str,
        regional_settings: str,
        standard,
    ):
        self.source_id = source_id
        self.source_url_pattern = source_url_pattern
        self.html_wrapper = html_wrapper
        self.standard = standard
        self.regional_settings = regional_settings

    def get_url(self, lemma: str):
        return self.source_url_pattern.format(lemma)

    def get_iframe(self, lemma: str):
        return self.html_wrapper.format(self.get_url(lemma))


class DictionaryPosTagEntry:
    def __init__(self, pos_tag: str, postag_group_by_object):
        self.pos_tag = pos_tag
        self.postag_group_by_object = postag_group_by_object
        self.definitions_set_entries = []
        self.morpheme_paradigm = ""
        self.misspellings_paradigm = ""
        self.features_paradigm = ""
        if self.postag_group_by_object is not None:
            self.morpheme_paradigm = list(
                self.postag_group_by_object[
                    DictionaryTable.MORPH_PARADIGM_COLUMN_NAME()
                ]
            )[0]
            self.misspellings_paradigm = list(
                self.postag_group_by_object[DictionaryTable.MISS_PARADIGM_COLUMN_NAME()]
            )[0]
            self.features_paradigm = list(
                self.postag_group_by_object[DictionaryTable.FET_PARADIGM_COLUMN_NAME()]
            )[0]
            self.definitions_set_group_by_object = self.postag_group_by_object.groupby(
                [DictionaryTable.DEFINITION_INDEX_COLUMN_NAME()]
            )
            for g in self.definitions_set_group_by_object:
                self.definitions_set_entries.append(
                    DictionaryDefinitionSetEntry(int(g[0]), g[1])
                )

    def get_definitions_count(self):
        return sum(
            [len(dsg.definitions_entries) for dsg in self.definitions_set_entries]
        )


class DictionaryLemmaEntry:
    def __init__(self, lemma: str, lemma_group_by_object):
        self.lemma = lemma
        self.lemma_group_by_object = lemma_group_by_object
        self.postags_entries = []
        self.postags_index_by_postag_id = {}
        self.word_type = ""
        self.regional_settings_lemma = ""
        self.afi = ""
        if self.lemma_group_by_object is not None:
            self.word_type = list(
                self.lemma_group_by_object[DictionaryTable.WORD_TYPE_COLUMN_NAME()]
            )[0]
            self.regional_settings_lemma = list(
                self.lemma_group_by_object[
                    DictionaryTable.REGIONAL_SETTINGS_LEMMA_COLUMN_NAME()
                ]
            )[0]
            self.afi = list(
                self.lemma_group_by_object[DictionaryTable.AFI_COLUMN_NAME()]
            )[0]
            self.postags_group_by_object = self.lemma_group_by_object.groupby(
                [DictionaryTable.POS_PARADIGM_COLUMN_NAME()]
            )
            for g in self.postags_group_by_object:
                self.add_pos_tag_entry(DictionaryPosTagEntry(g[0], g[1]))

    def get_definitions_count(self):
        return sum(
            [
                len(dsg.definitions_entries)
                for pg in self.postags_entries
                for dsg in pg.definitions_set_entries
            ]
        )

    def add_pos_tag_entry(self, pos_tag_entry: DictionaryPosTagEntry):
        self.postags_entries.append(pos_tag_entry)
        index = self.postags_entries.index(pos_tag_entry)
        self.postags_index_by_postag_id[pos_tag_entry.pos_tag] = index

    def remove_pos_tag_entry(self, pos_tag_entry: DictionaryPosTagEntry):
        self.postags_entries.remove(pos_tag_entry)
        del self.postags_index_by_postag_id[pos_tag_entry.pos_tag]


LexicalizationStatistics = namedtuple(
    "LexicalizationStatistics",
    [
        "lemmas_count",
        "definitions_count",
        "morphemes_count",
        "words_count",
        "undefined_words_count",
    ],
)


class DictionaryDefinitionSetEntry:
    def __init__(self, definition_index: int, definition_set_group_by_object):
        self.definition_index = definition_index
        self.definition_set_group_by_object = definition_set_group_by_object
        self.definitions_entries = []
        self.features = ""
        self.features_list = []
        if self.definition_set_group_by_object is not None:
            self.features = list(
                self.definition_set_group_by_object[
                    DictionaryTable.FEATURES_COLUMN_NAME()
                ]
            )[0]
            if self.features:
                self.features_list = self.features.split(",")
            for d in self.definition_set_group_by_object.iterrows():
                self.definitions_entries.append(
                    DictionaryDefinitionEntry(
                        d[1][DictionaryTable.SOURCE_COLUMN_NAME()],
                        d[1][DictionaryTable.TOPIC_COLUMN_NAME()],
                        d[1][DictionaryTable.DEFINITION_COLUMN_NAME()],
                        d[1][
                            DictionaryTable.REGIONAL_SETTINGS_DEFINITION_COLUMN_NAME()
                        ],
                        d[1][DictionaryTable.DATE_COLUMN_NAME()],
                        d[0],
                    )
                )

    def set_features_list(self, features_to_set):
        self.features_list = [fet_desc.feature_id for fet_desc in features_to_set]
        self.features = ""
        length = len(self.features_list)
        for i in range(0, length):
            self.features += self.features_list[i]
            if i < length - 1:
                self.features += ","

    def get_definitions_count(self):
        return len(self.definitions_entries)


class DictionaryDefinitionEntry:
    def __init__(
        self,
        source: str,
        topic: str,
        definition: str,
        regional_settings_definition: str,
        date: str,
        id: int = None,
    ):
        self.source = source
        self.topic = topic
        self.definition = definition
        self.regional_settings_definition = regional_settings_definition
        self.date = date
        self.id = id


class Dictionary:
    from mammut.common.lexicon.linguistic_standard import LinguisticStandard
    DEFAULT_START_CELL = "A1"
    DEFAULT_START_COLUMN = "A"
    DEFAULT_START_ROW = "1"
    DEFAULT_END_CELL = "P"
    DISAMBIGUATION_DEFAULT_END_CELL = "E"
    DISAMBIGUATION_SHEET_TITLE = "disambiguation"

    def __init__(
        self,
        spreadsheet_id: str,
        sheet_title: str,
        synonym_sheet_title: str,
        tokenizer: BasicTokenizer,
        standard: LinguisticStandard,
        is_base: bool = False,
        package_name="",
        local_storage: bool = False,
    ):
        self.package_name = package_name
        if not self.package_name:
            self.package_name = spreadsheet_id.lower()
        self.storage_manager = StorageManager()
        self.definition_indexer = DefinitionIndexer(self.package_name)
        self.standard = standard
        self.tokenizer = tokenizer
        self.tokenizer.set_dictionary(self)
        self.new_dictionaries_count = 0
        self.spreadsheet_id = spreadsheet_id
        self.original_sheet_title = sheet_title
        self.sheet_title = sheet_title
        self.synonym_sheet_title = synonym_sheet_title
        self.disambiguation_sheet_title = Dictionary.DISAMBIGUATION_SHEET_TITLE
        self.range_name = self.sheet_title + "!" + Dictionary.DEFAULT_START_CELL
        self.disambiguation_range_name = (
            self.disambiguation_sheet_title + "!" + Dictionary.DEFAULT_START_CELL
        )
        self.lemmas_entries = []
        self.morphemes = []
        self.lemmas_entries_by_lemma = {}
        self.lemmas_entries_by_morpheme = {}
        self.lemma_layer = {}
        self.synonym_inverted_index = {}
        self.data_frame = self.storage_manager.get_spreadsheet_as_dataframe(
            self.spreadsheet_id,
            self.sheet_title,
            Dictionary.DEFAULT_START_COLUMN,
            Dictionary.DEFAULT_START_ROW,
            Dictionary.DEFAULT_END_CELL,
        )

        self.definition_indexer.index_dictionary(
            self.data_frame, self.standard, self.spreadsheet_id, self.sheet_title
        )
        if not is_base:
            self.disambiguation_data_frame = self.storage_manager.get_spreadsheet_as_dataframe(
                self.spreadsheet_id,
                self.disambiguation_sheet_title,
                Dictionary.DEFAULT_START_COLUMN,
                Dictionary.DEFAULT_START_ROW,
                Dictionary.DISAMBIGUATION_DEFAULT_END_CELL,
            )

            self.standard.set_working_dictionary(self)
        if self.data_frame is not None:
            self.id_count = len(self.data_frame)
            self.lemmas_group_by_object = self.data_frame.groupby(
                [DictionaryTable.LEMMA_COLUMN_NAME()]
            )
            for g in self.lemmas_group_by_object:
                lemma_entry = DictionaryLemmaEntry(g[0], g[1])
                self.add_lemma_entry(lemma_entry)
        else:
            self.id_count = 0
        self.synonym_range_name = (
            self.synonym_sheet_title + "!" + Dictionary.DEFAULT_START_CELL
        )
        self.synonym_data_frame = self.storage_manager.get_spreadsheet_as_dataframe(
            self.spreadsheet_id,
            self.synonym_sheet_title,
            Dictionary.DEFAULT_START_COLUMN,
            Dictionary.DEFAULT_START_ROW,
            Dictionary.DEFAULT_END_CELL,
        )

        if self.synonym_data_frame is not None:
            for r in self.synonym_data_frame.iterrows():
                sense_lemma = r[1][DictionaryTable.SENSE_LEMMA_COLUMN_NAME()]
                syn_words = r[1][DictionaryTable.SYNONYM_WORDS_COLUMN_NAME()]
                for s_w in syn_words.split(","):
                    s_w = s_w.strip().lower()
                    if s_w in self.synonym_inverted_index:
                        self.synonym_inverted_index[s_w].append(sense_lemma)
                    else:
                        self.synonym_inverted_index[s_w] = [sense_lemma]

    def contains_lemma(self, lemma: str):
        return lemma in self.lemmas_entries_by_lemma

    def contains_morpheme(self, morpheme: str):
        return morpheme in self.lemmas_entries_by_morpheme

    def contains_synonym(self, word: str):
        return word in self.synonym_inverted_index

    def _update_lemma_entries(self, lemmas, regional_settings):
        entries = []
        receipts = ""
        for lg in lemmas:
            for pg in lg.postags_entries:
                morphemes = self.standard.get_morphemes(
                    pg.pos_tag,
                    pg.morpheme_paradigm.split(" ")[0],
                    lg.lemma,
                    regional_settings,
                )
                for dsg in pg.definitions_set_entries:
                    for d in dsg.definitions_entries:
                        entry = [
                            lg.lemma,
                            lg.word_type,
                            lg.regional_settings_lemma,
                            lg.afi,
                            pg.pos_tag,
                            pg.morpheme_paradigm,
                            pg.misspellings_paradigm,
                            pg.features_paradigm,
                            dsg.definition_index,
                            dsg.features,
                            d.source,
                            d.topic,
                            d.definition,
                            d.regional_settings_definition,
                            d.date,
                        ]
                        entries.append(entry)
                        definition_to_index = entry
                        self.definition_indexer.index_lemma(
                            definition_to_index, morphemes
                        )
                        if d.id is not None:
                            self.storage_manager.update_row_from_spreadsheet(
                                self.spreadsheet_id,
                                self.sheet_title,
                                entry,
                                "A",
                                str(d.id + 2),
                            )
                        else:
                            self.storage_manager.append_row_to_sheet(
                                self.spreadsheet_id, "dictionary", entry
                            )
                            next_id = self.id_count
                            d.id = next_id
                            self.id_count = self.id_count + 1

        self.data_frame = self.storage_manager.get_spreadsheet_as_dataframe(
            self.spreadsheet_id,
            self.sheet_title,
            Dictionary.DEFAULT_START_COLUMN,
            Dictionary.DEFAULT_START_ROW,
            Dictionary.DEFAULT_END_CELL,
        )

        for e in entries:
            if receipts:
                receipts += "\n"
            receipts += self.definition_indexer.get_receipt(e[0], e[12])
        return receipts

    def delete_definition_lemma(self, lemma_to_delete, definition):
        data = []
        data.append(
            [
                DictionaryTable.LEMMA_COLUMN_NAME(),
                DictionaryTable.WORD_TYPE_COLUMN_NAME(),
                DictionaryTable.REGIONAL_SETTINGS_LEMMA_COLUMN_NAME(),
                DictionaryTable.AFI_COLUMN_NAME(),
                DictionaryTable.POS_PARADIGM_COLUMN_NAME(),
                DictionaryTable.MORPH_PARADIGM_COLUMN_NAME(),
                DictionaryTable.MISS_PARADIGM_COLUMN_NAME(),
                DictionaryTable.FET_PARADIGM_COLUMN_NAME(),
                DictionaryTable.DEFINITION_INDEX_COLUMN_NAME(),
                DictionaryTable.FEATURES_COLUMN_NAME(),
                DictionaryTable.SOURCE_COLUMN_NAME(),
                DictionaryTable.TOPIC_COLUMN_NAME(),
                DictionaryTable.DEFINITION_COLUMN_NAME(),
                DictionaryTable.REGIONAL_SETTINGS_DEFINITION_COLUMN_NAME(),
                DictionaryTable.DATE_COLUMN_NAME(),
                DictionaryTable.TIMESTAMP_COLUMN_NAME(),
            ]
        )
        deleted = False
        for index, lemma in enumerate(
            self.data_frame[DictionaryTable.LEMMA_COLUMN_NAME()]
        ):
            if (
                lemma == lemma_to_delete
                and self.data_frame[DictionaryTable.DEFINITION_COLUMN_NAME()][index]
                == definition
            ):
                deleted = True
                pass
            else:
                if lemma == lemma_to_delete and deleted:
                    self.data_frame[DictionaryTable.DEFINITION_INDEX_COLUMN_NAME()][
                        index
                    ] = str(
                        int(
                            self.data_frame[
                                DictionaryTable.DEFINITION_INDEX_COLUMN_NAME()
                            ][index]
                        )
                        - 1
                    )
                data.append(
                    [
                        self.data_frame[DictionaryTable.LEMMA_COLUMN_NAME()][index],
                        self.data_frame[DictionaryTable.WORD_TYPE_COLUMN_NAME()][index],
                        self.data_frame[
                            DictionaryTable.REGIONAL_SETTINGS_LEMMA_COLUMN_NAME()
                        ][index],
                        self.data_frame[DictionaryTable.AFI_COLUMN_NAME()][index],
                        self.data_frame[DictionaryTable.POS_PARADIGM_COLUMN_NAME()][
                            index
                        ],
                        self.data_frame[DictionaryTable.MORPH_PARADIGM_COLUMN_NAME()][
                            index
                        ],
                        self.data_frame[DictionaryTable.MISS_PARADIGM_COLUMN_NAME()][
                            index
                        ],
                        self.data_frame[DictionaryTable.FET_PARADIGM_COLUMN_NAME()][
                            index
                        ],
                        int(
                            self.data_frame[
                                DictionaryTable.DEFINITION_INDEX_COLUMN_NAME()
                            ][index]
                        ),
                        self.data_frame[DictionaryTable.FEATURES_COLUMN_NAME()][index],
                        self.data_frame[DictionaryTable.SOURCE_COLUMN_NAME()][index],
                        self.data_frame[DictionaryTable.TOPIC_COLUMN_NAME()][index],
                        self.data_frame[DictionaryTable.DEFINITION_COLUMN_NAME()][
                            index
                        ],
                        self.data_frame[
                            DictionaryTable.REGIONAL_SETTINGS_DEFINITION_COLUMN_NAME()
                        ][index],
                        self.data_frame[DictionaryTable.DATE_COLUMN_NAME()][index],
                        self.data_frame[DictionaryTable.TIMESTAMP_COLUMN_NAME()][index],
                    ]
                )

        self.storage_manager.delete_sheet(
            self.spreadsheet_id,
            self.storage_manager.get_sheet_id(self.spreadsheet_id, "dictionary"),
        )
        self.storage_manager.create_new_sheet(self.spreadsheet_id, "dictionary")
        self.storage_manager.add_rows_to_spreadsheet(
            self.spreadsheet_id, self.sheet_title + "!" + "A1", data
        )
        self.data_frame = self.storage_manager.get_spreadsheet_as_dataframe(
            self.spreadsheet_id,
            self.sheet_title,
            Dictionary.DEFAULT_START_COLUMN,
            Dictionary.DEFAULT_START_ROW,
            Dictionary.DEFAULT_END_CELL,
        )

    def _save_lemma_entries(self, lemmas, regional_settings):
        entries = []
        receipts = ""
        for lg in lemmas:
            for pg in lg.postags_entries:
                morphemes = self.standard.get_morphemes(
                    pg.pos_tag,
                    pg.morpheme_paradigm.split(" ")[0],
                    lg.lemma,
                    regional_settings,
                )
                for dsg in pg.definitions_set_entries:
                    for d in dsg.definitions_entries:
                        next_id = (
                            self.id_count
                        )  # TODO:esto de setear los id's deberia ir el los metodos privados??
                        d.id = next_id
                        self.id_count = self.id_count + 1
                        entry = [
                            lg.lemma,
                            lg.word_type,
                            lg.regional_settings_lemma,
                            lg.afi,
                            pg.pos_tag,
                            pg.morpheme_paradigm,
                            pg.misspellings_paradigm,
                            pg.features_paradigm,
                            dsg.definition_index,
                            dsg.features,
                            d.source,
                            d.topic,
                            d.definition,
                            d.regional_settings_definition,
                            d.date,
                            str(mammut.get_timezone_aware_datetime_now()),
                        ]
                        definition_to_index = entry
                        self.definition_indexer.index_lemma(
                            definition_to_index, morphemes
                        )
                        entries.append(entry)
        self.storage_manager.add_rows_to_spreadsheet(
            self.spreadsheet_id, self.range_name, entries
        )
        self.data_frame = self.storage_manager.get_spreadsheet_as_dataframe(
            self.spreadsheet_id,
            self.sheet_title,
            Dictionary.DEFAULT_START_COLUMN,
            Dictionary.DEFAULT_START_ROW,
            Dictionary.DEFAULT_END_CELL,
        )

        for e in entries:
            if receipts:
                receipts += "\n"
            receipts += self.definition_indexer.get_receipt(e[0], e[12])
        return receipts

    def add_lemma_entry(
        self, lemma_entry: DictionaryLemmaEntry, save_to_google_sheet=False
    ):
        regional_settings = lemma_entry.regional_settings_lemma
        result = None
        self.lemmas_entries_by_lemma[lemma_entry.lemma] = lemma_entry
        self.lemmas_entries.append(lemma_entry)
        for pg in lemma_entry.postags_entries:
            layer = 0
            for m in self.standard.get_morphemes(
                pg.pos_tag, pg.morpheme_paradigm, lemma_entry.lemma, regional_settings
            ):
                if m.text not in self.lemmas_entries_by_morpheme:
                    self.lemmas_entries_by_morpheme[m.text] = []
                    self.morphemes.append(m.text)
                self.lemmas_entries_by_morpheme[m.text].append(lemma_entry)
                if (
                    m.text in self.tokenizer.stats[regional_settings].word_layer
                    and self.tokenizer.stats[regional_settings].word_layer[m.text]
                    > layer
                ):
                    layer = self.tokenizer.stats[regional_settings].word_layer[m.text]
            for dsg in pg.definitions_set_entries:
                for d in dsg.definitions_entries:
                    self.tokenizer.tokenize_definition(
                        d.definition, layer + 1, regional_settings, None
                    )
        if save_to_google_sheet:
            result = self._save_lemma_entries([lemma_entry], regional_settings)
        return result

    def update_lemma_entry(
        self, lemma_entry: DictionaryLemmaEntry, save_to_google_sheet=False
    ):
        regional_settings = lemma_entry.regional_settings_lemma
        result = None
        self.lemmas_entries_by_lemma[lemma_entry.lemma] = lemma_entry
        old_lemma_entry_index = next(
            index
            for (index, d) in enumerate(self.lemmas_entries)
            if d.lemma == lemma_entry.lemma
        )
        self.lemmas_entries[old_lemma_entry_index] = lemma_entry

        for pg in lemma_entry.postags_entries:
            layer = 0
            for m in self.standard.get_morphemes(
                pg.pos_tag, pg.morpheme_paradigm, lemma_entry.lemma, regional_settings
            ):
                if m.text not in self.lemmas_entries_by_morpheme:
                    self.lemmas_entries_by_morpheme[m.text] = []
                    self.morphemes.append(m.text)
                self.lemmas_entries_by_morpheme[m.text].append(lemma_entry)
                if (
                    m.text in self.tokenizer.stats[regional_settings].word_layer
                    and self.tokenizer.stats[regional_settings].word_layer[m.text]
                    > layer
                ):
                    layer = self.tokenizer.stats[regional_settings].word_layer[m.text]
            for dsg in pg.definitions_set_entries:
                for d in dsg.definitions_entries:
                    self.tokenizer.tokenize_definition(
                        d.definition, layer + 1, regional_settings, None
                    )
        if save_to_google_sheet:
            result = self._update_lemma_entries([lemma_entry], regional_settings)
        return result

    def create_new_dictionary(self, regional_settings):
        self.new_dictionaries_count += 1
        self.sheet_title = self.original_sheet_title + str(self.new_dictionaries_count)
        self.range_name = self.sheet_title + "!" + Dictionary.DEFAULT_START_CELL
        self.storage_manager.create_new_sheet(self.spreadsheet_id, self.sheet_title)
        result = self._save_lemma_entries(self.lemmas_entries, regional_settings)
        return result

    def get_undefined_morphemes_generator(
        self, regional_settings, layer=0, with_index=False
    ):
        return self.get_morphemes_generator(regional_settings, layer, with_index, True)

    def get_defined_morphemes_generator(
        self, regional_settings, layer=0, with_index=False
    ):
        return self.get_morphemes_generator(regional_settings, layer, with_index, False)

    def get_morphemes_generator(self, regional_settings, layer, with_index, undefined):
        stats_words_generator = self.tokenizer.stats[
            regional_settings
        ].get_words_generator(layer, with_index)
        stop = False
        while not stop:
            try:
                g_r = next(stats_words_generator)
                if with_index:
                    w = g_r[0]
                else:
                    w = g_r
                if undefined:
                    if (
                        not self.contains_morpheme(w)
                        and not self.standard.base_dictionary.contains_morpheme(w)
                        and not self.standard.has_functionals_by_lemma_regional_settings(
                            w, regional_settings
                        )
                        and not self.contains_synonym(w)
                        and not self.standard.base_dictionary.contains_synonym(w)
                    ):
                        yield g_r
                elif not undefined:
                    if (
                        self.contains_morpheme(w)
                        or self.standard.base_dictionary.contains_morpheme(w)
                        or self.standard.has_functionals_by_lemma_regional_settings(
                            w, regional_settings
                        )
                        or self.contains_synonym(w)
                        or self.standard.base_dictionary.contains_synonym(w)
                    ):
                        yield g_r
            except StopIteration:
                stop = True

    def get_definitions_count(self):
        return sum(
            [
                len(dsg.definitions_entries)
                for lg in self.lemmas_entries
                for pg in lg.postags_entries
                for dsg in pg.definitions_set_entries
            ]
        )

    def get_morphemes_count(self):
        return len(self.lemmas_entries_by_morpheme)

    def get_undefined_morphemes_count(self, regional_settings):
        return sum(
            [
                1
                if not self.contains_morpheme(w)
                and not self.standard.has_functionals_by_lemma_regional_settings(
                    w, regional_settings
                )
                else 0
                for w in self.tokenizer.stats[regional_settings].get_words_generator(
                    sys.maxsize
                )
            ]
        )

    def get_lemma(self, lemma: str):
        if self.contains_lemma(lemma):
            lemma_result = self.lemmas_entries_by_lemma[lemma]
        else:
            lemma_result = None
        return lemma_result

    def get_morphemes_of_lemma(self, lemma: str, as_tuple: bool = False
                               ):
        result = set()
        lemma_entry = self.get_lemma(lemma)
        if lemma_entry is not None:
            regional_settings = lemma_entry.regional_settings_lemma
            for pg in lemma_entry.postags_entries:
                for m in self.standard.get_morphemes(
                    pg.pos_tag,
                    pg.morpheme_paradigm,
                    lemma_entry.lemma,
                    regional_settings,
                ):
                    result.add(m.text)
        return result

    def get_implicit_functional_lemma_name(
        self, lemma, textbound_annotation, reference_dict
    ):
        functional_visual_identifier = "*"
        print("functional implicit lemma name", lemma)
        name = "{functional}({lemma})*".format(
            functional=lemma, lemma=textbound_annotation.text
        )
        if name in reference_dict.keys():
            print("se esta repitiendo un value en el dict")
        return name

    def get_functional_lemma_name(self, lemma, index, reference_dict):
        print("functional lemma name", lemma)
        name = "{functional}({index})*".format(functional=lemma, index=index)
        if name in reference_dict.keys():
            print("se esta repitiendo un value en el dict")
        return name

    def get_index_from_span(self, event_annotation, textbound_annotation):
        document = event_annotation.documents_by_dimension["t-pos"]
        sorted_spans = [
            tbsorted.spans[0]
            for tbsorted in sorted(
                document.ann_obj.get_textbounds(), key=lambda tb: tb.spans
            )
        ]
        return sorted_spans.index(textbound_annotation.spans[0])

    def get_functional_disambiguation_dicts(
        self,
        event_annotation,
        textbound_annotation,
        tokens_dict,
        tokens_info_dict,
        tokens_type_resume,
        implicit_functional_lemma_descriptor=None,
    ):
        textbound_index = self.get_index_from_span(
            event_annotation, textbound_annotation
        )
        # TODO: aqui debe ser el lemma de la palabra funcional cuando es implicita
        if implicit_functional_lemma_descriptor is not None:
            tokens_type_resume["functional"].append(
                implicit_functional_lemma_descriptor.lemma
            )
            funtional_lemma_descriptor = implicit_functional_lemma_descriptor
            span = ""
            dict_key = self.get_implicit_functional_lemma_name(
                implicit_functional_lemma_descriptor.lemma,
                textbound_annotation,
                tokens_dict,
            )
            tokens_dict[
                dict_key
            ] = implicit_functional_lemma_descriptor.implicit_condition_id
            tokens_info_dict[dict_key] = [
                event_annotation.get_id(),
                textbound_annotation.text,
                span,
                textbound_annotation.type,
            ]
        else:
            tokens_type_resume["functional"].append(textbound_annotation.text.lower())
            funtional_lemma_descriptor = self.standard.get_functional_lemma_descriptor(
                textbound_annotation.text.lower(),
                event_annotation.event["regnional_settings"],
                textbound_annotation.type,
            )
            span = (
                str(textbound_annotation.spans[0][0])
                + ","
                + str(textbound_annotation.spans[0][1])
            )
            dict_key = self.get_functional_lemma_name(
                textbound_annotation.text.lower(), textbound_index, tokens_dict
            )
            tokens_dict[dict_key] = (
                funtional_lemma_descriptor.lemma
                + "-"
                + event_annotation.event["regnional_settings"]
                + "-"
                + textbound_annotation.type
            )
            tokens_info_dict[dict_key] = [
                event_annotation.get_id(),
                textbound_annotation.text,
                span,
                textbound_annotation.type,
            ]
        return tokens_dict, tokens_info_dict, tokens_type_resume

    def get_event_tokens_dict_and_info(
        self, event_annotation
    ):  # TODO definir bien el nombre
        tokens_dict = {}
        tokens_info_dict = {}
        tokens_type_resume = {"lexical": [], "functional": [], "none": []}
        document = event_annotation.documents_by_dimension["t-pos"]
        ZERO_ARTICLE = "zero_article"
        for i in document.ann_obj.get_textbounds():
            attr_anns = [
                attribute_annotation
                for attribute_annotation in document.ann_obj.get_attributes()
                if i.id == attribute_annotation.target
                and attribute_annotation.value == ZERO_ARTICLE
            ]
            if i.text.lower() in self.lemmas_entries_by_morpheme:
                tokens_type_resume["lexical"].append(i.text.lower())
                for pos_index, pos_tag_entry in enumerate(
                    self.lemmas_entries_by_morpheme[i.text.lower()][0].postags_entries
                ):
                    # TODO: aqui te falta un gran if que condicione todo la ejecucion de toda la logica dentro del for
                    # la logica dentro del for solo te interesa si el pos-tag de la iteracion coincide con el pos-tag en la anotacion
                    if (
                        i.type == pos_tag_entry.pos_tag
                        or i.type
                        in self.standard.pos_descriptor_list[
                            pos_tag_entry.pos_tag
                        ].pos_shifts_ids
                    ):
                        if (
                            len(
                                self.lemmas_entries_by_morpheme[i.text.lower()][0]
                                .postags_entries[pos_index]
                                .definitions_set_entries
                            )
                            > 1
                        ):
                            tokens_dict[i.text.lower()] = (
                                self.lemmas_entries_by_morpheme[i.text.lower()][0].lemma
                                + "-"
                                + pos_tag_entry.pos_tag
                            )
                            # TODO deberia crear metodo para generar esta columan, lo hago aqui para no volver a iterar sobre los textbounbds, revisar que sale mejor
                            tokens_info_dict[i.text.lower()] = [
                                event_annotation.get_id(),
                                i.text,
                                str(i.spans[0][0]) + "," + str(i.spans[0][1]),
                                i.type,
                            ]
                        # TODO: debemos tener un if que siempre revise todas las anotaciones de todas las palabras lexicas
                        # para validar si tiene algun feature que indica la presencia de una palabra funcional implicita
                        # aqui abajo debes pasar el feature class y el feature id, no se como sacarlos de la anotacion
                        # el pos-tag y el regional settings creo que si lo pase bien
                        if len(attr_anns):
                            feature_pos, feature_class = attr_anns[0].type.split("-")
                            feature_id = attr_anns[0].value
                            implicit_functional_lemma_descriptor = self.standard.get_implicit_functional_lemma_descriptor(
                                feature_class,
                                feature_id,
                                feature_pos,
                                event_annotation.event["regnional_settings"],
                            )
                            if implicit_functional_lemma_descriptor is not None:
                                print("###################")
                                print(
                                    "el implicit functional es:",
                                    implicit_functional_lemma_descriptor.lemma,
                                )
                                # TODO: debes hacer algo parecido a lo que haces abajo cuando es un funcional
                                (
                                    tokens_dict,
                                    tokens_info_dict,
                                    tokens_type_resume,
                                ) = self.get_functional_disambiguation_dicts(
                                    event_annotation,
                                    i,
                                    tokens_dict,
                                    tokens_info_dict,
                                    tokens_type_resume,
                                    implicit_functional_lemma_descriptor,
                                )
            elif (
                self.standard.get_functional_lemma_descriptor(
                    i.text.lower(), event_annotation.event["regnional_settings"], i.type
                )
                is not None
            ):
                (
                    tokens_dict,
                    tokens_info_dict,
                    tokens_type_resume,
                ) = self.get_functional_disambiguation_dicts(
                    event_annotation,
                    i,
                    tokens_dict,
                    tokens_info_dict,
                    tokens_type_resume,
                )
            else:
                tokens_type_resume["none"].append(i.text.lower())
        return tokens_dict, tokens_info_dict, tokens_type_resume

    def get_definitions_entries_as_list(self, definitions_set_entries_id):
        id_elements = definitions_set_entries_id.split("-")
        lemma = id_elements[0]
        if lemma in self.lemmas_entries_by_lemma:
            pos = id_elements[1]
            pos_index = self.lemmas_entries_by_lemma[lemma].postags_index_by_postag_id[
                pos
            ]
            definition_set = []
            for i in (
                self.lemmas_entries_by_lemma[lemma]
                .postags_entries[pos_index]
                .definitions_set_entries
            ):
                definitions = []
                for j in i.definitions_entries:
                    definitions.append(j.definition)
                definition_set.append(definitions)
            return definition_set
        else:
            definition_set = []
            functional_lemma_descriptor = None
            if len(id_elements) == 3:  # id normal de lemma descriptor
                regional_settings = id_elements[1]
                pos = id_elements[2]
                # TODO: como hacemos para pedir los implicit_functional_lamadescripotors?pasamos un param que digasi buscamos functional o funtional implicit?
                if self.standard.get_functional_lemma_descriptor(
                    lemma, regional_settings, pos
                ):
                    functional_lemma_descriptor = self.standard.get_functional_lemma_descriptor(
                        lemma, regional_settings, pos
                    )
            elif len(id_elements) == 4:  # implicit_condition_id
                feature_class = id_elements[0]
                feature_id = id_elements[1]
                feature_pos = id_elements[2]
                regional_settings_lemma = id_elements[3]
                if self.standard.get_implicit_functional_lemma_descriptor(
                    feature_class, feature_id, feature_pos, regional_settings_lemma
                ):
                    functional_lemma_descriptor = self.standard.get_implicit_functional_lemma_descriptor(
                        feature_class, feature_id, feature_pos, regional_settings_lemma
                    )
            else:
                raise RuntimeError("Invalid functional lemma id.")
            for i in functional_lemma_descriptor.definitions:
                definition_set.append([i.get_description()])
            return definition_set

    def get_definition_complete_id(self, definitions_set_entries_id, index):
        splited_id = definitions_set_entries_id.split("-")
        if len(splited_id) == 2:
            return definitions_set_entries_id + "-" + str(index)
        elif len(splited_id) == 3:
            descriptor = self.standard.get_functional_lemma_descriptor(
                splited_id[0], splited_id[1], splited_id[2]
            )
            definition = descriptor.definitions[index]
            return (
                definition.lemma
                + "-"
                + descriptor.pos_paradigm
                + "-"
                + definition.index
            )
        elif len(splited_id) == 4:
            descriptor = self.standard.get_implicit_functional_lemma_descriptor(
                splited_id[0], splited_id[1], splited_id[2], splited_id[3]
            )
            definition = descriptor.definitions[index]
            return (
                definition.lemma
                + "-"
                + descriptor.pos_paradigm
                + "-"
                + definition.index
            )

    def is_disambiguation_selected(self, token_info, result_id):
        row_in_data_frame = self.disambiguation_data_frame.query(
            'id == "'
            + token_info[0]
            + '" and text == "'
            + token_info[1]
            + '" and span == "'
            + token_info[2]
            + '" and pos == "'
            + token_info[3]
            + '"  and definition_id == "'
            + result_id
            + '"'
        )
        return len(row_in_data_frame) > 0

    def save_lema_disambiguation(self, token_info, definition_id):
        row_in_data_frame = self.disambiguation_data_frame.query(
            'id == "'
            + token_info[0]
            + '" and text == "'
            + token_info[1]
            + '" and span == "'
            + token_info[2]
            + '" and pos == "'
            + token_info[3]
            + '"'
        )
        if len(row_in_data_frame) > 0:
            index = row_in_data_frame.index.values[0]
            self.storage_manager.delete_rows_from_spreadsheet(
                self.spreadsheet_id,
                Dictionary.DISAMBIGUATION_SHEET_TITLE,
                str(index + 1),
                str(index + 2),
            )
            self.disambiguation_data_frame = self.disambiguation_data_frame.drop(index)
        row = token_info + [definition_id]
        self.disambiguation_data_frame = self.disambiguation_data_frame.append(
            pd.Series(row, list(self.disambiguation_data_frame.columns)),
            ignore_index=True,
        )
        return self.storage_manager.append_row_to_sheet(
            self.spreadsheet_id, Dictionary.DISAMBIGUATION_SHEET_TITLE, row
        )

    def get_lexicalization_statistics(self, regional_settings: str):
        lemmas_count = 0
        definitions_count = 0
        for lg in self.lemmas_entries:
            lemmas_count = lemmas_count + 1
            for pg in lg.postags_entries:
                for dsg in pg.definitions_set_entries:
                    definitions_count = definitions_count + len(dsg.definitions_entries)
        morphemes_count = self.get_morphemes_count()
        words_count = 0
        undefined_morphemes_count = 0
        stats_words_generator = self.tokenizer.stats[
            regional_settings
        ].get_words_generator(sys.maxsize)
        stop = False
        while not stop:
            try:
                w = next(stats_words_generator)
                words_count = words_count + 1
                if not self.contains_morpheme(
                    w
                ) and not self.standard.has_functionals_by_lemma_regional_settings(
                    w, regional_settings
                ):
                    undefined_morphemes_count = undefined_morphemes_count + 1
            except StopIteration:
                stop = True
        return LexicalizationStatistics(
            lemmas_count,
            definitions_count,
            morphemes_count,
            words_count,
            undefined_morphemes_count,
        )

    def get_words_in_definitions_out_of_vocabulary(self, regional_settings: str):
        res = set()
        for lg in self.lemmas_entries:
            for pg in lg.postags_entries:
                for dsg in pg.definitions_set_entries:
                    for d in dsg.definitions_entries:
                        dov = set(
                            self.standard.is_in_vocabulary(
                                d.definition, regional_settings
                            ).list
                        )
                        res = res.union(dov)
        return res
