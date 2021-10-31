from mammut.common.lexicon.linguistic_standard import LinguisticStandard
from typing import List
from mammut.common.synthetic.synthetic_corpus_generator.token_generator import TokenGenerator


class FunctionalGenerator(TokenGenerator):
    """Functional words generator Encapsulates the retrieval of
    functional words in the Standard.

    Only 'es' functional words are being retrieved, since only 'es'
    functional words are being loaded in the LinguisticStandard
    class.
    """

    POS_PARADIGM_COL_NAME = "pos-paradigm"
    LEMMA_COL_NAME = "lemma"

    def __init__(self, standard: LinguisticStandard):
        self.standard = standard
        self.func_df = standard.functionals_data_frame

    # Override abstract method
    def get_tokens(
        self, pos: str = "", regional_settings: str = "es"
    ) -> List[str]:
        if (
            pos != "PREP"
            and pos != "CONJ"
            and pos != "PRON"
            and pos != "AUX"
            and pos != "ART"
        ):
            return []

        func_pos = self.func_df[self.POS_PARADIGM_COL_NAME] == pos
        selected_df = self.func_df[func_pos]
        selected_df_values = set(selected_df[self.LEMMA_COL_NAME].values)
        if pos == "ART":
            selected_df_values.remove("zero-ES")
        ret = list(selected_df_values)
        return ret
