import wandb
import numpy as np

from wandb.keras import WandbCallback


def log_distribution(df, label_column, labelencoder, name: str, desc: str):
    values = df[label_column].value_counts().tolist()
    labels = df[label_column].value_counts().index.tolist()
    labels = labelencoder.inverse_transform(labels).tolist()
    distribution_data = [[label, val] for (label, val) in zip(labels, values)]
    distribution_table = wandb.Table(data=distribution_data, columns=['label', 'samples'])
    wandb.log({name: wandb.plot.bar(distribution_table, 'label', 'samples', title=desc)})


class WandbClassificationCallback(WandbCallback):

    def __init__(self,
                 monitor='val_loss',
                 verbose=0,
                 mode='auto',
                 save_weights_only=False,
                 log_weights=False,
                 log_gradients=False,
                 save_model=True,
                 training_data=None,
                 validation_data=None,
                 labels=[],
                 data_type=None,
                 predictions=1,
                 generator=None,
                 input_type=None,
                 output_type=None,
                 log_evaluation=False,
                 validation_steps=None,
                 class_colors=None,
                 log_batch_frequency=None,
                 log_best_prefix="best_",
                 log_confusion_matrix=False,
                 classification_type='binary'):

        super().__init__(monitor=monitor,
                         verbose=verbose,
                         mode=mode,
                         save_weights_only=save_weights_only,
                         log_weights=log_weights,
                         log_gradients=log_gradients,
                         save_model=save_model,
                         training_data=training_data,
                         validation_data=validation_data,
                         labels=labels,
                         data_type=data_type,
                         predictions=predictions,
                         generator=generator,
                         input_type=input_type,
                         output_type=output_type,
                         log_evaluation=log_evaluation,
                         validation_steps=validation_steps,
                         class_colors=class_colors,
                         log_batch_frequency=log_batch_frequency,
                         log_best_prefix=log_best_prefix)

        self.log_confusion_matrix = log_confusion_matrix
        self.classification_type = classification_type

    def on_epoch_end(self, epoch, logs={}):
        if self.log_weights:
            wandb.log(self._log_weights(), commit=False)

        if self.log_gradients:
            wandb.log(self._log_gradients(), commit=False)

        if self.log_confusion_matrix:
            if self.validation_data is None:
                wandb.termwarn("No validation_data set, pass a generator to the callback.")
            elif self.validation_data:
                wandb.log(self._log_confusion_matrix(), commit=False)

        wandb.log({'epoch': epoch}, commit=False)
        wandb.log(logs, commit=True)

        self.current = logs.get(self.monitor)
        if self.current and self.monitor_op(self.current, self.best):
            if self.log_best_prefix:
                wandb.run.summary["%s%s" % (self.log_best_prefix, self.monitor)] = self.current
                wandb.run.summary["%s%s" % (self.log_best_prefix, "epoch")] = epoch
                if self.verbose and not self.save_model:
                    print('Epoch %05d: %s improved from %0.5f to %0.5f' % (
                        epoch, self.monitor, self.best, self.current))
            if self.save_model:
                self._save_model(epoch)
            self.best = self.current

    def _log_confusion_matrix(self):
        true = []
        pred = []

        for (x_val, y_val) in self.validation_data:
            if self.classification_type == 'multiclass':
                y_val = np.argmax(y_val, axis=1)
                y_pred = np.argmax(self.model.predict(x_val), axis=1)
            elif self.classification_type == 'binary':
                y_val = y_val.numpy()
                y_pred = np.round(self.model.predict(x_val)).squeeze().astype(int)
            else:
                wandb.termwarn('Unknown classification type')

            true.append(y_val)
            pred.append(y_pred)

        true = [val for sublist in true for val in sublist]
        pred = [val for sublist in pred for val in sublist]

        return {'confusion_matrix': wandb.plot.confusion_matrix(probs=None, y_true=true, preds=pred, class_names=self.labels)}
