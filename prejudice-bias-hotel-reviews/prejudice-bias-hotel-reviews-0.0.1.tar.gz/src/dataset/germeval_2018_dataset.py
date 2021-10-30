import pandas as pd

from typing import Union
from sklearn.model_selection import train_test_split

from src.dataset.utils import TokenizerType
from src.dataset.base_dataset import BaseDataset
from src.preprocessing.preprocessor import Preprocessor


class GermEval2018Dataset(BaseDataset):

    DATA_COLUMN = 'text'
    LABEL_COLUMN = 'lbl1'

    def __init__(self,
                 dataset_path: str,
                 tokenizer_name: Union[str, None],
                 tokenizer_type: TokenizerType,
                 model_path: str = 'models/',
                 SEED=42):
        """
        Initializes the GermEval2018Dataset dataset.

        This dataset specifies the binary classification problem to predict
        if a sentence is offensive or not.

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
        self.df_train = pd.read_table(self.dataset_path / 'germeval2018.training.txt', header=None)
        self.df_train.columns = ['text', 'lbl1', 'lbl2']
        self.df_train = self.df_train.drop(columns=['lbl2'])
        self.df_test = pd.read_table(self.dataset_path / 'germeval2018.test.txt', header=None)
        self.df_test.columns = ['text', 'lbl1', 'lbl2']
        self.df_test = self.df_test.drop(columns=['lbl2'])

        # split into train (85%) / val (15%) set
        self.df_train, self.df_val = train_test_split(self.df_train,
                                                      test_size=0.15,
                                                      random_state=SEED)
        # prepare the dataframe
        self._prepare_df()

        # get the tokenizer
        self.tokenizer = self._get_tokenizer()
