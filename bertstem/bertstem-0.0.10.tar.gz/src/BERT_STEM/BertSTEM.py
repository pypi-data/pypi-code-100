import torch
import numpy as np
import pandas as pd
import transformers

from BERT_STEM.Encode import *
from BERT_STEM.TrainBERT4PT import *

class BertSTEM:
    
    def __init__(self, model_name = None):
        
        if model_name is not None:
            self.model_name = model_name

        else:
            self.model_name = "pablouribe/bertstem"

        self._model = transformers.BertModel.from_pretrained(self.model_name)

        self._tokenizer = transformers.BertTokenizerFast.from_pretrained("dccuchile/bert-base-spanish-wwm-uncased",
                                                                         do_lower_case = True,
                                                                         add_special_tokens = False)

    def _encode_df(self, df, column, encoding):

        return(sentence_encoder(df, self._model, self._tokenizer, column, encoding))

    def _train_bert_for_pretraining(self, text, checkpoint):
        
        model = transformers.BertForPreTraining.from_pretrained(checkpoint)
        
        tokenizer = transformers.BertTokenizerFast.from_pretrained("dccuchile/bert-base-spanish-wwm-uncased",
                                                                   do_lower_case = True,
                                                                   add_special_tokens = False)

        train_Bert4PT(model, tokenizer, text)

    def _get_text_from_files(self, files_path):

        return(get_text_from_files(files_path))
