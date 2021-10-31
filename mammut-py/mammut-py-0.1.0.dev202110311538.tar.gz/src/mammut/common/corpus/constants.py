from enum import Enum


class CorpusTable(Enum):
    """
    Enum with the list of constant required by the Corpus table.
    """

    # Column names
    ID_COLUMN_NAME = "id"
    SUB_ID_COLUMN_NAME = "sub_id"
    SCENARIO_TYPE_COLUMN_NAME = "scenario_type"
    EVENT_MESSAGE_COLUMN_NAME = "event_message"
    HIDDEN_COLUMN_NAME = "hidden"
    FIELD_COLUMN_NAME = "field"
    LAMBDA_CONDITION_COLUMN_NAME = "lambda_condition"
    UI_EVENT_COLUMN_NAME = "ui_event"
    ACTION_COLUMN_NAME = "action"
    SOURCE_COLUMN_NAME = "source"
    REGIONAL_SETTINGS_COLUMN_NAME = "regional_settings"
    COMPLEXITY_COLUMN_NAME = "complexity"
    ISSUE_TYPE_COLUMN_NAME = "issue_type"
    DATE_COLUMN_NAME = "date"
    # Other constants
    MAMMUT_USERS_PREFIX = "mammut"

    def __repr__(self):
        return str(self.value)

    def __call__(self, *args, **kwargs):
        return str(self.value)


class CrawlerCorpusTable:
    """Data class to encapsulate Crawler Corpus default
    constant values.

    Defined here to avoid circular dependencies.
    """
    DEFAULT_COLUMN_TITTLES = [
        [
            CorpusTable.ID_COLUMN_NAME(),
            CorpusTable.SUB_ID_COLUMN_NAME(),
            CorpusTable.SCENARIO_TYPE_COLUMN_NAME(),
            CorpusTable.EVENT_MESSAGE_COLUMN_NAME(),
            CorpusTable.HIDDEN_COLUMN_NAME(),
            CorpusTable.FIELD_COLUMN_NAME(),
            CorpusTable.SOURCE_COLUMN_NAME(),
            CorpusTable.REGIONAL_SETTINGS_COLUMN_NAME(),
            CorpusTable.COMPLEXITY_COLUMN_NAME(),
        ]
    ]
    DEFAULT_COLUMN_TITTLE_RANGE = "!A2"
    DEFAULT_START_COLUMN_TITTLE = "A"
    DEFAULT_START_ROW_TITTLE = "2"
    URL_KEY = "url"
    NODES_PATTERN_KEY = "nodes_pattern"
    NODE_ELEMENT_KEY = "node_elements"
    PAGE_HREF_KEY = "page_href"
    DEFAULT_PAGES_LIMIT_KEY = "pages_limit"
    PAGINATION_NODE_PATTERN_KEY = "pagination_node_pattern"
    PAGINATION_NODE_ELEMENT_KEY = "pagination_node_element"
    DEFAULT_SCENARIO_TYPE_VALUE = "Monologue"
    DEFAULT_EVENT_MESSAGE_VALUE = ""
    DEFAULT_HIDDEN_VALUE = ""
    DEFAULT_FIELD_VALUE = ""
    DEFAULT_SOURCE_VALUE = "CrawlerCorpus"
    DEFAULT_COMPLEXITY_VALUE = ""
    DEFAULT_CRAWLING_PERIOD = 86400  # 1 day



