import random
import torch

class SimpleMapTokenizer(object):
    r''' Not even really a tokenizer, will take a list of tokens and
    covert them to IDs

    Args:
        tkn2id
        pad_id
        max_len
    '''
    def __init__(self, tkn2id, pad_id, max_len=50, tkn2name=None):
        self.tkn2id = tkn2id
        self.pad_id = pad_id
        self.max_len = max_len
        self.tkn2name = tkn2name

        # Create id2tkn 
        self.id2tkn = {v:k for k,v in self.tkn2id.items()}


    def __call__(self, text, return_tensors=False):
        out = {'input_ids': [], 'attention_mask': []}

        out['input_ids'] = out['input_ids'] + [self.tkn2id[tkn] for tkn in text.split(" ")]
        if self.end_id is not None:
            out['input_ids'] = out['input_ids'] + [self.end_id]

        out['attention_mask'] = [1] * len(out['input_ids'])

        if return_tensors:
            out = {k:torch.tensor([v]) for k,v in out.items()}

        return out


    def decode(self, token_ids, get_names=True):
        tkns = self.convert_ids2tokens(token_ids, get_names=get_names)
        if type(tkns) != list:
            tkns = [tkns]
        return " ".join(tkns)


    def convert_ids2tokens(self, token_ids, get_names=True):
        if type(token_ids) == torch.Tensor:
            token_ids = token_ids.tolist()
        if type(token_ids) == list and type(token_ids[0]) == torch.Tensor:
            token_ids = [x.tolist() for x in token_ids]

        # Same as decode, but needed for compatibility with ecco
        out = []
        if type(token_ids) != list:
            out = [self.id2tkn[int(token_ids)]]
        else:
            # Convert tokens to IDs
            out = [self.id2tkn[int(id)] for id in token_ids]

        if get_names:
            _out = []
            for tkn in out:
                _out.append(self.tkn2name.get(tkn, tkn))
                #_out.append(" | ")
            out = _out

        return out



    def tokens_to_ids(self, tokens):
        r''' This will skip tokens if they are not in the tkn2id dict
        '''
        out = [self.tkn2id[tkn] for tkn in tokens if tkn in self.tkn2id]
        out = out[:self.max_len]

        return out


    def encode(self, examples):
        r''' Convert 'stream' in the examples from tokens to IDs, save as 'input_ids'. Use with HF datasets.map
        '''
        examples['input_ids'] = [self.tokens_to_ids(stream) for stream in examples['stream']]

        return examples
