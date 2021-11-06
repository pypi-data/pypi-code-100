import torch
import opencc
from pathlib import Path
from transformers import BertTokenizer, BertConfig, BertModel


class AnchiBert:

    def __init__(self, model_path=None):
        if model_path is None:
            model_path = 'AnchiBERT/'
            if not Path(model_path).is_dir():
                _download_bert_model()

        # Bert initialization
        print(f'Loading AnchiBERT model from {model_path} ...')
        config = BertConfig.from_pretrained(model_path)
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.model = BertModel.from_pretrained(model_path,config=config)

        # Traditional to simplified chinese
        self.t2s = opencc.OpenCC('t2s.json')


    def encode_sentence(self, sent:str, idx_from:int=None, idx_to:int=None, is_traditional=True):
        """Encode a raw sentence as a vector

        Parameters
        ----------
        sent : str
            The sentence to encode.
        idx_from : int, optional
            Begining index of a token in the :code:`sent`, 
            by default None.
        idx_to : int, optional
            Ending index of a token in the :code:`sent`, 
            by default None. If :code:`idx_from` or 
            :code:`idx_to` is None, the sentence would be
            encoded by summing all tokens' vectors from the
            last hidden state in the Bert model. Otherwise,
            the subset of tokens in :code:`sent` as specified 
            by :code:`(idx_from, idx_to)` are used.
        is_traditional : bool, optional
            [description], by default True

        Returns
        -------
        numpy.ndarray
            A :code:`(768,)` numpy.ndarray array.
        """
        if is_traditional: sent = self.t2s.convert(sent)
        input = self.tokenizer(sent, return_tensors="pt")
        last_hidden_state = self.model(**input)[0]

        # Sentence vector (sum all tokens together)
        if idx_from is None or idx_to is None:
            return torch.sum(last_hidden_state[0, :, :], dim=0).detach().numpy()
        # Token vector (sum subset of tokens together)
        return torch.sum(last_hidden_state[0, (idx_from+1):(idx_to+2), :], dim=0).detach().numpy()


def _download_bert_model():
    print("Downloading AnchiBert model ...")
    import gdown
    gdown.download('https://drive.google.com/uc?id=1uMlNJzilEhSigIcfjTjPdYOZL9IQfHNK', quiet=False, output="AnchiBERT.zip")
    gdown.extractall("AnchiBERT.zip")
