import wandb
import argparse
import logging
import tensorflow as tf

from wandb.keras import WandbCallback
from transformers import TFBertForSequenceClassification

from src.utils.utils_visualize import log_distribution
from src.dataset.natio_dataset import NationalityDataset
from src.dataset.utils import DatasetType, TokenizerType
from src.metrics.standard_metrics import f1_score, recall_score, precision_score
from src.models.utils import huggingface_predict_sample


logging.disable(logging.WARNING)

my_parser = argparse.ArgumentParser(description='Runs a W&B sweep (hyperparameter search) on the nationality dataset using a BERT model.')
my_parser.add_argument('--data_path',
                       type=str,
                       required=True,
                       help='path to the cleaned dataset to load.')
args = my_parser.parse_args()


def train():
    # specify the hyperparameter to be tuned
    config_defaults = {'learning_rate': 2e-5,
                       'epochs': 10,
                       'batch_size': 16,
                       'huggingface_model': 'bert-base-german-cased'}
    # configure W&B
    wandb.init(project='vm01-nationality-detection',
               entity='fabiangroeger',
               config=config_defaults)
    config = wandb.config
    config.model_type = 'BERT'

    # instantiate the dataset
    dataset = NationalityDataset(dataset_path=args.data_path,
                                 tokenizer_name=config.huggingface_model,
                                 tokenizer_type=TokenizerType.HUGGINGFACE)
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

    # model initialization
    model = TFBertForSequenceClassification.from_pretrained(config.huggingface_model)
    optimizer = tf.keras.optimizers.Adam(learning_rate=config.learning_rate, epsilon=1e-08, clipnorm=1.0)
    loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    acc = tf.keras.metrics.SparseCategoricalAccuracy('accuracy')

    # compile the model
    model.compile(optimizer=optimizer,
                  loss=loss,
                  metrics=[acc, f1_score, recall_score, precision_score])
    model.summary()

    # save model
    model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=wandb.run.dir + '/model_weights.h5',
        save_weights_only=True,
        monitor='val_f1_score',
        mode='max',
        save_best_only=True)

    # train the model
    model.fit(train_data,
              epochs=config.epochs,
              validation_data=val_data,
              callbacks=[
                  WandbCallback(monitor='val_f1_score', mode='max'),
                  model_checkpoint_callback
              ])

    # predict for all samples in the validation set and log to W&B
    rdm_table = wandb.Table(columns=['Text', 'Predicted', 'True'])
    for i, row in dataset.df_val.iterrows():
        pred_lbl = huggingface_predict_sample(row.text, dataset.tokenizer,
                                              model, dataset.labelencoder)
        rdm_table.add_data(row.text, pred_lbl, dataset.labelencoder.inverse_transform([row.prediction])[0])
    wandb.log({'predicted_val_samples': rdm_table})


if __name__ == "__main__":
    # configure W&B sweep
    sweep_config = {
      'method': 'bayes',
      'metric': {
          'name': 'val_f1_score',
          'goal': 'maximize',
      },
      'early_terminate':{
          'type': 'hyperband',
          'min_iter': 3,
      },
      'parameters': {
          'huggingface_model': {
              'values': [
                  'bert-base-german-cased',
                  'deepset/gbert-base',
                  'dbmdz/bert-base-german-cased',
                  'Geotrend/bert-base-de-cased'
              ]
          },
          'learning_rate': {
              'values': [5e-5, 3e-5, 2e-5]
          },
          'batch_size': {
              'values': [16, 32]
          },
      }
    }

    sweep_id = wandb.sweep(sweep_config, project='vm01-nationality-detection', entity='fabiangroeger')
    wandb.agent(sweep_id, function=train)
