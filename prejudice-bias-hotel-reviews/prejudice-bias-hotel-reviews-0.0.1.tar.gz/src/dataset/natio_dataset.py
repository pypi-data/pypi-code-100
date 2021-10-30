import pandas as pd

from ast import literal_eval
from typing import Union
from sklearn.model_selection import train_test_split

from src.dataset.utils import TokenizerType
from src.preprocessing.preprocessor import Preprocessor
from src.dataset.base_dataset import BaseDataset


class NationalityDataset(BaseDataset):

    DATA_COLUMN = 'text'
    TOKEN_COLUMN = 'tokens'
    LABEL_COLUMN = 'prediction'

    def __init__(self,
                 dataset_path: str,
                 tokenizer_name: Union[str, None],
                 tokenizer_type: TokenizerType,
                 use_umlaute: bool = False,
                 SEED=42):
        """
        Initializes the nationality dataset.

        This dataset specifies the binary classification problem to predict
        if a sentence contains a nationality reference or not.

        Parameters
        ----------
        dataset_path : str
            Path to the dataset file.
        tokenizer_name : Union[str, None]
            Name of the Huggingface tokenizer to use,
            if no Huggingface model is used set None.
        tokenizer_type : TokenizerType
            Type of tokenizer to use.
        use_umlaute : bool
            If the dataset should contain umlaute or not,
            i.e. `False` all umlautes will be `ae` and `True` umlaute will be ä.
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
                         use_umlaute=use_umlaute,
                         SEED=SEED)

        # load the dataset
        self.df = pd.read_csv(self.dataset_path, index_col=0)
        # prepare the dataframe
        self._prepare_df()

        # split into train (68%)/val (12%)/test (20%) set
        self.df_train, self.df_test = train_test_split(self.df,
                                                       test_size=0.2,
                                                       random_state=SEED)
        self.df_train, self.df_val = train_test_split(self.df_train,
                                                      test_size=0.15,
                                                      random_state=SEED)

        self.tokenizer = self._get_tokenizer()

    def _prepare_df(self):
        # filter out the marked ones
        self.df = self.df[self.df[self.LABEL_COLUMN] != 'X']
        # evaluate the list of tokens
        self.df[self.TOKEN_COLUMN] = self.df[self.TOKEN_COLUMN].apply(
            literal_eval)
        # if needed apply backtransformation of non-umlaute to umlaute
        if self.use_umlaute:
            self.df[self.DATA_COLUMN] = self.df[self.DATA_COLUMN].apply(
                lambda x: Preprocessor.apply_umlaut(x))
        # transform the predictions into numeric values
        self.df[self.LABEL_COLUMN] = self.labelencoder.fit_transform(
            self.df[self.LABEL_COLUMN])
