import pandas as pd

from typing import Union
from sklearn.model_selection import train_test_split

from src.dataset.utils import TokenizerType
from src.dataset.base_dataset import BaseDataset
from src.preprocessing.preprocessor import Preprocessor


class HateDataset(BaseDataset):

    DATA_COLUMN = 'text'
    LABEL_COLUMN = 'label'

    def __init__(self,
                 dataset_path: str,
                 tokenizer_name: Union[str, None],
                 tokenizer_type: TokenizerType,
                 germeval_name: str = 'GermEval-2018',
                 hasoc_name: str = 'HASOC-2019',
                 model_path: str = 'models/',
                 SEED=42):
        """
        Initializes the HateDataset dataset, combination of GermEval and HASOC.

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
        germeval_name : str
            Name of the GermEval-2018 folder.
        hasoc_name : str
            Name of the HASOC-2019 folder.
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

        # load the HASOC dataset
        self._load_hasoc_dataset(hasoc_name)
        # load the GermEval dataset
        self._load_germeval_dataset(germeval_name)

        # combine the datsets
        self.df_train = self.df_hasoc_train.append(self.df_germ_train)
        self.df_test = self.df_hasoc_test.append(self.df_germ_test)

        # reset the index to truly combine datasets
        self.df_train = self.df_train.reset_index(drop=True)
        self.df_test = self.df_test.reset_index(drop=True)

        # split into train (85%) / val (15%) set
        self.df_train, self.df_val = train_test_split(self.df_train,
                                                      test_size=0.15,
                                                      random_state=SEED)

        # prepare the dataframe
        self._prepare_df()

        # get the tokenizer
        self.tokenizer = self._get_tokenizer()

    def _load_hasoc_dataset(self, hasoc_path):
        self.df_hasoc_train = pd.read_csv(self.dataset_path / hasoc_path /
                                          'german_dataset.tsv',
                                          sep='\t')
        self.df_hasoc_train = self.df_hasoc_train.drop(
            columns=['text_id', 'task_2'])
        self.df_hasoc_test = pd.read_csv(self.dataset_path / hasoc_path /
                                         'hasoc_de_test_gold.tsv',
                                         sep='\t')
        self.df_hasoc_test = self.df_hasoc_test.drop(
            columns=['text_id', 'task_2'])

        # bring into correct format
        self.df_hasoc_train['task_1'] = self.df_hasoc_train[
            'task_1'].str.replace('HOF', 'HATE')
        self.df_hasoc_test['task_1'] = self.df_hasoc_test[
            'task_1'].str.replace('HOF', 'HATE')

        self.df_hasoc_train.columns = ['text', 'label']
        self.df_hasoc_test.columns = ['text', 'label']

    def _load_germeval_dataset(self, germeval_path):
        self.df_germ_train = pd.read_table(self.dataset_path / germeval_path /
                                           'germeval2018.training.txt',
                                           header=None)
        self.df_germ_train.columns = ['text', 'lbl1', 'lbl2']
        self.df_germ_train = self.df_germ_train.drop(columns=['lbl2'])
        self.df_germ_test = pd.read_table(self.dataset_path / germeval_path /
                                          'germeval2018.test.txt',
                                          header=None)
        self.df_germ_test.columns = ['text', 'lbl1', 'lbl2']
        self.df_germ_test = self.df_germ_test.drop(columns=['lbl2'])

        # bring into correct format
        self.df_germ_train['lbl1'] = self.df_germ_train['lbl1'].str.replace(
            'OFFENSE', 'HATE')
        self.df_germ_test['lbl1'] = self.df_germ_test['lbl1'].str.replace(
            'OFFENSE', 'HATE')
        self.df_germ_train['lbl1'] = self.df_germ_train['lbl1'].str.replace(
            'OTHER', 'NOT')
        self.df_germ_test['lbl1'] = self.df_germ_test['lbl1'].str.replace(
            'OTHER', 'NOT')

        self.df_germ_train.columns = ['text', 'label']
        self.df_germ_test.columns = ['text', 'label']
