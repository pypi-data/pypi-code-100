import functools
import json

import mammut
from mammut.common.basic_tokenizer import BasicTokenizer
from mammut.common.corpus.constants import CorpusTable, CrawlerCorpusTable
from mammut.common.corpus.mammut_brat_document import MammutBratDocument
from mammut.common.lexicon.dictionary import Dictionary
from mammut.common.lexicon.mammut_brat_configuration import (
    MammutBratConfiguration,
)
from mammut.common.storage.storage_manager import StorageManager
from mammut.common.util import StringEnum, RegionalSettingsType
from mammut.common.corpus.corpus_operations import CorpusOperations
from typing import List


class ScenarioType(StringEnum):
    """
        Possible Scenario types.
    """
    Monologue = "Monologue"
    Conversation = "Conversation"
    Dialogue = "Dialogue"


class CorpusEventEntry:
    """This class encapsulates the concrete notion
    of a Corpus Event.

    An event is a message emitted by an agent in a channel.

    This class can be used as it is, or it can be extended by
    other specific events classes.

    TODO: Document class methods.
    """
    def __init__(
        self,
        sub_id: int,
        str_message: str,
        str_field: str,
        str_complexity: str,
        str_source: str,
        str_regional_settings: str,
        tokenizer: BasicTokenizer,
        dictionary: Dictionary,
        scenario_entry,
    ):
        self.valid = True
        self.errors = []
        self.tokenized_messages = []
        self.sub_id = sub_id
        self.field = str_field
        self.str_complexity = str_complexity
        self.str_source = str_source
        self.str_regional_settings = str_regional_settings
        self.tokenizer = tokenizer
        self.dictionary = dictionary
        self.scenario_entry = scenario_entry
        self.is_from_mammut = (
            CorpusTable.MAMMUT_USERS_PREFIX() in self.str_source.lower()
        )
        # Validating
        if self.str_complexity.isdigit():
            self.complexity = int(self.str_complexity)
        elif not self.str_complexity:
            self.complexity = 1
        else:
            self.complexity = 1
            self.valid = False
            self.errors.append(
                f"Invalid Complexity: not a digit. SubId = {self.sub_id}"
            )
        if RegionalSettingsType.contains_value(self.str_regional_settings):
            self.regional_settings = RegionalSettingsType(
                self.str_regional_settings
            )
        else:
            self.regional_settings = RegionalSettingsType.ES
            self.valid = False
            self.errors.append(
                f"Invalid Regional Settings: unknown regional settings {self.str_regional_settings}. SubId = {self.sub_id}"
            )
        self.add_message(str_message, False)

    def add_message(self, str_message: str, is_extension: bool):
        def add_error_of_invalid_message(error_msg, invalid_tokens):
            self.valid = False
            invalid_tokens_str = functools.reduce(
                lambda l, r: f"{l} - {r}", invalid_tokens, ""
            )
            if not is_extension:
                error_msg = (
                    "Invalid Meesage: "
                    + error_msg
                    + f". SubId = {self.sub_id}"
                )
            else:
                error_msg = (
                    "Invalid Extension Meesage: "
                    + error_msg
                    + f". SubId = {self.sub_id} - Message = {str_message}"
                )
            self.errors.append(
                error_msg + f" Invalid tokens: {invalid_tokens_str}"
            )

        tokenized_message = self.tokenizer.tokenize_corpus_entry(
            str_message,
            self.scenario_entry.corpus.annotable,
            self.str_regional_settings,
        )
        if tokenized_message.contains_invalid_variables():
            add_error_of_invalid_message(
                "the message contains invalid variables",
                tokenized_message.invalid_variables,
            )
        if tokenized_message.contains_invalid_images():
            add_error_of_invalid_message(
                "the message contains invalid images",
                tokenized_message.invalid_images,
            )
        if tokenized_message.contains_invalid_verbs():
            add_error_of_invalid_message(
                "the message contains invalid buttons",
                tokenized_message.invalid_verbs,
            )
        if tokenized_message.contains_unknown():
            add_error_of_invalid_message(
                "the message contains a token that is not qualifiy as valid",
                tokenized_message.unknowns,
            )
        self.tokenized_messages.append(tokenized_message)

    def get_annotation_documents(self, config: MammutBratConfiguration):
        return [
            MammutBratDocument(mt, config) for mt in self.tokenized_messages
        ]


class CorpusScenarioEntry:
    """This class encapsulates the general notion of a scenario.

    A scenario is a set of interactions that belongs to the same context,
    then they are a sequence of chronological corpus events. Each new sequence
    of events will be part of a new scenario.

    This class can be used as it is, or it can be extended by other
    specific scenario classes.

    # TODO: Document class methods
    """
    def __init__(
        self,
        str_id: str,
        str_type: str,
        scenerie_group_by_object,
        tokenizer: BasicTokenizer,
        dictionary: Dictionary,
        language_settings: str,
        corpus,
    ):
        self.valid = True
        self.contains_invalid_events = False
        self.errors = []
        self.str_id = str_id
        self.scenerie_group_by_object = scenerie_group_by_object
        self.tokenizer = tokenizer
        self.dictionary = dictionary
        self.language_settings = language_settings
        self.corpus = corpus
        self.str_type = str_type
        self.events = []
        # Global validations
        if self.str_id.isdigit():
            self.id = int(self.str_id)
        else:
            self.valid = False
            self.errors.append("Invalid Id: is not a integer")
        if self.str_type in list(ScenarioType.__members__):
            self.type = ScenarioType(self.str_type)
        else:
            self.type = ScenarioType.Conversation
            self.valid = False
            self.errors.append("Invalid Type: unknown scenario type")
        last_event_is_from_mammut = True
        last_event_source = ""
        index = 0
        all_hidden = True
        for e in self.scenerie_group_by_object.iterrows():
            if (
                CorpusTable.HIDDEN_COLUMN_NAME() not in e[1]
                or not e[1][CorpusTable.HIDDEN_COLUMN_NAME()]
            ):
                cee = self.get_corpus_event_entry_from_event_row(index, e)
                self.events.append(cee)
                self.validate_corpus_event_entry(
                    index, cee, last_event_source, last_event_is_from_mammut
                )
                last_event_source = cee.str_source
                last_event_is_from_mammut = cee.is_from_mammut
                index = index + 1
                all_hidden = False
        if (
            self.type is not ScenarioType.Monologue
            and len(self.events) < 2
            and not all_hidden
        ):
            self.valid = False
            self.errors.append(
                f"Invalid Amount of entries: less than 2. Id = {self.str_id}"
            )

    def get_corpus_event_entry_from_event_row(self, index, e):
        event_message = ""
        if (
            CorpusTable.EVENT_MESSAGE_COLUMN_NAME() in e[1]
            and e[1][CorpusTable.EVENT_MESSAGE_COLUMN_NAME()]
        ):
            event_message = e[1][CorpusTable.EVENT_MESSAGE_COLUMN_NAME()]

        return CorpusEventEntry(
            index,
            event_message,
            e[1][CorpusTable.FIELD_COLUMN_NAME()]
            if CorpusTable.FIELD_COLUMN_NAME() in e[1]
            else "",
            e[1][CorpusTable.COMPLEXITY_COLUMN_NAME()]
            if CorpusTable.COMPLEXITY_COLUMN_NAME() in e[1]
            else "",
            e[1][CorpusTable.SOURCE_COLUMN_NAME()]
            if CorpusTable.SOURCE_COLUMN_NAME() in e[1]
            else "",
            e[1][CorpusTable.REGIONAL_SETTINGS_COLUMN_NAME()],
            self.tokenizer,
            self.dictionary,
            self,
        )

    def validate_corpus_event_entry(
        self, index, cee, last_event_source, last_event_is_from_mammut
    ):
        # Validations at event level
        if not cee.valid and not self.contains_invalid_events:
            self.valid = False
            self.contains_invalid_events = True
            self.errors.append("Contains invalid events")
            self.errors.extend(cee.errors)
        if (
            self.type is not ScenarioType.Monologue
            and cee.str_source == last_event_source
        ):
            self.valid = False
            self.errors.append(
                f"Invalid sequence of events: two consecutive events from the same source. Id = {self.str_id} - SubId = {index}"
            )
        if (
            self.type is ScenarioType.Conversation
            and not last_event_is_from_mammut
            and not cee.is_from_mammut
        ):
            self.valid = False
            self.errors.append(
                f"Invalid sequence of events: two consecutive events from users in a conversation scenario. Id = {self.str_id} - SubId = {index}"
            )
        if self.type is ScenarioType.Monologue:
            if cee.is_from_mammut:
                self.valid = False
                self.errors.append(
                    f"Invalid sequence of events: one event from mammut in a monologue scenario. Id = {self.str_id} - SubId = {index}"
                )
            elif cee.str_source != last_event_source and index != 0:
                self.valid = False
                self.errors.append(
                    f"Invalid sequence of events: more than one source in a monologue scenario. Id = {self.str_id} - SubId = {index}"
                )

    def add_event_extension(self, sub_id: int, str_message: str):
        if sub_id < len(self.events):
            self.events[sub_id].add_message(str_message, True)
        else:
            self.valid = False
            self.errors.append(
                f"Invalid Extension Meesage: the message has a sub-id greater or equal to the amount of events in the scenario . SubId = {sub_id} - Message = {str_message}"
            )

    def add_event_extensions(self, scenerie_ext_group_by_object):
        for ee in scenerie_ext_group_by_object.iterrows():
            if (
                CorpusTable.HIDDEN_COLUMN_NAME() not in ee[1]
                or not ee[1][CorpusTable.HIDDEN_COLUMN_NAME()]
            ):
                sub_id_str = ee[1][CorpusTable.SUB_ID_COLUMN_NAME()]
                str_message = ""
                if CorpusTable.EVENT_MESSAGE_COLUMN_NAME() in ee[1]:
                    str_message = ee[1][
                        CorpusTable.EVENT_MESSAGE_COLUMN_NAME()
                    ]
                if sub_id_str.isdigit():
                    sub_id = int(sub_id_str)
                    self.add_event_extension(sub_id, str_message)
                else:
                    self.valid = False
                    self.errors.append(
                        f"Invalid Extension Meesage: the message has a invalid sub-id. SubId = {sub_id_str} - Message = {str_message}"
                    )


class Corpus(CorpusOperations):
    """This class abstracts the concept of Corpus.

    A Corpus is a set of prototypical conversations that represents
    the communication between different agents, typically a bot and one
    or more human users.

    TODO: document class methods.
    """
    DEFAULT_CORPUS_START_COLUMN = "A"
    DEFAULT_CORPUS_START_ROW = "2"
    DEFAULT_CORPUS_END_CELL = "N"
    DEFAULT_CORPUS_EXTENSION_END_CELL = "G"
    DEFAULT_CONFIGURATION_LOAD_DATA_INTERVAL = "load_data_interval"
    storage_manager = StorageManager()

    def __init__(
        self,
        spreadsheet_id: str,
        id,
        corpus_sheet_title: str,
        corpus_extension_sheet_title: str,
        tokenizer: BasicTokenizer,
        dictionary: Dictionary,
        regional_settings: str,
        annotable: bool,
        configuration_json=None,
        corpus_dataframe=None,
    ):
        self.valid = True
        self.contains_invalid_sceneries = False
        self.errors = []
        self.sceneries = {}
        self.invalid_sceneries = []
        self.spreadsheet_id = spreadsheet_id
        self.id = id
        self.corpus_sheet_title = corpus_sheet_title
        self.sheet_title = self.corpus_sheet_title
        self.corpus_extension_sheet_title = corpus_extension_sheet_title
        self.tokenizer = tokenizer
        self.dictionary = dictionary
        self.regional_settings = regional_settings
        self._annotable = annotable

        if configuration_json is not None:
            self.configuration = json.loads(configuration_json)
            temporal_sheets = self.storage_manager.get_temporal_sheets_from_new_to_old(
                self.spreadsheet_id, self.corpus_sheet_title
            )
            if (
                Corpus.DEFAULT_CONFIGURATION_LOAD_DATA_INTERVAL
                in self.configuration
            ):
                if (
                    len(temporal_sheets) == 0
                    or (
                        mammut.get_timezone_aware_datetime_now()
                        - temporal_sheets[0][2]
                    ).total_seconds()
                    > self.configuration[
                        Corpus.DEFAULT_CONFIGURATION_LOAD_DATA_INTERVAL
                    ]
                ):
                    self.dump_sheet_title = self.create_dump_sheet(
                        spreadsheet_id
                    )
                    self.corpus_sheet_title = self.dump_sheet_title
                    self.DEFAULT_CORPUS_RANGE = self.dump_sheet_title + "!A3"
                    self.load_data()
                    for ts in temporal_sheets:
                        self.storage_manager.delete_sheet(
                            spreadsheet_id, ts[0]
                        )
                else:
                    self.dump_sheet_title = temporal_sheets[0][1]
                    self.corpus_sheet_title = self.dump_sheet_title
                    self.DEFAULT_CORPUS_RANGE = self.dump_sheet_title + "!A3"

        if corpus_dataframe is not None:
            self.corpus_data_frame = corpus_dataframe
        else:
            self.corpus_data_frame = self.storage_manager.get_spreadsheet_as_dataframe(
                self.spreadsheet_id,
                self.corpus_sheet_title,
                self.DEFAULT_CORPUS_START_COLUMN,
                self.DEFAULT_CORPUS_START_ROW,
                self.DEFAULT_CORPUS_END_CELL,
            )
        self.sceneries_group_by_object = self.corpus_data_frame.groupby(
            CorpusTable.ID_COLUMN_NAME()
        )
        for g in self.sceneries_group_by_object:
            cse = self.get_corpus_scenario_entry_from_row(g)
            if len(cse.events) > 0:
                if cse.valid:
                    if cse.id not in self.sceneries:
                        self.sceneries[cse.id] = cse
                    else:
                        self.invalid_sceneries.append(cse)
                        self.valid = False
                        self.errors.append(
                            f"Invalid scenario ID: repeated id. Id = {cse.id}"
                        )
                else:
                    self.invalid_sceneries.append(cse)
                    self.valid = False
                    if not self.contains_invalid_sceneries:
                        self.contains_invalid_sceneries = True
                        self.errors.append("Contains invalid sceneries")
        if self.corpus_extension_sheet_title:
            self.corpus_ext_data_frame = self.storage_manager.get_spreadsheet_as_dataframe(
                self.spreadsheet_id,
                self.corpus_extension_sheet_title,
                self.DEFAULT_CORPUS_START_COLUMN,
                self.DEFAULT_CORPUS_START_ROW,
                self.DEFAULT_CORPUS_EXTENSION_END_CELL,
            )

            self.sceneries_ext_group_by_object = self.corpus_ext_data_frame.groupby(
                [CorpusTable.ID_COLUMN_NAME()]
            )
            for ge in self.sceneries_ext_group_by_object:
                str_id = ge[0]
                if str_id.isdigit():
                    id = int(str_id)
                    if id in self.sceneries:
                        self.sceneries[id].add_event_extensions(ge[1])
                        if not self.sceneries[id].valid:
                            self.valid = False
                            if (
                                self.sceneries[id]
                                not in self.invalid_sceneries
                            ):
                                self.invalid_sceneries.append(
                                    self.sceneries[id]
                                )
                            if not self.contains_invalid_sceneries:
                                self.contains_invalid_sceneries = True
                                self.errors.append(
                                    "Contains invalid sceneries"
                                )
                else:
                    if not self.contains_invalid_sceneries:
                        self.contains_invalid_sceneries = True
                        self.errors.append("Contains invalid sceneries")
                    self.valid = False
                    self.errors.append(
                        "Invalid Id: id in corpus extension is not a integer"
                    )

    def get_corpus_scenario_entry_from_row(self, g):
        raise NotImplementedError()

    def load_data(self):
        raise NotImplementedError()

    def create_dump_sheet(self, spreadsheet_id):
        temporal_sheet_title = self.storage_manager.create_temporal_new_sheet(
            spreadsheet_id, self.corpus_sheet_title
        )
        self.storage_manager.add_rows_to_spreadsheet(
            spreadsheet_id,
            temporal_sheet_title,
            CrawlerCorpusTable.DEFAULT_COLUMN_TITTLES,
            CrawlerCorpusTable.DEFAULT_START_ROW_TITTLE,
            CrawlerCorpusTable.DEFAULT_START_COLUMN_TITTLE,
        )
        return temporal_sheet_title

    def print_validation_result(self):

        output = []
        if self.valid:
            output.append("✔ El corpus es valido")
        else:
            output.append("✘ El corpus NO es valido")
            if len(self.errors) > 0:
                print(
                    f"Errores a nivel del corpus: ({len(self.errors)} errores)"
                )
                for e in self.errors:
                    print("\t" + e)
            if self.contains_invalid_sceneries:
                print("Errores a nivel de los escenarios:")
                for s in self.invalid_sceneries:
                    for es in s.errors:
                        print("\t" + es)
                    if s.contains_invalid_events:
                        print(
                            f"\tErrores a nivel de los eventos del escenario {s.str_id}:"
                        )
                        for ev in s.events:
                            if not ev.valid:
                                for eev in ev.errors:
                                    print("\t\t" + eev)

        return output

    @property
    def indexable(self) -> bool:
        return True

    @property
    def annotable(self) -> bool:
        return self._annotable

    def get_events_as_strings(self) -> List[str]:
        """
            Not implemented here, will require deep work.
        """
        raise NotImplementedError()


