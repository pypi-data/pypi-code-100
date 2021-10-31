from mammut.common.storage.storage_manager import StorageManager
from mammut.common.catalog.hugging_face_datasets import TextOnly


class Catalog:
    """Catalog class allows find out interactively
     which documents do we have that are valid and
     meaningful.

     Attributes:
        catalog_data: Catalog class has a dataframe
            with the information of all internal documents
            (spreadsheet or presentations) that can used
            in different processes.
     """

    storage_manager = StorageManager()

    FEATURE_NAME_COLUMN = "source_name"
    FEATURE_TYPE_COLUMN = "source_type"
    FEATURE_SUBTYPE_COLUMN = "source_subtype"
    FEATURE_ID_COLUMN = "source_id"
    FEATURE_DESCRIPTION_COLUMN = "source_description"
    FEATURE_REGIONAL_SETTINGS_COLUMN = "regional_settings"
    FEATURE_DEFAULT_COLUMN = "default"

    def __init__(self):
        self.catalog_data = self.storage_manager.get_spreadsheet_as_dataframe(
            "1xwP87zj5m71-MtzTeAuwbGP2-FgPaM5imbVcCMcJudU",
            "catalog",
            "A",
            "1",
            "G",
            False,
        )

    def show_catalog_data(self):
        """Returns the complete catalog.
        """
        return self.catalog_data

    def show_info_source_type(self, source_type):
        """returns the catalog filtered by source_type.

        Arg:
            source_type(str): source type, it can be
            standard, package, documentation or
            annotated_corpus.
        """
        for r, c in self.catalog_data.iterrows():
            if c[Catalog.FEATURE_TYPE_COLUMN] == source_type:
                return (
                    c[Catalog.FEATURE_NAME_COLUMN],
                    c[Catalog.FEATURE_ID_COLUMN],
                )

    def get_default_id(self, source_type):
        """returns a default id of a standard document.

        Args:
            source_type(str): source type, it can be
            standard, package, documentation or
            annotated_corpus.
        """
        for r, c in self.catalog_data.iterrows():
            if c[Catalog.FEATURE_TYPE_COLUMN] == source_type:
                if c[Catalog.FEATURE_DEFAULT_COLUMN] == "TRUE":
                    return c[Catalog.FEATURE_ID_COLUMN]

    def get_standard_id_subtype(self, source_subtype, regional_settings):
        """Returns the id of some model developed by
        Mammut in English or Spanish.

        Args:
            source_subtype(str): standard document subtype,
            it can be conjunctions, com_conjunctions,
            prepositions, com_prepositions
            articles, deictics.

            regional_settings(str): model language, en or es.
        """
        for r, c in self.catalog_data.iterrows():
            if c[Catalog.FEATURE_TYPE_COLUMN] == "standard":
                if c[Catalog.FEATURE_SUBTYPE_COLUMN] == source_subtype:
                    if (
                        c[Catalog.FEATURE_REGIONAL_SETTINGS_COLUMN]
                        == regional_settings
                    ):
                        return c[Catalog.FEATURE_ID_COLUMN]

    def get_external_corpus(self, corpus_type):
        """Returns a corpus sentences made with a huggingface dataset.

        Arg:
            corpus_type(str): for now, this implementation only
            supports single feature dataset.
        """
        if corpus_type == "HF_TO":
            dataset = TextOnly()
            corpus = dataset.data_translator()
            return corpus
