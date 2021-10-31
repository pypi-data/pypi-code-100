from mammut.common.basic_tokenizer import BasicTokenizer
from mammut.common.corpus.constants import CorpusTable
from mammut.common.corpus.corpus_base import (
    CorpusEventEntry,
    CorpusScenarioEntry,
    Corpus,
)
from mammut.common.lexicon.dictionary import Dictionary


class IssueCorpusEventEntry(CorpusEventEntry):
    def __init__(
        self,
        sub_id: int,
        str_message: str,
        str_source: str,
        str_issue_type: str,
        str_date: str,
        str_regional_settings: str,
        tokenizer: BasicTokenizer,
        dictionary: Dictionary,
        scenario_entry,
    ):
        CorpusEventEntry.__init__(
            self,
            sub_id,
            str_message,
            "",
            "",
            str_source,
            str_regional_settings,
            tokenizer,
            dictionary,
            scenario_entry,
        )

        self.issue_type = str_issue_type
        self.date = str_date


class IssueCorpusScenarioEntry(CorpusScenarioEntry):
    def __init__(
        self,
        str_id,
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

        return IssueCorpusEventEntry(
            index,
            event_mesage,
            e[1][CorpusTable.SOURCE_COLUMN_NAME()]
            if CorpusTable.SOURCE_COLUMN_NAME() in e[1]
            else "",
            e[1][CorpusTable.ISSUE_TYPE_COLUMN_NAME()],
            e[1][CorpusTable.DATE_COLUMN_NAME()],
            e[1][CorpusTable.REGIONAL_SETTINGS_COLUMN_NAME()],
            self.tokenizer,
            self.dictionary,
            self,
        )

    def validate_corpus_event_entry(
        self, index, cee, last_event_source, last_event_is_from_mammut
    ):
        if not cee.valid and not self.contains_invalid_events:
            self.valid = False
            self.contains_invalid_events = True
            self.errors.append("Contains invalid events")
            self.errors.extend(cee.errors)


class IssueCorpus(Corpus):
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
        return IssueCorpusScenarioEntry(
            g[0][0],
            "Dialogue",
            g[1],
            self.tokenizer,
            self.dictionary,
            self.regional_settings,
            self,
        )
