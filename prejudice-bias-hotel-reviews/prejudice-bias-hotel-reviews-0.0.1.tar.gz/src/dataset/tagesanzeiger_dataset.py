import pandas as pd
import pickle5 as pickle

from typing import Union
from sklearn.model_selection import train_test_split

from src.dataset.utils import TokenizerType
from src.dataset.base_dataset import BaseDataset
from src.preprocessing.preprocessor import Preprocessor


class TagesanzeigerDataset(BaseDataset):

    DATA_COLUMN = 'text'
    LABEL_COLUMN = 'rejected'

    def __init__(self,
                 dataset_path: str,
                 tokenizer_name: Union[str, None],
                 tokenizer_type: TokenizerType,
                 model_path: str = 'models/',
                 SEED=42):
        """
        Initializes the TagesanzeigerDataset dataset.

        This dataset specifies the binary classification problem to predict
        if a sentence is rejected or not.

        Parameters
        ----------
        dataset_path : str
            Path to the dataset file.
        tokenizer_name : Union[str, None]
            Name of the Huggingface tokenizer to use,
            if no Huggingface model is used set None.
        tokenizer_type : TokenizerType
            Type of tokenizer to use.
        model_path : str
            Path to the model directory.
        SEED : int
            Random seed to use (for reproducibility).

        Raises
        ------
        ValueError:
            Gets raised if an unknown tokenizer type is specified.
        """
        super().__init__(dataset_path=dataset_path,
                         tokenizer_name=tokenizer_name,
                         tokenizer_type=tokenizer_type,
                         use_umlaute=False,
                         SEED=SEED)

        # define a preprocessor
        self.preprocessor = Preprocessor(fasttext_model_path=model_path,
                                         remove_hashtags=False,
                                         merge_cols=False)

        # load the dataset
        with open(self.dataset_path / 'data_cleaned.pkl', "rb") as fh:
            self.df = pickle.load(fh)

        # split into train (68%)/val (12%)/test (20%) set
        self.df_train, self.df_test = train_test_split(self.df,
                                                       test_size=0.2,
                                                       random_state=SEED)
        self.df_train, self.df_val = train_test_split(self.df_train,
                                                      test_size=0.15,
                                                      random_state=SEED)
        self.df_train, self.df_val = train_test_split(self.df_train,
                                                      test_size=0.15,
                                                      random_state=SEED)
        # prepare the dataframe
        self._prepare_df()

        # get the tokenizer
        self.tokenizer = self._get_tokenizer()
