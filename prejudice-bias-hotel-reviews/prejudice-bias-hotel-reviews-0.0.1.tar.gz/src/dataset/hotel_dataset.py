import torch
from pathlib import Path
from torch.utils.data import Dataset
from tokenizers.implementations import ByteLevelBPETokenizer
from tokenizers.processors import BertProcessing


class HotelDataset(Dataset):

    MAX_LENGTH = 512

    def __init__(self,
                 evaluate: bool = False,
                 data_path: str = 'data/hotel-reviews/transformed/',
                 tokenizer_path: str = 'models/'):
        # define the data path and tokenizer path
        data_path = Path(data_path)
        save_path = Path(tokenizer_path)

        # define the tokenizer
        tokenizer = ByteLevelBPETokenizer(
            str(save_path / 'HotelBERT' / "vocab.json"),
            str(save_path / 'HotelBERT' / "merges.txt"),
        )
        tokenizer._tokenizer.post_processor = BertProcessing(
            ("</s>", tokenizer.token_to_id("</s>")),
            ("<s>", tokenizer.token_to_id("<s>")),
        )
        tokenizer.enable_truncation(max_length=self.MAX_LENGTH)

        self.examples = []
        src_files = data_path.glob("*-val.txt") if evaluate else data_path.glob("*-train.txt")
        for src_file in src_files:
            print("🔥", src_file)
            lines = src_file.read_text(encoding="utf-8").splitlines()
            self.examples += [x.ids for x in tokenizer.encode_batch(lines)]

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, i):
        # pad at the batch level
        return torch.tensor(self.examples[i])
