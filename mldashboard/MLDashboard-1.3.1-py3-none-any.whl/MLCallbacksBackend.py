from MLDashboard.MLCommunicationBackend import Message, MessageMode
from tensorflow.keras.callbacks import Callback
import numpy as np
import warnings
from typing import List


class CallbackConfig:
    """Customize when data is send to the dashboard"""
    def __init__(self, send_on_train_start = True, send_on_train_end = True, send_on_test_start = True,
                 send_on_test_end = True, send_on_predict_start = True, send_on_predict_end = True,
                 send_on_epoch_end = True, send_on_batch_end = False, send_on_test_batch_end = False,
                 send_on_predict_batch_end = False, force_update_on_epoch_end=True):

        self.send_on_train_start = send_on_train_start
        self.send_on_train_end = send_on_train_end
        self.send_on_test_start = send_on_test_start
        self.send_on_test_end = send_on_test_end
        self.send_on_predict_start = send_on_predict_start
        self.send_on_predict_end = send_on_predict_end

        self.send_on_epoch_end = send_on_epoch_end
        self.send_on_batch_end = send_on_batch_end #this can quickly overwhelm the dashboard
        self.send_on_test_batch_end = send_on_test_batch_end
        self.send_on_predict_batch_end = send_on_predict_batch_end

        #batch begin does not contain any keys

        self.force_update_on_epoch_end = force_update_on_epoch_end #redraws the screen

#region Callbacks
class DashboardCallbacks(Callback):
    def __init__(self, updatelist: List[Message], returnlist: List[Message], model, x_train, y_train, x_test, y_test,
                 prediction_labels, config: CallbackConfig):
        """
        This inherits from Tensorflow callbacks and connects the model training to the dashboard. Can be customized
        by overriding the custom_on functions.

        :param updatelist: List from dashboard creation
        :param returnlist: List from dashboard creation
        :param model: Tensorflow model
        :param x_train: Training set features
        :param y_train: Training set output
        :param x_test: Test set features
        :param y_test: Test set output
        :param prediction_labels: Allows images to be labeled with friendly text
        :param config: Customize when data is sent
        """

        super().__init__()
        self.updatelist = updatelist
        self.returnlist = returnlist
        self.model = model
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test

        self.predictionlabels = prediction_labels

        self.config = config

        self.handleDataRequest()

    def label(self, data):
        labels = []
        for item in data:
            labels.append(self.predictionlabels[item])
        return labels

    def predlabel(self, data):
        labels = []
        for item in data:
            labels.append(self.predictionlabels[np.argmax(item)])
        return labels

    def sample(self, data, x, y):
        start = data.body["startingindex"]
        num = data.body["num"] + start
        x = x[start:num]
        y = y[start:num]
        return {"x": x, "y": self.label(y)}

    def predsample(self, data, x, y):
        start = data.body["startingindex"]
        num = data.body["num"] + start
        pred = self.predlabel(self.model.predict(x[start:num]))
        x = x[start:num]
        y = y[start:num]
        return {'x': x, 'y': self.label(y), 'pred': pred}

    def wrongpredsample(self, data, x, y):
        maxnum = data.body["num"]
        attempts = data.body["attempts"]

        preds = self.predlabel(self.model.predict(x[0:attempts]))
        y = self.label(y)
        features = []
        wrongpreds = []
        correctresult = []
        for i in range(0, attempts):
            if preds[i] != y[i]:
                features.append(x[i])
                wrongpreds.append(preds[i])
                correctresult.append(y[i])

            if len(features) >= maxnum:
                break
        return {'x': features, 'y': correctresult, 'pred': wrongpreds}

    # on epoch begin
    def handleDataRequest(self):
        rmlist = []
        for index, item in enumerate(self.returnlist):
            if item.mode == MessageMode.Train_Set_Sample:
                rmlist.append(index)
                self.updatelist.append(Message(MessageMode.Train_Set_Sample,
                                               self.sample(item, self.x_train, self.y_train)))

            elif item.mode == MessageMode.Test_Set_Sample:
                rmlist.append(index)
                self.updatelist.append(Message(MessageMode.Test_Set_Sample,
                                               self.sample(item, self.x_test, self.y_test)))

            elif item.mode == MessageMode.Pred_Sample:
                rmlist.append(index)
                self.updatelist.append(Message(MessageMode.Pred_Sample,
                                               self.predsample(item, self.x_test, self.y_test)))


            elif item.mode == MessageMode.Pred_Sample_Train:
                rmlist.append(index)
                self.updatelist.append(Message(MessageMode.Pred_Sample_Train,
                                               self.predsample(item, self.x_train, self.y_train)))

            elif item.mode == MessageMode.Wrong_Pred_Sample:
                rmlist.append(index)
                self.updatelist.append(Message(MessageMode.Wrong_Pred_Sample,
                                               self.wrongpredsample(item, self.x_test, self.y_test)))

            elif item.mode == MessageMode.Wrong_Pred_Sample_Train:
                rmlist.append(index)
                self.updatelist.append(Message(MessageMode.Wrong_Pred_Sample_Train,
                                               self.wrongpredsample(item, self.x_train, self.y_train)))

        rmlist.reverse()
        for index in rmlist:
            self.returnlist.pop(index)

    # on epoch end
    def handleCommands(self, allowstop=True):
        rmlist: List[int] = []
        for index, item in enumerate(self.returnlist):
            if item.mode == MessageMode.Command:
                rmlist.append(index)
                if item.body['command'] == 'stop':
                    if allowstop:
                        print("Training manually stopped.")
                        self.model.stop_training = True
                    else:
                        warnings.warn("Stop was triggered but training has already exited.")
                elif item.body['command'] == 'save':
                    print("Model manually saved.")
                    self.model.save(input("File name: "))

        rmlist.reverse()
        for index in rmlist:
            self.returnlist.pop(index)

    def HandleRemaingCommands(self):  # TODO - handle remaining data requests
        """
        This should be called after the dashboard exits.
        """
        self.handleCommands(allowstop=False)
        if len(self.returnlist) > 0:
            warnings.warn("We couldn't handle these remaining requests: ")
        for req in self.returnlist:
            print(req)

    #region callbacks
    def on_train_begin(self, logs=None):
        if self.config.send_on_train_start:
            self.updatelist.append(Message(MessageMode.Train_Begin, logs))
        self.custom_on_train_begin(logs)

    def on_train_end(self, logs=None):
        if self.config.send_on_train_end:
            self.updatelist.append(Message(MessageMode.Train_End, logs))
        self.custom_on_train_end(logs)

    def on_test_begin(self, logs=None):
        if self.config.send_on_test_start:
            self.updatelist.append(Message(MessageMode.Test_Begin, logs))
        self.custom_on_test_begin(logs)

    def on_test_end(self, logs=None):
        if self.config.send_on_test_end:
            self.updatelist.append(Message(MessageMode.Test_End, logs))
        self.custom_on_test_end(logs)

    def on_predict_begin(self, logs=None):
        if self.config.send_on_predict_start:
            self.updatelist.append(Message(MessageMode.Predict_Begin, logs))
        self.custom_on_predict_begin(logs)

    def on_predict_end(self, logs=None):
        if self.config.send_on_predict_end:
            self.updatelist.append(Message(MessageMode.Predict_End, logs))
        self.custom_on_predict_end(logs)

    def on_epoch_begin(self, epoch, logs=None):
        logs['epoch'] = epoch
        self.handleDataRequest()
        self.custom_on_epoch_begin(logs)

    def on_epoch_end(self, epoch, logs=None):
        logs['epoch'] = epoch
        if self.config.send_on_epoch_end:
            self.updatelist.append(Message(MessageMode.Epoch_End, logs))
        if self.config.force_update_on_epoch_end:
            self.updatelist.append(Message(MessageMode.ForceUpdate, {}))
        self.handleCommands()
        self.custom_on_epoch_end(logs)

    def on_train_batch_begin(self, batch, logs=None):
        logs['batch'] = batch
        self.custom_on_train_batch_begin(logs)

    def on_test_batch_begin(self, batch, logs=None):
        logs['batch'] = batch
        self.custom_on_test_batch_begin(logs)

    def on_predict_batch_begin(self, batch, logs=None):
        logs['batch'] = batch
        self.custom_on_predict_batch_begin(logs)


    def on_train_batch_end(self, batch, logs=None):
        logs['batch'] = batch
        if self.config.send_on_batch_end:
            self.updatelist.append(Message(MessageMode.Train_Batch_End, logs))
        self.custom_on_train_batch_end(batch)

    def on_test_batch_end(self, batch, logs=None):
        logs['batch'] = batch
        if self.config.send_on_batch_end:
            self.updatelist.append(Message(MessageMode.Test_Batch_End, logs))
        self.custom_on_test_batch_end(batch)

    def on_predict_batch_end(self, batch, logs=None):
        logs['batch'] = batch
        if self.config.send_on_batch_end:
            self.updatelist.append(Message(MessageMode.Predict_Batch_End, logs))
        self.custom_on_predict_batch_end(batch)
    #endregion
    #region custom overrides
    def custom_on_train_begin(self, logs):
        pass

    def custom_on_train_end(self, logs):
        pass

    def custom_on_test_begin(self, logs):
        pass

    def custom_on_test_end(self, logs):
        pass

    def custom_on_predict_begin(self, logs):
        pass

    def custom_on_predict_end(self, logs):
        pass

    def custom_on_epoch_begin(self, logs):
        pass

    def custom_on_epoch_end(self, logs):
        pass

    def custom_on_train_batch_begin(self, logs):
        pass

    def custom_on_test_batch_begin(self, logs):
        pass

    def custom_on_predict_batch_begin(self, logs):
        pass

    def custom_on_train_batch_end(self, logs):
        pass

    def custom_on_test_batch_end(self, logs):
        pass

    def custom_on_predict_batch_end(self, logs):
        pass
    #endregion
#endregion Callbacks