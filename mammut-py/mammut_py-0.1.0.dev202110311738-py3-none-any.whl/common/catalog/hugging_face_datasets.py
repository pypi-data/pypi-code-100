from datasets import load_dataset
from datasets import Dataset


class TextOnly:
    """TextOnly class is one of the dataset
    possibilities that can be used in mammut
    processes.
    """
    def data_translator(self):
        """Returns a pandas dataframe with the data of the
        single feature dataset.
        """
        sentences: Dataset = load_dataset("ptb_text_only", subset=None, split="train")
        sentences_df = sentences.data.to_pandas()
        return sentences_df
