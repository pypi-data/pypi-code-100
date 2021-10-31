from brat_widget import Document

from mammut.common.lexicon.mammut_brat_configuration import (
    MammutBratConfiguration,
)


class MammutBratDocument(Document):
    def __init__(self, tokenized_message, config: MammutBratConfiguration):
        self.tokenized_message = tokenized_message
        # TODO: El manejo de offsets que espera el BRAT WIDGET no es el mismo que tenemos
        # Debemos definir correctamente esto.
        Document.__init__(
            self,
            self.tokenized_message.original_text,
            [],  # self.tokenized_message.token_offsets,
            self.tokenized_message.sentence_offsets,
            config,
        )
