# coding=utf-8
import sys
from typing import Any, Dict, List, Optional
from mammut.apps.corpus_compiler_service import CorpusCompilerService
from mammut.common.basic_tokenizer import BasicTokenizer
from mammut.common.corpus.corpus_map import CorpusMap
from mammut.common.indexer import CorpusIndexer, NGramIndexer
from mammut.common.lexicon.linguistic_standard import LinguisticStandard
from mammut.common.lexicon.dictionary import Dictionary
from mammut.common.lexicon.paradigm_producer import (
    ParadigmProducer,
    ParadigmProducerGroup,
)
from mammut.common.storage.storage_base import SheetsStorageBase
from mammut.linguistics.concordance import Concordance
from mammut.common.annotations import Restitution, MammutEventAnnotation
import mammut.visualization.lexicalization_widget as lexicalization_widget
import mammut.visualization.disambiguation_widget as disambiguation_widget
import mammut.visualization.annotations_widget as annotations_widget
import mammut.visualization.annotations_validator_widget as annotations_validator_widget
import mammut.visualization.widgets_utilities as widgets_utilities
from mammut.common.annotations import MammutAnnotations
from mammut.common.annotations_validator import CorpusAnnotationsValidator
from mammut.common.ngram import NGram
from mammut.common.corpus_transformer import *
from mammut.common.synthetic.synthetic_corpus_generator.morphemes_generator import (
    MorphemesGenerator,
)
from mammut.common.synthetic.synthetic_corpus_generator.synthetic_corpus_generator import (
    SyntheticCorpusGenerator,
)
from mammut.common.catalog.catalog_manager import Catalog
import logging
from IPython.display import display
from ipywidgets import widgets
import pandas as pd

from mammut.common.storage.storage_manager import StorageManager

log = logging.getLogger(__name__)


class Package:
    """The entrypoint class for Mammut Computational Linguistics Framework.
    Package class provides a client API for Computational Linguistics
    operations to work with structured, semi-structured and unstructured
    information supported by Mammut Framework.

    Args:
        package_id(str): ID of the presentation document. It can be a Google
            presentation ID or a local path to a .pptx file.
        standard_spreadsheet_id(str): ID of the standard document. It can be a Google
            presentation ID or a local path to a .pptx file.
        package_id_is_spreadsheet(bool): If True, package_id arg can be
            directly an ID of a package spreadsheet file.
    """

    storage_manager = StorageManager()

    def __init__(
        self,
        package_id: str,
        standard_spreadsheet_id: str,
        package_id_is_spreadsheet: bool = False,
        show_progress: bool = True,
        standard_base_sheet_title: str = "base",
        standard_dict_sources_sheet_title: str = "dict-sources",
        standard_pos_sheet_title: str = "pos-tags",
        standard_features_sheet_title: str = "features",
        standard_dimensions_sheet_title: str = "dimensions",
        dictionary_sheet_title: str = "dictionary",
        standard_functionals_sheet_title: str = "functionals",
        standard_non_functionals_sheet_title: str = "non-functionals",
        standard_primes_sheet_title: str = "primes",
        standard_synonym_sheet_title: str = "synonym",
        synonym_sheet_title: str = "synonym"
    ):
        # Start package loading
        log.info("Start loading package...")
        self.package_id_is_spreadsheet = package_id_is_spreadsheet
        self.spreadsheet_id = self._extract_spreadsheet_id_from_slide(
            package_id
        )
        self.main_id = package_id
        self.package_name = self.spreadsheet_id.lower()
        self.show_progress: bool = show_progress
        self.standard_spreadsheet_id = standard_spreadsheet_id
        self.standard_base_sheet_title = standard_base_sheet_title
        self.standard_dict_sources_sheet_title = standard_dict_sources_sheet_title
        self.standard_pos_sheet_title = standard_pos_sheet_title
        self.standard_features_sheet_title = standard_features_sheet_title
        self.standard_dimensions_sheet_title = standard_dimensions_sheet_title
        self.dictionary_sheet_title = dictionary_sheet_title
        self.standard_functionals_sheet_title = standard_functionals_sheet_title
        self.standard_non_functionals_sheet_title = standard_non_functionals_sheet_title
        self.standard_primes_sheet_title = standard_primes_sheet_title
        self.standard_synonym_sheet_title = standard_synonym_sheet_title
        self.synonym_sheet_title = synonym_sheet_title
        self.storage_manager.infer_spreadsheet_storage(package_id)
        self.tokenizer = BasicTokenizer()
        self.standard: Optional[LinguisticStandard] = None
        self.dictionary: Optional[Dictionary] = None
        self.synonym_sheet_title: str = "synonym"
        self.jde = lexicalization_widget
        self.disambiguation_widget = disambiguation_widget
        self.annotations_widget = annotations_widget
        self.annotations_validator_widget = annotations_validator_widget
        self.jde.DEFAULT_STANDARD = self.standard
        self.operation_counter = 0
        self.status_text_box = widgets.Text(
            value="Your package is being initialized!",
            disabled=True,
            layout=widgets.Layout(width="900px", height="120px"),
        )
        if self.show_progress:
            display(self.status_text_box)
        self.corpus_map: Optional[CorpusMap] = None
        self.corpus_indexer = CorpusIndexer()
        log.info("Indexer loaded")
        self.ngram_indexer = NGramIndexer()
        self.ngram_query = NGram()
        log.info("NGram handler loaded")
        self.concordance = Concordance()
        self.library = None
        self.restitution = Restitution(self, self.spreadsheet_id)
        log.info("Restitutions loaded")
        self.corpus_compiler_service = None
        self.paraphrases = None
        self.morphemes_generator: Optional[MorphemesGenerator] = None
        self.synthetic_corpus_generator: Optional[SyntheticCorpusGenerator] = None
        self.catalog: Optional[Catalog] = None
        self.annotations: Optional[MammutAnnotations] = None
        self.corpus_annotations_validator: Optional[CorpusAnnotationsValidator] = None
        log.info("Package loaded!!!")

    def load_main_classes(self):
        """Loads main classes LinguisticStandard, Dictionary, and CorpusMap.
        """
        self.standard = LinguisticStandard(
            self.standard_spreadsheet_id,
            self.standard_base_sheet_title,
            self.standard_dict_sources_sheet_title,
            self.standard_pos_sheet_title,
            self.standard_features_sheet_title,
            self.standard_dimensions_sheet_title,
            self.standard_functionals_sheet_title,
            self.standard_non_functionals_sheet_title,
            self.tokenizer,
            self.standard_primes_sheet_title,
            self.standard_synonym_sheet_title,
        )
        self.dictionary = Dictionary(
            self.spreadsheet_id,
            self.dictionary_sheet_title,
            self.synonym_sheet_title,
            self.tokenizer,
            self.standard,
            False,
            self.package_name,
        )
        self.corpus_map = CorpusMap(
            self.spreadsheet_id,
            self.tokenizer,
            self.dictionary,
            self.standard,
            self.catalog,
            self._update_status_text_box,
        )
        self._index_all_corpus()
        self.annotations = MammutAnnotations(self)
        self.corpus_annotations_validator = CorpusAnnotationsValidator(self)
        self.morphemes_generator = MorphemesGenerator(self.standard, self.dictionary)
        self.synthetic_corpus_generator = SyntheticCorpusGenerator(self.morphemes_generator)

    def _extract_spreadsheet_id_from_slide(self, presentation_id: str):
        """Extracts the spreadsheet_id from the presentation specified by
            presentation_id.

        Note:
            For local .pptx files, there may be runtime errors if the
            environment variable LOCAL_STORAGE_BASE_FOLDER is not set
            correctly. LOCAL_STORAGE_BASE_FOLDER refers to the local
            folder where the package resides.

        Args:
            presentation_id(str): Google presentation ID or local
                path to a .pptx file.

        Returns:
            If the presentation_id is a Google presentation, returns the
                spreadsheet_id from the Google Spreadsheet.

            If the presentation_id is a local path to a .pptx file, returns
                the absolute path to the .xlsx file found in the .pptx file
                entry for the spreadsheet_id.

            If self.package_id_is_spreadsheet, then the package_id class arg
                is returned immediately.
        """
        if self.package_id_is_spreadsheet:
            return presentation_id
        else:
            slide_elements = self.storage_manager.get_slide_elements(
                presentation_id
            )
            for pageElements in slide_elements:
                for element in pageElements:
                    if (
                        not re.search(
                            self.storage_manager.get_slides_metadata_re_string(
                                presentation_id
                            ),
                            element.content,
                        )
                        is None
                    ):
                        return re.search(
                            self.storage_manager.get_slides_metadata_re_string(
                                presentation_id
                            ),
                            element.content,
                        ).group(2)

    def get_custom_table(
        self,
        spreadsheet_id: str,
        sheet_title: str,
        start_cell: str = "A1",
        end_cell: str = "",
        transpose: bool = False,
    ) -> pd.DataFrame:
        """Get a Dataframe from a sheet in a spreadsheet.

        Todo:
            * Test method with local packages (.xlsx files)
            * Transpose support will be eventually removed.

        Args:
            spreadsheet_id(str): The ID of the Google Spreadsheet.
            sheet_title(str): sheet name in the Google Spreadsheet.
            start_cell(str): first cell of the range in A1 notation.
            end_cell(str): last cell of the range in A1 notation.
            transpose(bool): True if the sheet is written in transpose order.

        Returns:
            Returns the Pandas' Dataframe containing the specified sheet
                range.
        """
        data_frame = self.storage_manager.get_spreadsheet_as_dataframe(
            spreadsheet_id,
            sheet_title,
            start_cell[0],
            start_cell[1 : len(start_cell)],
            end_cell,
            transpose,
        )
        return data_frame

    def set_custom_table(
        self,
        spreadsheet_id: str,
        data_frame,
        sheet_title: str,
        start_row=SheetsStorageBase.DEFAULT_START_ROW,
        start_col=SheetsStorageBase.DEFAULT_START_COLUMN,
        is_update_cells: bool = False,
    ) -> str:
        """Save a Dataframe to a sheet in a spreadsheet.

        Todo:
            * Test method with local packages (.xlsx files)

        Args:
            spreadsheet_id(str): The ID of the Google Spreadsheet.
            data_frame(Dataframe): The Pandas' Dataframe to save.
            sheet_title(str): sheet name in the Google Spreadsheet.
            start_row(str): start row number in the spreadsheet.
            start_col(str): start column name in the spreadsheet.
            is_update_cells(bool): False to append data_frame.
                True will override cells if needed.

        Returns:
            Returns a string containing the A1 notation of the modified
            spreadsheet.
        """
        rows = data_frame.to_numpy().tolist()
        if not is_update_cells:
            return self.storage_manager.add_rows_to_spreadsheet(
                spreadsheet_id, sheet_title, rows, start_row, start_col
            )
        else:
            return self.storage_manager.update_rows_from_spreadsheet(
                spreadsheet_id, sheet_title, rows, start_row, start_col
            )

    def _index_all_corpus(self):
        """Index all corpus.

        Index all corpus using the configured backend
        (Elasticsearch at the moment of the doc).
        This is used by several other components to perform fast lookups over
        the corpus.
        """
        for corpus in self.corpus_map.get_all_corpus():
            if corpus.indexable:
                self.corpus_indexer.index_corpus(
                    corpus.corpus_data_frame,
                    corpus.spreadsheet_id,
                    corpus.corpus_sheet_title,
                    self.package_name,
                )

    def check_concordance(self, query_list: List[str]) -> widgets.HTML:
        """Checks concordance in a corpus.
            
        This method returns the concordance of one or more words
        in context of the events from the corpus noted in the corpus_map
        of the spreadsheet. A corpus is a collection of prototypical 
        conversations, while events are each of the messages in those
        conversations.

        Example:
            >>> input=(['restaurant'])
            >>> check_concordance(input)
            [
             this ____ restaurant, apart from being emblematic is affordable',
            'the ____ restaurant is very nice, they have a nice atmosphere',
            'I had very good recommendations from this ___________ restaurant'
            ]
            
        Args:
            query_list (List[str]): list of lemmas to check concordance for.
                
        Returns:
            Returns all concordance occurrences of one or more words in
                HTML format.
        """
        concordance_results = []
        for query in query_list:
            concordance_results.append(
                self.concordance.get_data_from_index(self.package_name, query)
            )
        concordance_html = lexicalization_widget.concordance_template.render(
            {"concordance_results": concordance_results}
        )
        return widgets.HTML(value=concordance_html)

    def check_concordance_for_lemma(self, lemma: str) -> widgets.HTML:
        """Checks the concordance of a lemma in the corpus. 
        
        This method returns the concordance of a specific lemma
        in context of the events from the corpus (C, N, M) noted in the
        corpus_map of the spreadsheet. Through this method developers can
        check all concordance occurrences of a lemma, also, they can see all
        the inflections of a lemma that exist in events of the corpus
        declared. A corpus is a collection of prototypical conversations,
        while events are each of the messages in those conversations.

        Example:
            >>> input='have'
            >>> check_concordance_for_lemma(input)
            ['we do not _____ have this service',
            'do you _____ have a website ?',
            'in addition to our coffees we also _____ have natural juices']

        Args:
            lemma: word to check concordance for.

        Returns:
            Returns all concordance occurrences of a lexicalized lemmas in
                HTML format.
        """
        concordance_results = []
        query_list = self.dictionary.get_morphemes_of_lemma(lemma)
        for query in query_list:
            concordance_results.append(
                self.concordance.get_data_from_index(self.package_name, query)
            )
        concordance_html = lexicalization_widget.concordance_template.render(
            {"concordance_results": concordance_results}
        )
        return widgets.HTML(value=concordance_html)

    def show_defined_lemmas(self, date: str) -> pd.DataFrame:
        """This method shows lemmas or words defined in a specific date.

        Example:            
            >>> package.show_defined_lemmas('2019/05/20')

        Args:
            date (str): date to check. The date parameter must be a in the
                format ('YYYY/MM/DD') supported by Elasticsearch.
                https://www.elastic.co/guide/en/elasticsearch/reference/current/date.html

        Returns:
            Returns a Pandas' Dataframe with lemmas defined in the
            date specified.
        """
        l_d = self.dictionary.definition_indexer.get_defined_lemmas(date)
        return widgets_utilities.create_defined_words_section(l_d)

    def show_lexicalization_widget(self):
        """Shows the lexicalization widget view.
            
        The lexicalization widget is a tool that allows developers to create 
        an internal lexicon or dictionary from the words present in each of 
        the events of the corpus declared in the corpus map of a spreadsheet. 
        The words present in the events of a corpus are incorporated into 
        the internal dictionary through lexicalization.

        Returns:
            Displays a box containing various add-ons. 
            Through these add-ons it is possible to define a word.
            Returns the view of the lexicalization widget. 
        """
        all_box = lexicalization_widget.show_restart_add_lemma_entry_section_button(
            self.dictionary, self.package_name
        )

        def search_for_lemma(sender):
            """This method shows a box in the lexicalization widget that
            permits the developer to enter a specific word, and search a
            definition of it in the dictionaries available:
            Word-Reference, RAE, Oxford, or Wiktionary.
            """
            new_accordion = lexicalization_widget.create_external_dictionaries_section(
                all_box.children[1].children[0].children[0].value.lower(),
                self.dictionary.standard,
                all_box.children[1].children[0].children[3].value,
            )
            for i in range(0, len(all_box.children[1].children[1].children)):
                all_box.children[1].children[1].set_title(
                    i, new_accordion.get_title(i)
                )
            all_box.children[1].children[1].children = new_accordion.children

        def handle_restart_section_button_click(sender):
            """Handles the words browser in the lexicalization widget.
                
            Returns:
                Resets the section to search words in the lexicalization
                    widget.
            """
            all_box.children = [
                all_box.children[0],
                lexicalization_widget.create_lemma_section(
                    self.dictionary, self.package_name
                ),
            ]
            all_box.children[1].children[0].children[4].on_click(
                search_for_lemma
            )

        all_box.children[0].on_click(handle_restart_section_button_click)
        all_box.children[1].children[0].children[4].on_click(search_for_lemma)
        return all_box

    def _update_status_text_box(self, new_value: str = ""):
        """Updates the progress widget when the Package is loading.

        """
        self.operation_counter = self.operation_counter + 1
        standar_text = "Operation number: " + str(self.operation_counter)
        if new_value:
            value = standar_text + " --- extra info: " + new_value
        else:
            value = standar_text
        self.status_text_box.value = value

    def add_restitution(
        self, event_annotation: MammutEventAnnotation, restitution_input: str
    ):
        """Adds a word in a corpus event.
            
        The 'add restitution' component is a section that is part of 
        the annotation widget. Through this component, developers can add 
        a word which is also part of a specific event in a corpus, 
        but that word does not appear in the event explicitly.
        The word that does not appear in the event explicitly is an ellipsis.
        Ellipsis is the omission from a clause of one 
        or more words that are nevertheless understood 
        in the context of the remaining elements.
        This component allows developers to add the
        restitution in the initial position of the event. 
        This method is used directly by the annotation widget. 
        The annotation widget has the data that points to the corpus, 
        scenario, and corpus event that requires restitution. 
        The annotation widget passes the required MammutEventAnnotation 
        given user interaction.

        #TODO: Example must use MammutEventAnnotation class
        Example:
            >>> input='Just saying!'
            >>> resitution='I'
            >>> add_restitution(input, restitution)
            'I just saying'
        
        TODO: 
            * Currently, this method only places the restitution
            in the initial position of the event. 
            * The method should allow developers to choose
            the location of the event where restitution is needed. 

        Args:
            event_annotation (MammutEventAnnotation): corpus event to be
                annotated.
            restitution_input (str): the word that does not appear in the
                event explicitly. (Ellipsis)

        """
        deleted_restitutions = self.delete_restitutions(event_annotation)
        restitutions = [restitution_input.lower()] + deleted_restitutions
        ordered_restitutions = restitutions[::-1]
        for rest in ordered_restitutions:
            self.restitution.add_restitution(
                event_annotation.event["corpus"]["name"],
                event_annotation.event[
                    MammutEventAnnotation.SCENARIO_INDEX_ID
                ],
                event_annotation.event["event_entry"],
                event_annotation.event["tokenized_message_index"],
                rest,
            )
        event_annotation.update_documents_after_restitution(
            " ".join(restitutions)
        )
        self.annotations.delete_all_annotations(event_annotation)

    def delete_restitutions(
        self, event_annotation: MammutEventAnnotation
    ) -> List[str]:
        """Deletes all restored words in a corpus event.

        The 'delete restitution' component is a section that is part of 
        the annotation widget. Through this component, developers can delete 
        all words that were previously restored for a specific event in a
        corpus.

        #TODO: Example must use event annotation class
        Example:
            >>> input= 'I just saying!'
            >>> delete_restitution(input, restitution)
            'Just saying!'

        Args:
            event_annotation (MammutEventAnnotation): corpus event to be annotated.

        #TODO: Verify the meaning of the return value.
        Returns:
            Returns the number of deleted restitutions.
        """
        deleted_restitutions = self.restitution.delete_restitutions(
            event_annotation
        )
        deleted_restitutions = event_annotation.update_documents_after_delete_restitution(
            deleted_restitutions
        )
        self.annotations.delete_all_annotations(event_annotation)
        return deleted_restitutions

    def show_annotation_widget(self):
        """Shows the annotation widget view. 
            
        The annotation widget is a tool that allows developers 
        to annotate each of the events that make up a corpus. 
        Through the annotation widget developers can tag all 
        relevant information required for the design of their chatbot. 
            
        Returns:
            Returns the view of the annotation widget.
        """
        annotation_widget = self.annotations_widget.annotations_widget_section(
            self
        )
        return annotation_widget

    def show_annotations_validator_widget(self):
        annotations_validator_widget = self.annotations_validator_widget.get_validator_widget(
            self
        )
        return annotations_validator_widget

    def show_invalid_spans_table(self):
        invalid_spans_table = self.annotations_validator_widget.get_invalid_spans_list(
            self
        )
        return invalid_spans_table

    def show_functionals_help_widget(self):
        functionals_help_widget = self.annotations_widget.functionals_help_widget_section(
            self
        )
        return functionals_help_widget

    def show_disambiguation_widget(self):
        """Shows the disambiguation widget view.

        The disambiguation widget is a tool that allows developers
        to access all ambiguous lemma inputs.
        Ambiguity occurs when a word is susceptible to two or more
        meanings and interpretations, so the same word can be 
        understood in different ways. 
        Therefore, through the disambiguation widget developers 
        can disambiguate a lemma with multiple inputs to the lexicon.
        Developers can identify and select the appropriate meaning of a lemma 
        within the corpus and lexicon.
            
        Developers can disambiguate:
        Non-functional lemmas: nouns, adjectives, verbs and adverbs.
        Developers can select the appropriate meaning of a word within
        the corpus and lexicon. 
            
        Functional lemmas: prepositions, articles, pronouns, conjunctions. 
        Developers can choose the prototypical scheme that
        identifies the function of a lemma in a context.
        Also, developers can also create their own word classes. 
        Nouns, adjectives, articles are classes that are delivered with
        the standard, but other custom classes can be built.

        Returns:
            Returns the view of the disambiguation widget .
        """
        disambiguation_widget = self.disambiguation_widget.disambiguation_widget_section(
            self
        )
        return disambiguation_widget

    def test_paradigm(
        self,
        word_model: str,
        grammar: str,
        descriptions: Dict[str, Any],
        words: List[str],
        regional_settings: str,
        words_inflections: List = [],
    ) -> widgets.widget_box.VBox:
        """Tests a morphological paradigm in a word.

        This method allows developers to test a morphological paradigm
        of a word.
        Through morphological paradigms developers can see the inflections
        of a specific word.
        The morphological paradigms are constructed according to the following
        syntax:
        - Commands and characters can be combined in any way.
        - The FEATURES that you want to associate to a rule are combined with
            the '+' sign and separated from the commands with a '/'.
        - A paradigm can contain many concatenated rules using the '|' as a
            separator.
        - The created paradigms can be reused to create new paradigms in the
            same excel sheet or in some other simply by referencing them like
            this: <sheet:word_model>.

        Commands:
        <E>: Empty element. The word is not modified in any way.
        <L[#]>: Pointer.  One or more characters to the left.
        <R[#]>: Pointer.  One or more characters to the right.
        <A>: Deletes the check mark from the character.
        <B[#]>: Delete one or more characters and move the pointer to the left.
        <Á>: Adds an acute accent to the pointed vowel.
        <Ä>: Adds dieresis/trema/umlaut to the pointed vowel.

        Args:
            word_model (str): is a word that allows to identify the paradigm.
            grammar (str): morphological rule in the form of grammar following
                the syntax explained above.
            descriptions (Dict[str, Any]): a description for each kind of
                feature specified in the grammar.
            words: contains a set of words on which the rule in grammar
                will be tested.
            regional_settings: specifies the language of the input.
                Use 'es' for Spanish or 'en' for English.
            words_inflections (List[str]): contains a list of the inflections
                of a word.
                
        Returns:
            Returns a list table view of inflected words.
        """
        res = []
        producer_group = ParadigmProducerGroup(
            "", self.standard, regional_settings
        )
        producer = ParadigmProducer(
            word_model, grammar, False, descriptions, producer_group
        )
        for i in range(0, len(words)):
            ms = producer.apply(words[i])
            wi = []
            if len(words_inflections) != 0:
                wi = words_inflections[i]
            res.append(widgets_utilities.show_paradigm(ms, wi))
        return widgets.VBox(res)

    def test_paradigm_excel(
        self,
        pos_id: str,
        word_model: str,
        words,
        regional_settings,
        words_inflections=[],
    ):
        res = []
        for i in range(0, len(words)):
            ms = self.standard.get_morphemes(
                pos_id, word_model, words[i], regional_settings
            )
            wi = []
            if len(words_inflections) != 0:
                wi = words_inflections[i]
            res.append(widgets_utilities.show_paradigm(ms, wi))
        return widgets.VBox(res)

    def create_conjugator_section(
        self, verb: str, language_tool: str = "es-wr"
    ):
        """Creates a verb conjugation section.

        This method allows the developer to check the conjugation of a verb 
        in Spanish according to wordreference.com and in English according
        to verbix.com website.

        Args:
            verb (str): verb to be conjugated.
            language_tool (str): language of the input.
                Use 'es-wr' for Spanish (Word Reference website) or
                'en' for English (Verbix website).

        Returns:
            Creates a conjugation section and returns the conjugation of a
                verb in the language selected.
        """
        res = widgets_utilities.create_conjugator_section(verb, language_tool)
        return res

    def create_rae_conjugation_section(self):
        """The method shows the RAE models of verbal conjugation. 

        Through this method the developers can see some tables
        that show the model for the conjugation of regular and irregular
        verbs.
        
        Returns:
             Returns the view of the RAE conjugation models.
        """
        res = widgets_utilities.create_rae_conjugation_section()
        return res

    def clean_word_reference_conjugation(self, list_str: str) -> List[str]:
        """Cleans Word Reference conjugator section.

        The 'clean word reference conjugation' method allows you get a list
        of verb inflections from the conjugation section of Word Reference
        website. This method cleans or erases unnecessary characters in order
        to get a "clean list" able to be used in any purpose need it.

        Example:
            >>> input = '''I read
            >>> you read
            >>> he
            >>> she
            >>> it reads
            >>> we read
            >>> you read
            >>> they read'''
            >>>
            >>> self.creat_conjugation_section(input)
            ['read', 'read', 'reads', 'read', 'read', 'read', 'read']

        Args:
            list_str (str): list of inflections of a verb from the conjugation
                section of Word Reference website.

        Returns:
            Returns a clean list of the inflections of a verb.
        """
        list_split = list_str.split("\n")
        list_res = []
        for c in list_split:
            i = c.find("\t")
            c_n = c[i + 1 :] if i > 0 else c
            list_res.append(c_n)
            print(c_n)
        return list_res

    def get_ready_lemmas_table(
        self,
        regional_settings: str,
        layer: int = 0,
        as_data_frame: bool = True,
    ):
        """Gets ready lemmas table from.
        
        The 'ready lemmas table' is a plug-in to the lexicalization widget.
        This table allows developers to see the lemmas that are part of
        the events in the corpus and that have been lexicalized.
        This table includes lexicalized lemmas coming directly from
        corpus events (level 1) as well as lemmas coming from definitions
        created by the developer in previous lexicalization
        stages (level 2 or higher).

        Ready lemmas can be one of:
            - lemmas that has been lexicalized
            - functional lemmas
            - semantic primes
            - synonyms

        Args:
            regional_settings: specifies the language of the lexicon. 
                Use 'es' for Spanish or 'en' for English.
            layer: specifies the level of the lexicon. Zero-based. 
            as_data_frame: specifies the format of the return
                to be a pandas Dataframe. If False, Renders the widget_string
                value as HTML.
                
        Returns:
            Returns the view of a table of already lexicalized lemmas to
            the level indicated in the layer argument.
        """
        return widgets_utilities.create_ready_words_section(
            self.dictionary, regional_settings, layer, as_data_frame
        )

    def get_pending_words_table(
        self,
        regional_settings: str,
        layer: int = 0,
        as_data_frame: bool = True,
    ):
        """Gets pending words table.

        In the process of creation of a lexicon or internal dictionary, 
        the 'pending words table' allows the developer to identify words
        that have not been lexicalized. 'Pending words' are words that come
        from the events of a corpus (level 1) or from definitions created by
        the developer in previous stages of lexicalization (level 2 or higher)

        Args:
            regional_settings (str): specifies the language of the lexicon.
                Use 'es' for Spanish or 'en' for English.
            layer (int): specifies the level of the lexicon. Zero-based.
            as_data_frame (bool): specifies the format of the return to be a
                Pandas' DataFrame. If False, renders the widget_string value
                as HTML.

        Returns:
            Returns the view of a table with words that have not been
            lexicalized at the specified level.
        """
        return widgets_utilities.create_pending_words_section(
            self.dictionary, regional_settings, layer, as_data_frame
        )

    def get_undefined_functionals_table(
        self, regional_settings: str, as_data_frame: bool = True
    ):
        """Gets undefined functional table.

        The 'undefined functionals table' component is a plug-in to the
        lexicalization widget. Through this add-on developers can see all
        functional words that are part of the corpus to be lexicalized.
        The words shown in this table are functional words that have not been
        modeled through Mammut's cognitive models.

        These models organize and analyze the functionality of words in
        discourse. Each of the words that are part of the events of the corpus
        belongs to a category:

        Non-functional words are those that can be defined through the
        lexicalization widget. Example: Nouns, adjectives, verbs and adverbs.

        Functional words are those that can be defined through the
        lexicalization widget. Example: Pronouns, articles, prepositions, and
        conjunctions. These functional words are treated separately in
        the lexicon.
        
        Args:
            regional_settings: specifies the language of the lexicon. 
                Use 'es' for Spanish or 'en' for English.
            as_data_frame: specifies the format of the return
                to be a pandas' Dataframe. If False, Renders the widget_string
                value as HTML.

        Returns:
            Returns the view of a table with the functional words not defined
            in the lexicon
        """
        return widgets_utilities.create_undefined_functionals_section(
            self.standard, regional_settings, as_data_frame
        )

    def get_all_ready_lemmas_table(
        self, regional_settings: str, as_data_frame: bool = True
    ):
        """Gets all ready lemmas table.

        The 'all ready lemmas table' is a plug-in to the lexicalization
        widget. This table allows developers to see all the lemmas that are
        part of the events in the corpus and that have been lexicalized.

        This table includes lexicalized lemmas coming directly from corpus
        events (level 1) as well as lemmas coming from definitions created
        by the developer in previous lexicalization stages (level 2 or higher)

        All ready lemmas can be one of:
            - lemmas that has been lexicalized
            - functional lemmas
            - semantic primes
            - synonyms

        Args:
            regional_settings: specifies the language of the lexicon. 
                Use 'es' for Spanish or 'en' for English.
            as_data_frame: specifies the format of the return
                to be a pandas' Dataframe. If False, Renders the widget_string
                value as HTML.

        Returns:
            Returns the view of a table with all the words that have been
            lexicalized.
        """
        return widgets_utilities.create_ready_words_section(
            self.dictionary, regional_settings, sys.maxsize, as_data_frame
        )

    def get_all_pending_words_table(
        self, regional_settings: str, as_data_frame: bool = True
    ):
        """This method gets all pending words table.

        In the process of creation of a lexicon or internal dictionary, 
        the 'all pending words table' allows the developer to identify all
        words that have not been lexicalized. 'Pending words' are words that
        come from the events of a corpus (level 1) or from definitions created
        by the developer in previous stages of
        lexicalization (level 2 or higher).

        Args:
            regional_settings (str): specifies the language of the lexicon.
                Use 'es' for Spanish or 'en' for English.
            as_data_frame (bool): specifies the format of the return to be a
                Pandas' DataFrame. If False, renders the widget_string value
                as HTML.

        Returns:
            Returns the view of a table with words of all levels which have
            not been lexicalized.
        """
        return widgets_utilities.create_pending_words_section(
            self.dictionary, regional_settings, sys.maxsize, as_data_frame
        )

    def get_words_in_definitions_out_of_vocabulary(
        self, regional_settings: str, as_data_frame: bool = True
    ):
        """This method allows the developer to know which words out of the
        lexicon could be lexicalized.
        
        These are words found in the lexicalized definitions
        that the developer builds through the lexicalization process.
        
        For the Framework a word is considered 'out of the vocabulary' if it
        is not present neither in the annotable corpus nor in the list of
        functional and non-functional words of the Standard, nor in the list
        of synonyms or primes.

        Args:
            regional_settings (str): specifies the language of the lexicon.
                Use 'es' for Spanish or 'en' for English.
            as_data_frame (bool): specifies the format of the return to be a
                Pandas' DataFrame. If False, renders the widget_string
                value as HTML.

        Returns:
            Returns the view of a table with all the words in the vocabulary.
        """
        return widgets_utilities.create_words_in_definitions_out_of_vocabulary_section(
            self.dictionary, regional_settings, as_data_frame
        )

    def show_lexicalization_evolution(self, regional_settings: str):
        """This method shows a line graph representing data on the evolution
        and size of the lexicon.

        This graph helps the developer to know the relationship between the
        amount of lexicalized lemmas and the amount of words that have not
        been lexicalized, in order to see how close, the lexicon is to have
        a balance.

        Args:
            regional_settings (str): specifies the language of the lexicon.
                Use 'es' for Spanish or 'en' for English.

        Returns:
            Returns the plot of the lexicalization evolution.
        """
        widgets_utilities.show_lexicalization_evolution(
            self.tokenizer, regional_settings
        )

    def get_lexicalization_statistics(self, regional_settings: str):
        """This method collects statistics of the lexicon about number of
        lemmas, number of definitions, number of morphemes, number of
        lexicalized lemmas, and number of undefined words.

        Example:
            >>> self.get_lexicalization_statistics('es')
            LexicalizationStatistics(
              lemmas_count=675,
              definitions_count=804,
              morphemes_count=11356,
              words_count=654,
              undefined_words_count=38
              )


        Args:
            regional_settings (str): specifies the language of the lexicon.
                Use 'es' for Spanish or 'en' for English.

        Returns:
            Returns lexicalization statistics. 
        """
        return self.dictionary.get_lexicalization_statistics(regional_settings)

    def get_similar_phrases(
        self, corpus_name: str, corpus_type: str, query: str
    ) -> List[str]:
        """Looks in a corpus for all phrases similar to one provided.
        
        Through this method developers can look at a corpus (N, M, C) 
        all phrases similar to a phrase provided as input. 
        This method checks the phrase provided as input and returns 
        outputs similar to the input. 
        Semantic similarity in the area of natural language processing
        is the measure of the interrelationship between any two words
        in a text.
        Two words or terms have a similar context because they exist in 
        the same document. It is understood that these two words are related,
        and therefore their semantic distance can be deduced.
        However, in this context, two phrases are considered similar 
        if the output phrases have a meaning close to the input phrase. 
        Two phrases are similar if one can be used instead of the other.
        
        Example: 
            >>> package.get_similar_phrases(
            >>> 'corpus_degusta',
            >>> CorpusMap.DEFAULT_CRAWLER_TYPE,
            >>> 'un buen lugar para almorzar'
            >>> )
            
            [
            'Que buen local,la atencion es muy buena y el ambiente excelente',
            'El mejor ambiente para cenar. Totalmente recomendado.',
            'encantada con este sitio, vale la pena darse el gusto.',
            'Comidas deliciosas y con un ambiente muy calido.',
            'Variedad de platos de excelente calidad recomendado.',
            'Me parece muy buen restaurante aunque un poco costoso.',
            'Excelente atención, y un menú de primera',
            'Definitivamente uno de los mejores lugares para comer sushi',
            'Muy bueno de verdad muy buena opción en la ciudad'
            ]

        Args:
            corpus_name (str): name of the corpus to check.
            corpus_type (str): type of the corpus to check.
            query (str): phrase which we are looking similarities for.

        Returns:
            Returns a list of similar phrases found in the corpus specified.
            Specifically, the method returns 10 output sentences similar
            to input query sentence.
        """
        if self.paraphrases is None:
            from mammut.linguistics.paraphrases import Paraphrases

            self.paraphrases = Paraphrases(self)

        return self.paraphrases.get_similar_phrases(
            corpus_name, corpus_type, query
        )

    # Templates temporal

    def span_calculator(
        self, dataframe: pd.DataFrame, source: List[str], target: List[str]
    ):
        """Span Calculator

        This method takes a source list with the variables to substitute in
        the annotations and a target list with the words to be included in
        the annotations. Then, shows a Dataframe that has the annotation of
        a single sentence, on a single level.
        
        Args:
            dataframe: Pandas' object that has the annotation of a single
                sentence, on a single level
            source(list): list with the variables to substitute in the
                annotations.
            target(list): list with the words to be included in the
                annotations

        Returns:
            Shows the Dataframe with the changes.
        """
        span_series = []
        original_span_series = []

        for num_variable in range(len(source)):
            variable = source[num_variable]
            variant = target[num_variable]
            if num_variable == 0:
                for s in dataframe[dataframe.text == variable].span:
                    previous_span = (
                        s  # Mejorar esta forma de seleccionar un span
                    )
            else:
                previous_span = new_span_series[num_variable]
            growth = len(variant) - len(variable)
            try:
                start = int(previous_span[0])
            except UnboundLocalError:
                print(
                    "Error: La palabra <<{0}>> no se encuentra en el dataframe".format(
                        source[num_variable]
                    )
                )
                break

            # Obtención de los spans originales:

            if len(span_series) == 0:
                for i in dataframe.span:
                    try:
                        if str(type(i)) == """<class 'str'>""":
                            comma_pos = i.find(",")
                            span_tuple = (
                                int(i[:comma_pos]),
                                int(i[comma_pos + 1 :]),
                            )
                            span_series.append(span_tuple)
                            original_span_series.append(span_tuple)
                        else:
                            span_series.append("nan")
                    except:
                        span_series.append("nan")

            new_span_series = []
            for j in span_series:
                if str(type(j)) == """<class 'tuple'>""":
                    if j[0] == start:
                        new_span_tuple = (start, j[1] + growth)
                    elif j[0] > start:
                        new_span_tuple = (j[0] + growth, j[1] + growth)
                    elif j[0] < start and j[1] <= start:
                        new_span_tuple = (j[0], j[1])
                    else:
                        new_span_tuple = (j[0], j[1] + growth)
                    new_span_series.append(new_span_tuple)
                else:
                    new_span_series.append("nan")
            span_series = new_span_series

            dataframe = dataframe.replace({variable: variant}, regex=True)

        # Remplazar los spans en la columna span:

        for span in range(len(new_span_series)):
            if str(type(new_span_series[span])) == """<class 'tuple'>""":
                dataframe.iloc[span, 2] = str(new_span_series[span])[
                    1:-1
                ].replace(" ", "")
            else:
                continue

        # Remplazar los spans en otras columnas:

        corpus_name = (
            dataframe.iloc[0, 0][: dataframe.iloc[0, 0].find("SP")] + "SP-"
        )
        for n in range(len(original_span_series)):
            if str(type(original_span_series[n])) == """<class 'tuple'>""":
                first_number, second_number = (
                    original_span_series[n][0],
                    original_span_series[n][1],
                )
                id_regex = re.compile(corpus_name + r"(\d){1,4}-0-0")
                sentence_num = id_regex.search(dataframe.iloc[0, 0]).group(1)
                source_id = "{3}{0}-0-0-{1}-{2}-".format(
                    sentence_num, first_number, second_number, corpus_name
                )
                target_id = "{3}{0}-0-0-{1}-{2}-".format(
                    sentence_num,
                    str(new_span_series[n][0]),
                    str(new_span_series[n][1]),
                    corpus_name,
                )
                dataframe = dataframe.replace(
                    {source_id: target_id}, regex=True
                )
            else:
                continue

        return dataframe

    def id_replace(self, dataframe: pd.DataFrame, id_number: int):
        """ID Replace

        This method accepts as a second argument a number that will indicate 
        the number of the annotated sentence.

        Args:
            dataframe: Pandas' object that has the annotation of a single
                sentence, on a single level.
            id_number(int): number that will indicate the number of the
                annotated sentence.
        
        Returns:
            Shows the Dataframe.
        """
        corpus_name = (
            dataframe.iloc[0, 0][: dataframe.iloc[0, 0].find("SP")] + "SP-"
        )
        id_regex = re.compile(corpus_name + r"(\d+)-0-0")
        sentence_num = id_regex.search(dataframe.iloc[0, 0]).group(1)
        source_id = "{0}{1}-0-0".format(corpus_name, sentence_num)
        print(source_id)
        target_id = "{0}{1}-0-0".format(corpus_name, str(id_number))
        dataframe = dataframe.replace({source_id: target_id}, regex=True)
        return dataframe

    def build_synthetic_corpus(
        self,
        nouns_words: int,
        adjective_words: int,
        verbs_words: int,
        nouns_bound: int,
        adjectives_bound: int,
        verbs_bound: int,
        free_lemmas_word: int,
        random_ext: int
    ):
        """Returns a synthetic corpus using the provided guidelines

        Args:
            nouns_words(int): number of times that a noun bound morpheme
                will appear in company of a random free morpheme.
            adjective_words(int): number of times that an adjective bound
                morpheme will appear in company of a random free morpheme.
            verbs_words(int): number of times that a verb bound morpheme
                will appear in company of a random free morpheme.
            nouns_bound(int): number of times that a noun bound morpheme
                will appear alone in the corpus.
            adjectives_bound(int): number of times that an adjective
                bound morpheme will appear alone in the corpus.
            verbs_bound(int): number of times that a verb bound morpheme
                will appear alone in the corpus.
            free_lemmas_word(int): number of times that a free morpheme
                will appear in the corpus with a random suffix.

        Returns
            A list of strings. Each string is a word in the synthetic
            corpus.
        """
        return self.synthetic_corpus_generator.generate_synthetic_corpus(
            nouns_words,
            adjective_words,
            verbs_words,
            nouns_bound,
            adjectives_bound,
            verbs_bound,
            free_lemmas_word,
            random_ext
        )

    def get_all_bound_morphemes(self, regional_settings: str) -> List[str]:
        """Retrieve all the bounded morphemes founded in package.
        All the bound morphemes are retrieved for all POS and
        for the specified regional_settings.

        Todo: Only 'es' regional setting is supported.
        Todo: Only POS nouns, adjectives and some verbs models are
            supported

        Each returned element will be a string composed of the
        free morpheme in a randomly altered form and the bound
        morpheme.
        Args:
            regional_settings(str): language of the bound morphemes
                models
        Returns:
            A list containing the words composed of the altered
            free morpheme and the bound morpheme.
        """
        ret = self.morphemes_generator.get_tokens("NOUN", regional_settings)
        ret = ret + self.morphemes_generator.get_tokens(
            "ADJ", regional_settings
        )
        ret = ret + self.morphemes_generator.get_tokens(
            "VERB", regional_settings
        )
        return ret

    def compile_corpus_list(
        self,
        mammut_id: int,
        compilation_message_callback,
        corpus_ids: List[str],
    ):
        """Used to compile a Mammut bot.

        Args:
            mammut_id(int): the bot user ID in the API database.
            compilation_message_callback: callback to update the simulator
                widget output.
            corpus_ids(List[str]): list of corpus IDs to compile according
                to the corpus_map sheet.

        """
        if self.main_id is not None:
            if self.corpus_compiler_service == None:
                self.corpus_compiler_service = CorpusCompilerService()
            return self.corpus_compiler_service.compile(
                mammut_id,
                self.main_id,
                True,
                "en",
                "->",
                corpus_ids,
                compilation_message_callback,
            )
        else:
            compilation_message_callback(
                "Error: para compilar se debe especificar "
                "un presentation id como paquete",
                None,
            )

    @staticmethod
    def image_retraining(
        self, directory: str, mammut_id: int, samples: int = 50,
    ):
        # TODO:Debemos separar todo lo relacionado con vision
        # Para asi no forzar que siempre se deba instalar ciertas librerias.
        from mammut.models.imaging.mammut_image_retraining import (
            augmentate_and_retrain,
        )

        return augmentate_and_retrain(directory, mammut_id, samples,)

    def get_image_retraining_widget(self, mammut_user):
        # TODO:Debemos separar todo lo relacionado con vision
        # Para asi no forzar que siempre se deba instalar ciertas librerias.
        from mammut.visualization.image_retraining_widget import (
            get_image_retraining_widget,
        )

        return get_image_retraining_widget(self, mammut_user)

    @staticmethod
    def validate_challenge(class_name: str,
                           public_field_name: str,
                           private_field_name: str,
                           property_name: str,
                           public_instance_method_name: str,
                           public_static_method_name: str):
        """Hello, I'll help you to validate your challenge.

        For this challenge you shall write a Class. Whatever class you want,
        but ensure that your class has:
            - A public field name
            - A private field name
            - A property name
            - An instance method name
            - A class method (static) name

        If your class has constructor parameters, ensure that they have a default
        value.

        I need the following args:

        Args:
            class_name(str): The name of the class that you've defined above.
            public_field_name(str): The name of the public field
            private_field_name(str): The name of the private field
            property_name(str): The name of the property
            public_instance_method_name(str): The name of the instance method.
            public_static_method_name(str): The name of the class method.

        Returns:
            "Success, you've made it!" if correct
            "Test failed" if failed. And maybe some hint :)
        """
        import sys
        from types import FunctionType
        obj = getattr(sys.modules['__main__'], class_name)

        # Test class method
        try:
            static_mth = obj.__dict__[public_static_method_name]
            if not isinstance(static_mth, staticmethod) and not isinstance(static_mth, classmethod):
                return f"Test failed: Class method {public_static_method_name} not found :("
        except:
            return f"Test failed: Class method {public_static_method_name} not found :("

        # Test instance method
        try:
            instance_mth = obj.__dict__[public_instance_method_name]
            if not isinstance(instance_mth, FunctionType):
                return f"Test failed: Instance method {public_instance_method_name} not found :("
        except:
            return f"Test failed: Instance method {public_instance_method_name} not found :("

        # Test class property
        try:
            prop = obj.__dict__[property_name]
            if not isinstance(prop, property):
                return f"Test failed. Property {property_name} not found :("
        except:
            return f"Test failed. Property {property_name} not found :("

        try:
            instance = obj()
        except:
            return f"Test failed. Does your class has default values for constructor parameters?"

        fields = vars(instance)
        if not public_field_name in fields and not public_field_name in obj.__dict__:
            return f"Test failed. Public field {public_field_name} not found :("

        if not private_field_name in fields and not private_field_name in obj.__dict__:
            return f"Test failed. Private field {private_field_name} not found :("

        return "Success, you've made it!"





