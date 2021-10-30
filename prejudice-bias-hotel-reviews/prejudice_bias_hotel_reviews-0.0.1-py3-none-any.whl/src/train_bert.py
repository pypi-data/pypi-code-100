import wandb
import logging
import torch

from pathlib import Path
from transformers import RobertaConfig
from transformers import RobertaTokenizerFast
from transformers import RobertaForMaskedLM
from transformers import DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments
from tokenizers import ByteLevelBPETokenizer
from tokenizers.implementations import ByteLevelBPETokenizer

from src.dataset.hotel_dataset import HotelDataset

logging.disable(logging.WARNING)


def train_model():
    tokenizer = RobertaTokenizerFast.from_pretrained(
        str(save_path / 'HotelBERT'),
        max_len=max_len
    )

    # define the model
    config = RobertaConfig(
        vocab_size=vocab_size,
        max_position_embeddings=max_len + 2,
        num_attention_heads=12,
        num_hidden_layers=6,
        type_vocab_size=1,
    )
    model = RobertaForMaskedLM.from_pretrained(str(save_path / 'HotelBERT'),
                                               config=config)

    # define the datasets
    dataset = HotelDataset()
    dataset_val = HotelDataset(evaluate=True)

    # define the data collator for the MLM objective
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer,
                                                    mlm=True,
                                                    mlm_probability=0.15)
    training_args = TrainingArguments(
        output_dir=str(save_path / 'HotelBERT'),
        overwrite_output_dir=True,
        num_train_epochs=40,
        per_device_train_batch_size=50,
        save_steps=10_000,
        save_total_limit=2,
        weight_decay=0.001,
        evaluation_strategy='epoch',
        report_to="wandb",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=dataset,
        eval_dataset=dataset_val,
    )

    # train the model
    trainer.train()
    wandb.finish()

    # save the model
    trainer.save_model(str(save_path / 'HotelBERT'))

    # clean up
    del model
    del trainer
    del dataset
    torch.cuda.empty_cache()


def train_tokenizer():
    # define the files to train the tokenizer on
    data_files = [str(x) for x in data_path.glob("*.txt")]

    # Initialize a tokenizer
    tokenizer = ByteLevelBPETokenizer()
    # Customize training
    special_tokens = ["<s>", "<pad>", "</s>", "<unk>", "<mask>"]
    tokenizer.train(files=data_files,
                    vocab_size=vocab_size,
                    min_frequency=2,
                    special_tokens=special_tokens)

    # save the tokenizer
    Path(save_path / 'HotelBERT').mkdir(parents=True, exist_ok=True)
    tokenizer.save_model(str(save_path / 'HotelBERT'))


if __name__ == "__main__":
    data_path = Path('data/hotel-reviews/transformed/')
    save_path = Path('models/')

    max_len = 512
    vocab_size = 52_000

    # configure W&B
    wandb.init(project='vm01-HotelBERT', entity='fabiangroeger')

    # train tokenizer
    if not (save_path / 'HotelBERT' / 'vocab.json').exists():
        train_tokenizer()
    else:
        print('Tokenizer exists, using existing one.')

    # train model
    train_model()
