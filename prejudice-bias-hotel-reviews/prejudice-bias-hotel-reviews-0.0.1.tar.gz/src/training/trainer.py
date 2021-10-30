import wandb
import tensorflow as tf

from transformers import TFAutoModelForSequenceClassification, create_optimizer
from wandb.keras import WandbCallback

from src.utils.utils_visualize import log_distribution
from src.dataset.base_dataset import BaseDataset
from src.dataset.hasoc_2019_dataset import HASOC2019Dataset
from src.dataset.germeval_2018_dataset import GermEval2018Dataset
from src.dataset.germeval_2021_dataset import GermEval2021Dataset
from src.dataset.hate_dataset import HateDataset
from src.dataset.natio_dataset import NationalityDataset
from src.dataset.tagesanzeiger_dataset import TagesanzeigerDataset
from src.dataset.utils import DatasetType, TokenizerType, Dataset
from src.metrics.standard_metrics import f1_score, recall_score, precision_score, f1_macro_score
from src.models.utils import huggingface_predict_sample, ModelType
from src.models.roberta_cnn import get_roberta_cnn_model


class Trainer():
    def __init__(self, data_path: str,
                 dataset_type: Dataset,
                 config_defaults: dict,
                 one_hot=False):
        self.data_path = data_path
        self.dataset_type = dataset_type
        self.config_defaults = config_defaults
        self.one_hot = one_hot

    def create_optimizer(self, config):
        total_steps = (config.epochs + config.num_warmup_epochs) * int(
            config.dataset_train_size / config.batch_size)
        config.num_warmup_steps = config.num_warmup_epochs * int(
            config.dataset_train_size / config.batch_size)
        optimizer, _ = create_optimizer(
            init_lr=config.learning_rate,
            num_train_steps=total_steps,
            num_warmup_steps=config.num_warmup_steps,
            weight_decay_rate=config.weight_decay_rate)

        return optimizer

    def create_model(self, config, optimizer):
        model_type = ModelType[config.classification_head]

        if model_type is ModelType.DEFAULT:
            model = TFAutoModelForSequenceClassification.from_pretrained(
                config.huggingface_model)
        elif model_type is ModelType.CNN:
            model = get_roberta_cnn_model(
                config.huggingface_model,
                dropout=config.dropout,
                weight_regularization=config.weight_regularization)
        else:
            raise ValueError('Invalid classification head')
        model.summary()

        if self.one_hot:
            acc = tf.keras.metrics.CategoricalAccuracy('accuracy')
            loss = tf.keras.losses.CategoricalCrossentropy(
                from_logits=True, label_smoothing=config.label_smoothing)
        else:
            acc = tf.keras.metrics.SparseCategoricalAccuracy('accuracy')
            loss = tf.keras.losses.SparseCategoricalCrossentropy(
                from_logits=True)

        model.compile(optimizer=optimizer,
                      loss=loss,
                      metrics=[
                          acc,
                          f1_score,
                          recall_score,
                          precision_score,
                          f1_macro_score
                      ])

        return model

    def _get_dataset(self):
        switcher = {
            Dataset.GERM_EVAL: GermEval2018Dataset,
            Dataset.HASOC: HASOC2019Dataset,
            Dataset.COMBINED_HATE: HateDataset,
            Dataset.NATIONALITY: NationalityDataset,
            Dataset.GERM_EVAL_2021: GermEval2021Dataset,
            Dataset.TAGESANZEIGER: TagesanzeigerDataset,
        }
        dataset_cls = switcher.get(self.dataset_type, None)

        if dataset_cls is None:
            raise ValueError('Invalid dataset')

        return dataset_cls

    def _log_dataset(self, dataset: BaseDataset, config):
        config.dataset_train_size = len(dataset.df_train)
        config.dataset_val_size = len(dataset.df_val)
        config.dataset_test_size = len(dataset.df_test)

        # log the distribution
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

    def _train_func(self):
        # configure W&B
        wandb.init(config=self.config_defaults)
        # get hyperparameters
        config = wandb.config

        # init dataset
        dataset_cls = self._get_dataset()
        dataset = dataset_cls(dataset_path=self.data_path,
                              tokenizer_name=config.huggingface_model,
                              tokenizer_type=TokenizerType.HUGGINGFACE)
        dataset_class_weight = dataset.get_class_weights()

        # log the dataset
        self._log_dataset(dataset, config)

        # save the tokenizer to W&B
        dataset.save_tokenizer(path=wandb.run.dir)
        # save the label encoder to W&B
        dataset.save_label_encoder(path=wandb.run.dir)

        # get the training and val dataset
        train_data = dataset.get_dataset(dataset_type=DatasetType.TRAIN,
                                         batch_size=config.batch_size,
                                         one_hot=self.one_hot)
        val_data = dataset.get_dataset(dataset_type=DatasetType.VAL,
                                       batch_size=config.batch_size,
                                       one_hot=self.one_hot)

        # reset the session to make sure a new model gets trained
        tf.keras.backend.clear_session()

        # define optimizer
        optimizer = self.create_optimizer(config)

        # model initialization
        model = self.create_model(config, optimizer)

        # save model
        model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
            filepath=wandb.run.dir + '/model_weights.h5',
            save_weights_only=True,
            monitor='val_f1_macro_score',
            mode='max',
            save_best_only=True)

        # train the model
        model.fit(train_data,
                  epochs=config.epochs + config.num_warmup_epochs,
                  validation_data=val_data,
                  class_weight=dataset_class_weight,
                  callbacks=[
                      # look at combination with model and callback....
                      WandbCallback(monitor='val_f1_macro_score', mode='max'),
                      model_checkpoint_callback
                  ])

        # predict validation set
        self._predict_val_samples(dataset, model)

        # finish and save the W&B run
        wandb.run.finish()

    def _predict_val_samples(self, dataset, model):
        # predict for all samples in the validation set and log to W&B
        rdm_table = wandb.Table(columns=['Text', 'Predicted', 'True'])
        for i, row in dataset.df_val.iterrows():
            pred_lbl = huggingface_predict_sample(row.text, dataset.tokenizer,
                                                  model, dataset.labelencoder)
            true_lbl = dataset.labelencoder.inverse_transform(
                [row[dataset.LABEL_COLUMN]])[0]
            rdm_table.add_data(row.text, pred_lbl, true_lbl)
        wandb.log({'predicted_val_samples': rdm_table})

    def train(self, config_defaults):
        # configure W&B
        wandb.init(config=config_defaults)
        # call train function
        self._train_func()

    def hyperparameter_search(self,
                              config: dict,
                              project_name: str,
                              entity: str = 'fabiangroeger'):
        sweep_id = wandb.sweep(config, project=project_name, entity=entity)
        # configure agent
        wandb.agent(sweep_id, function=self._train_func, count=50)
