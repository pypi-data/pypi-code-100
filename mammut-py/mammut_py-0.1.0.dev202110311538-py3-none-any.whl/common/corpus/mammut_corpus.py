from mammut.common.basic_tokenizer import BasicTokenizer
from mammut.common.corpus.constants import CorpusTable
from mammut.common.corpus.corpus_base import (
    CorpusEventEntry,
    CorpusScenarioEntry,
    Corpus,
)
from mammut.common.lexicon.dictionary import Dictionary


class MammutCorpusEventEntry(CorpusEventEntry):
    def __init__(
        self,
        sub_id: int,
        str_message: str,
        str_field: str,
        str_lambda_condition: str,
        str_complexity: str,
        str_source: str,
        str_regional_settings: str,
        str_ui_event: str,
        str_action: str,
        tokenizer: BasicTokenizer,
        dictionary: Dictionary,
        scenario_entry,
    ):
        CorpusEventEntry.__init__(
            self,
            sub_id,
            str_message,
            str_field,
            str_complexity,
            str_source,
            str_regional_settings,
            tokenizer,
            dictionary,
            scenario_entry,
        )
        self.str_action = str_action
        self.str_ui_event = str_ui_event
        self.lambda_condition = str_lambda_condition
        self.source = self.str_source
        self.valid = False
        self.errors.append(f"Invalid Source")


class MammutCorpusScenarioEntry(CorpusScenarioEntry):
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
        CorpusScenarioEntry.__init__(
            self,
            str_id,
            str_type,
            scenerie_group_by_object,
            tokenizer,
            dictionary,
            language_settings,
            corpus,
        )

    def get_corpus_event_entry_from_event_row(self, index, e):
        event_mesage = ""
        if (
            CorpusTable.EVENT_MESSAGE_COLUMN_NAME() in e[1]
            and e[1][CorpusTable.EVENT_MESSAGE_COLUMN_NAME()]
        ):
            event_mesage = e[1][CorpusTable.EVENT_MESSAGE_COLUMN_NAME()]

        return MammutCorpusEventEntry(
            index,
            event_mesage,
            e[1][CorpusTable.FIELD_COLUMN_NAME()]
            if CorpusTable.FIELD_COLUMN_NAME() in e[1]
            else "",
            e[1][CorpusTable.LAMBDA_CONDITION_COLUMN_NAME()]
            if CorpusTable.LAMBDA_CONDITION_COLUMN_NAME() in e[1]
            else "",
            e[1][CorpusTable.COMPLEXITY_COLUMN_NAME()]
            if CorpusTable.COMPLEXITY_COLUMN_NAME() in e[1]
            else "",
            e[1][CorpusTable.SOURCE_COLUMN_NAME()]
            if CorpusTable.SOURCE_COLUMN_NAME() in e[1]
            else "",
            e[1][CorpusTable.REGIONAL_SETTINGS_COLUMN_NAME()],
            e[1][CorpusTable.UI_EVENT_COLUMN_NAME()]
            if CorpusTable.UI_EVENT_COLUMN_NAME() in e[1]
            else "",
            e[1][CorpusTable.ACTION_COLUMN_NAME()]
            if CorpusTable.ACTION_COLUMN_NAME() in e[1]
            else "",
            self.tokenizer,
            self.dictionary,
            self,
        )

    def validate_corpus_event_entry(
        self, index, cee, last_event_source, last_event_is_from_mammut
    ):
        CorpusScenarioEntry.validate_corpus_event_entry(
            self, index, cee, last_event_source, last_event_is_from_mammut
        )
        # Validations at event level
        if cee.is_from_mammut and last_event_is_from_mammut:
            self.valid = False
            if index == 0:
                self.errors.append(
                    f"Invalid sequence of events: first event is from mammut. Id = {self.str_id} - SubId = {index}"
                )
            else:
                self.errors.append(
                    f"Invalid sequence of events: two consecutive events from mammut. Id = {self.str_id} - SubId = {index}"
                )


class MammutCorpus(Corpus):
    def __init__(
        self,
        spreadsheet_id: str,
        id,
        corpus_sheet_title: str,
        corpus_extension_sheet_title: str,
        corpus_variables_sheet_title: str,
        tokenizer: BasicTokenizer,
        dictionary: Dictionary,
        regional_settings: str,
        annotable: bool,
    ):
        self.corpus_variables_sheet_title = corpus_variables_sheet_title
        Corpus.__init__(
            self,
            spreadsheet_id,
            id,
            corpus_sheet_title,
            corpus_extension_sheet_title,
            tokenizer,
            dictionary,
            regional_settings,
            annotable,
        )

    def get_corpus_scenario_entry_from_row(self, g):
        return MammutCorpusScenarioEntry(
            g[0][0],
            g[1].iloc[0][CorpusTable.SCENARIO_TYPE_COLUMN_NAME()],
            g[1],
            self.tokenizer,
            self.dictionary,
            self.regional_settings,
            self,
        )
