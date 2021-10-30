import argparse
import logging

from src.dataset.utils import Dataset
from src.training.trainer import Trainer

logging.disable(logging.WARNING)

my_parser = argparse.ArgumentParser(
    description='Runs a W&B sweep (hyperparameter search) '
    'on the combined GermEval-2018 and HASOC-2019 dataset using a pre-trained BERT model.'
)
my_parser.add_argument('--data_path',
                       type=str,
                       required=True,
                       help='path to the dataset to load.')
args = my_parser.parse_args()

if __name__ == "__main__":
    sweep_config = {
        'method': 'bayes',
        'metric': {
            'name': 'val_f1_macro_score',
            'goal': 'maximize',
        },
        'early_terminate': {
            'type': 'hyperband',
            'min_iter': 3,
        },
        'parameters': {
            'learning_rate': {
                'values': [6e-5, 5e-5, 4e-5, 3e-5]
            },
            'batch_size': {
                'values': [16, 32]
            },
            'classification_head': {
                'values': ['CNN', 'DEFAULT']
            },
            'num_warmup_epochs': {
                'values': [1, 2]
            },
            'weight_decay_rate': {
                'values': [0.4, 0.2, 0.1, 0.01]
            },
            'label_smoothing': {
                'values': [0.2, 0.1, 0.01]
            },
        }
    }

    config_defaults = {
        'learning_rate': 2e-5,
        'epochs': 10,
        'batch_size': 32,
        'num_warmup_epochs': 2,
        'weight_decay_rate': 0.01,
        'label_smoothing': 0.0,
        'huggingface_model': 'FabianGroeger/HotelBERT',
        'classification_head': 'DEFAULT',
        'model_type': 'HuggingFace',
    }

    trainer = Trainer(data_path=args.data_path,
                      dataset_type=Dataset.COMBINED_HATE,
                      config_defaults=config_defaults,
                      one_hot=True)
    trainer.hyperparameter_search(config=sweep_config,
                                  project_name='vm01-Combined-Hate')
