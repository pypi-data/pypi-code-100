import torch
import numpy as np
import pandas as pd
from typing import Union

from src.utils.utils_embedding import cosine_sim_list


class BERTEmbedder:
    def __init__(self, model, tokenizer, df: Union[pd.DataFrame, None]):
        self.model = model
        self.tokenizer = tokenizer
        self.df = df

    def set_df(self, df: pd.DataFrame):
        self.df = df

    def mean_pooling(self, model_output, attention_mask):
        """
        Mean Pooling on a Transformer-based Architecture output.
        Takes the attention mask into account for correct averaging.
        """
        # first element of model_output contains all token embeddings
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(
            token_embeddings.size()).float()
        sum_embed = torch.sum(token_embeddings * input_mask_expanded, 1)
        mean_embed = sum_embed / torch.clamp(input_mask_expanded.sum(1),
                                             min=1e-9)

        return mean_embed

    def get_sentence_embedding(self, sentences):
        # Tokenize sentences
        encoded_input = self.tokenizer(sentences,
                                       padding=True,
                                       truncation=True,
                                       return_tensors='pt')

        # Compute token embeddings
        with torch.no_grad():
            model_output = self.model(**encoded_input)

        # Perform pooling. In this case, max pooling.
        sentence_embeddings = self.mean_pooling(
            model_output, encoded_input['attention_mask'])

        return sentence_embeddings

    def get_neighbors(self, sent: str, n=10):
        if self.df is not None:
            sentence_embeddings = self.get_sentence_embedding([sent])
            cos_sim = cosine_sim_list(sentence_embeddings[0].numpy(),
                                      np.asarray(self.df.embed))
            arg_max_sim = np.asarray(cos_sim).argsort()[-n:][::-1]
            df_neigh = self.df.iloc[arg_max_sim].copy(deep=True)
            df_neigh['cos_sim'] = np.take(cos_sim, arg_max_sim)
        else:
            raise ValueError('DataFrame needs to be defined for this.')

        return df_neigh
