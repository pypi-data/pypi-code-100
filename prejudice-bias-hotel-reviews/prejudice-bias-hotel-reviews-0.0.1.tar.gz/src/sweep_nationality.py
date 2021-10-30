import wandb
import argparse
import logging
import numpy as np
import tensorflow as tf

from src.dataset.natio_dataset import NationalityDataset
from src.dataset.utils import DatasetType, TokenizerType
from src.metrics.standard_metrics import f1_score, recall_score, precision_score
from src.utils.utils_visualize import log_distribution, WandbClassificationCallback
from src.models.fasttext_model import FastTextModel

logging.disable(logging.WARNING)

my_parser = argparse.ArgumentParser(
    description='Runs a W&B sweep (hyperparameter search) '
    'on the nationality dataset using a simple models.')
my_parser.add_argument('--data_path',
                       type=str,
                       required=True,
                       help='path to the cleaned dataset to load.')
args = my_parser.parse_args()


def train():
    # specify the hyperparameter to be tuned
    config_defaults = {
        'learning_rate': 0.01,
        'epochs': 100,
        'batch_size': 32,
        'model_type': 'bilstm',
        'embedding_type': 'fasttext',
        'layers': [16, 4],
        'dropout': 0,
        'recurrent_dropout': 0,
        'regularizer_weight': 0,
        'use_umlaute': True
    }
    # configure W&B
    wandb.init(project='vm01-nationality-detection',
               entity='fabiangroeger',
               config=config_defaults)
    config = wandb.config

    # change configs depending on architecture
    if config.model_type == 'lstm' or config.model_type == 'bilstm':
        tokenizer_type = TokenizerType.TOKENS
    else:
        config.embedding_type = 'fasttext'
        tokenizer_type = TokenizerType.NONE

    # instantiate the dataset
    dataset = NationalityDataset(dataset_path=args.data_path,
                                 tokenizer_name=None,
                                 tokenizer_type=tokenizer_type,
                                 use_umlaute=config.use_umlaute)
    config.dataset_size = len(dataset.df)
    config.dataset_train_size = len(dataset.df_train)
    config.dataset_val_size = len(dataset.df_val)
    config.dataset_test_size = len(dataset.df_test)

    # log the distribution
    log_distribution(dataset.df,
                     label_column=dataset.LABEL_COLUMN,
                     labelencoder=dataset.labelencoder,
                     name='original_class_distribution',
                     desc='Original Class Distribution')
    log_distribution(dataset.df_train,
                     label_column=dataset.LABEL_COLUMN,
                     labelencoder=dataset.labelencoder,
                     name='train_class_distribution',
                     desc='Training Set Class Distribution')
    log_distribution(dataset.df_val,
                     label_column=dataset.LABEL_COLUMN,
                     labelencoder=dataset.labelencoder,
                     name='val_class_distribution',
                     desc='Validation Set Class Distribution')

    # save the tokenizer to W&B
    dataset.save_tokenizer(path=wandb.run.dir)
    # save the label encoder to W&B
    dataset.save_label_encoder(path=wandb.run.dir)

    # get the training and val dataset
    train_data = dataset.get_dataset(dataset_type=DatasetType.TRAIN,
                                     batch_size=config.batch_size)
    val_data = dataset.get_dataset(dataset_type=DatasetType.VAL,
                                   batch_size=config.batch_size)

    # reset the session to make sure a new model gets trained
    tf.keras.backend.clear_session()

    # get one of the different models
    model_switcher = {
        'linear': FastTextModel.create_linear,
        'lstm': FastTextModel.create_lstm,
        'bilstm': FastTextModel.create_bilstm,
    }
    model_func = model_switcher.get(config.model_type, None)
    if model_func is None:
        raise ValueError('Wrong model type')
    # model initialization
    model = model_func(layers=config.layers,
                       embedding_type=config.embedding_type,
                       word_index=dataset.tokenizer.word_index,
                       dropout=config.dropout,
                       recurrent_dropout=config.recurrent_dropout,
                       regularizer_weight=config.regularizer_weight)
    optimizer = tf.keras.optimizers.Adam(learning_rate=config.learning_rate,
                                         epsilon=1e-08,
                                         clipnorm=1.0)
    loss = tf.keras.losses.BinaryCrossentropy()
    acc = tf.keras.metrics.BinaryAccuracy('accuracy')

    # compile the model
    model.compile(optimizer=optimizer,
                  loss=loss,
                  metrics=[acc, f1_score, recall_score, precision_score])
    model.summary()

    # define callback
    wandb_callback = WandbClassificationCallback(
        monitor='val_f1_score',
        mode='max',
        input_type='text',
        log_confusion_matrix=True,
        validation_data=val_data,
        labels=dataset.labelencoder.classes_.tolist(),
        classification_type='binary')

    # train the model
    model.fit(train_data,
              epochs=config.epochs,
              validation_data=val_data,
              callbacks=[wandb_callback])

    # predict for all samples in the validation set and log to W&B
    rdm_table = wandb.Table(columns=['Text', 'Predicted', 'True'])
    for i, row in dataset.df_val.iterrows():
        # correctly preprocess the text
        if tokenizer_type is TokenizerType.TOKENS:
            val_sample = dataset.tokenizer.texts_to_sequences([row.text])
            val_sample = tf.keras.preprocessing.sequence.pad_sequences(
                val_sample, maxlen=dataset.max_len)
        else:
            val_sample = [row.text]

        pred_lbl = np.round(model.predict(val_sample)[0][0])
        pred_lbl = dataset.labelencoder.inverse_transform([int(pred_lbl)])[0]
        true_lbl = dataset.labelencoder.inverse_transform([row.prediction])[0]
        rdm_table.add_data(row.text, pred_lbl, true_lbl)
    wandb.log({'predicted_val_samples': rdm_table})

    # finish and save the W&B run
    wandb.run.save()
    wandb.run.finish()


if __name__ == "__main__":
    # configure W&B sweep
    sweep_config = {
        'method': 'bayes',
        'metric': {
            'name': 'val_f1_score',
            'goal': 'maximize',
        },
        'early_terminate': {
            'type': 'hyperband',
            'min_iter': 10,
        },
        'parameters': {
            'epochs': {
                'values': [200]
            },
            'learning_rate': {
                'values': [0.001, 0.003, 0.01, 0.03]
            },
            'batch_size': {
                'values': [16, 32]
            },
            'layers': {
                'values': [
                    [8, 4],
                    [16, 4],
                ]
            },
            'model_type': {
                'values': ['bilstm']
            },
            'embedding_type': {
                'values': ['fasttext']
            },
            'dropout': {
                'values': [0, 0.1, 0.2]
            },
            'recurrent_dropout': {
                'values': [0]
            },
            'regularizer_weight': {
                'values': [0]
            },
            'use_umlaute': {
                'values': [True, False]
            }
        }
    }

    sweep_id = wandb.sweep(sweep_config,
                           project='vm01-nationality-detection',
                           entity='fabiangroeger')
    wandb.agent(sweep_id, function=train)
