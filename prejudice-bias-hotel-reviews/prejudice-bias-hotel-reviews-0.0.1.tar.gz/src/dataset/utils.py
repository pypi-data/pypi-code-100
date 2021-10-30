import nltk
import pandas as pd
from enum import Enum

from src.preprocessing.preprocessor import Preprocessor


class Dataset(Enum):
    GERM_EVAL = 0
    HASOC = 1
    COMBINED_HATE = 2
    NATIONALITY = 3
    GERM_EVAL_2021 = 4
    TAGESANZEIGER = 5


class DatasetType(Enum):
    """
    Enum that specifies what dataset to use.

    TRAIN: used to train the model.
    VAL: used to evaluate the model.
    TEST: used to test the model.
    """
    TRAIN = 0
    VAL = 1
    TEST = 2


class TokenizerType(Enum):
    """
    Enum that specifies what tokenizer to use for preprocessing the dataset.

    NONE: don't use a tokenizer.
    TOKENS: use sklearn tokenizer.
    HUGGINGFACE: use HuggingFace AutoTokenizer to determine.
    """
    NONE = 0
    TOKENS = 1
    HUGGINGFACE = 2


def load_ethnicities(file_path,
                     model,
                     add_neigh=True,
                     add_plural=True,
                     add_adj=True,
                     remove_umlaut=True,
                     return_df=False) -> pd.DataFrame:
    # make sure that punctuation from nltk is loaded
    nltk.download('punkt', quiet=True)

    # load the ethnicities file
    ethnien = pd.read_csv(file_path, delimiter='\t')
    ethnien = ethnien.astype(str)
    ethnien = ethnien.replace('nan', '', regex=True)

    # preprocess the ethnicities file
    for col in ethnien.columns:
        ethnien[col] = ethnien[col].apply(lambda x: x.split(','))

    if return_df:
        return ethnien

    # get a list of the nationalities
    demonyme = [item.strip() for sublist in ethnien['Einwohner'] for item in sublist]

    if add_neigh:
        # enhance list with nearest neighbors using a FastText model
        demonyme_neigh = [model.get_nearest_neighbors(demonym, k=15)[0] for demonym in demonyme]
        demonyme_neigh = [demonym[1] for demonym in demonyme_neigh]

        # filter out strings that are longer than 30 chars and are only lowercase
        demonyme_neigh = [x for x in demonyme_neigh if len(x) < 30 and x.lower() != x]
        # combine both lists
        demonyme = set(demonyme + demonyme_neigh)

    if add_plural:
        # pluralize the nationalities
        demonyme = set(list(demonyme) + [Preprocessor.pluralize(word) for word in demonyme])
        demonyme.discard('')

    if add_adj:
        # adjectives for nationalities
        demonyme_adj = [item.strip() for sublist in ethnien['Adjektiv'] for item in sublist]
        demonyme = set(list(demonyme) + demonyme_adj)
        demonyme.discard('')

    if remove_umlaut:
        # remove umlaute
        demonyme = [Preprocessor.remove_umlaut(word) for word in demonyme]

    return list(demonyme)
