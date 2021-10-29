"""
@author: Charles Hajjar

Use this class as your pipeline, use it for all of your data manipulation/feature creation functionality.

Functions here are used across the bot and training classes!

"""
#!/usr/bin/env python
#encoding: utf-8

from binance.client import Client
import pandas as pd 
import numpy as np
import pickle
# import libraries
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import json
import seaborn as sns
sns.set(color_codes=True)
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.keras.layers import Input, Dropout, Dense, LSTM, TimeDistributed, RepeatVector
from tensorflow.keras.models import Model
from tensorflow.keras import regularizers
# Multiple Inputs
from tensorflow.keras.utils import plot_model
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import GRU
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import RepeatVector
from tensorflow.keras.layers import TimeDistributed
from tensorflow.keras.layers import Conv1D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import concatenate
from tensorflow.keras.layers import Bidirectional
from tensorflow.keras.layers import Flatten
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import GRU, TimeDistributed, LSTM
from tensorflow.compat.v1.keras import backend as K
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import Dense, Flatten, Dropout, Input
from sklearn.preprocessing import MinMaxScaler
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
from tensorflow.keras.models import load_model
from sklearn.metrics import mean_squared_error
import math, sys, time
import datetime
# import Standadise data pickle
minmax = pickle.load(open('scaletime.pickle', 'rb'))

MinmaxR = pickle.load(open('scale.pickle', 'rb'))



class GatedActivationUnit(tf.keras.layers.Layer):
    """
        class GATE ACTIVATION FOR WAVENET AND FUNCTION RESIDUAL BLOCK
    """
    def __init__(self, activation="tanh", **kwargs):
        super().__init__(**kwargs)
        self.activation = tf.keras.activations.get(activation)

    def call(self, inputs):
        n_filters = inputs.shape[-1] // 2
        linear_output = self.activation(inputs[..., :n_filters])
        gate = tf.keras.activations.sigmoid(inputs[..., n_filters:])
        return self.activation(linear_output) * gate



class TradeChange:
    """
        class IA Trading Change Binance
    """
    def __init__(self, indata=None, data=None, x=None, X=None,y=None):
        self.indata = indata
        self.data = data
        self.x = x
        self.X = X
        self.y = y
        
    def __init__(self):

       
        self.keras_model = tf.keras.models.load_model('Change',custom_objects={'last_time_step_mse':self.last_time_step_mse})
        #print(self.keras_model)  
        
    def CreateOpenHighLowCloseVolumeData(sefl,indata=None):
        """
        create data import 
        """
        out = pd.DataFrame()
        d = []
        o = []
        h = []
        l = []
        c = []
        v = []
        for i in indata:
        #print(i)
            d.append(float(i[0]))
            o.append(float(i[1]))
            h.append(float(i[2]))
            c.append(float(i[3]))
            l.append(float(i[4]))
            v.append(float(i[5]))

        out['date'] = d
        out['open'] = o
        out['high'] = h
        out['low'] = l
        out['close'] = c
        out['volume'] = v
        return out


    @staticmethod
    def DataRegression(indata=None):
        """
        selecte close to data regression
        """
        out = pd.DataFrame()
        c = []
        for i in indata:
            c.append(float(i[3]))
        out['close'] = c
        return out


    @staticmethod
    def candleRatios(data):
        """
        préprocesse to analyse strategie data to classification
        """
        data['mid'] = (data['low']+data['high'])/2.0
        data['DayMA50'] = data['close'].rolling(window=50).mean()
        data['DayMA20'] = data['close'].rolling(window=20).mean()
        data['MAC'] = data['DayMA20']-data['DayMA50']
        data['50moyenmobile'] = data['close'].rolling(window=50).std()
        data['20moyenmobile'] = data['close'].rolling(window=20).std()  
        data['UpperBand'] = data['DayMA20'] + (data['20moyenmobile']* 2)
        data['LowerBand'] = data['DayMA20'] - (data['20moyenmobile'] * 2)
        return data


    @staticmethod
    def StepData(x, data):
        #self.x = x
        #self.data = data
        SEQ_LEN = 1  # how long of a preceeding sequence to collect for RNN
        FUTURE_PERIOD_PREDICT = 1  # how far into the future are we trying to predict?
        RATIO_TO_PREDICT = "MAC"
        data['MACtendance'] = data[RATIO_TO_PREDICT].shift(-FUTURE_PERIOD_PREDICT)
        data['L50']= data['LowerBand'] - data['DayMA50']
        data['L20']= data['DayMA20'] - data['LowerBand']

        return data


    @staticmethod
    def GetChangeData(data):
        """
        change processe data to new feature in classification
        """
        cols = data.columns
        for i in cols:
            j = "c_" + i
            try:
                dif = data[i].diff()
                data[j] = dif
            except Exception as e:
                print(e)
        return data


    @staticmethod
    def to_sequences(data, seq_len):
        """
        créate sequence to model regression
        """
        SEQ_LEN = 500
        d = []
        for index in range(len(data) - seq_len):
            d.append(data[index: index + seq_len])
        return np.array(d)


    def Split(self,data, seq_len, train_split):
        """
           processe data split train
        """

        data = self.to_sequences(data, seq_len)

        num_train = int(train_split * data.shape[0])

        X_train = data[:num_train, :-1, :]
        y_train = data[:num_train, -1, :]

        X_test = data[num_train:, :-1, :]
        y_test = data[num_train:, -1, :]

        return X_train, y_train, X_test, y_test



    @staticmethod
    def Minmax_encodeR(data):
        """
        Scales numerical columns using their means and standard deviation to get
        """
        #print('# Standardize')
        data = pd.DataFrame(data, columns = ['close'])
        df_x = data
        #print(df_x)
        x_transform = MinmaxR.transform(df_x)
        return x_transform



    @staticmethod
    def invers_transform(data):
        """
        Scales inverse transforme
        """
        #data = data.reshape(1, -1)
        #data = pd.DataFrame(data, columns = ['close'])
        df_x = data
        x_invtransform = MinmaxR.inverse_transform(df_x)
        return x_invtransform

    #@staticmethod
    def FeatureCreationClassification(self,indata):
        """
        fonction pour la classification
        """
        convertedData = self.CreateOpenHighLowCloseVolumeData(indata)
        FeatureData = pd.DataFrame()
        FeatureData['open'] = convertedData['open']
        FeatureData['high'] = convertedData['high']
        FeatureData['low'] = convertedData['low']
        FeatureData['close'] = convertedData['close']
        FeatureData['volume'] = convertedData['volume']
        FeatureData['date'] = convertedData['date']
        FeatureData = self.candleRatios(FeatureData)
        #StepData(FeatureData['close'],FeatureData)
        #CreateTargets(FeatureData,1)
        FeatureData = self.GetChangeData(FeatureData)
        FeatureData = FeatureData.dropna().reset_index(drop=True)  
        return FeatureData

    #@staticmethod
    def FeatureCreationRegressiontrain(self,indata):
        """
        processe data to training regression

        """
        convertedData = self.DataRegression(indata)
        FeatureData = pd.DataFrame()
        FeatureData['close'] = convertedData['close']
        return FeatureData

    #@staticmethod
    def DataRegressionModel(self,indata,n):
        """
           processe data to  Model regression
        """
        convertedData = self.DataRegression(indata)
        FeatureData = pd.DataFrame()
        FeatureData['close'] = convertedData['close']
        FeatureData = self.Minmax_encodeR(FeatureData)
        FeatureData = self.to_sequences(FeatureData,n)
        return FeatureData



    @staticmethod
    def signalMma(x):
        """
           processe signale O nothing
           1 signal == MM20
           2 signale sup Upperband
        """
        low_signal = x.iloc[0,2]#58151.73#x.iloc[0:1,1]
    
        sortie = 0
        for i, row in x.iterrows():
            for i, row in x.iterrows():
                print("it")
                print(i)
                if x.loc[i,"low"] >  low_signal:
                    print("le low bougie test")
                    print(x.loc[i,"low"])
                    if x.loc[i,"DayMA20"] >= x.loc[i,"low"]  and x.loc[i,"DayMA20"] <= x.loc[i,"high"] :
                        sortie = 1
                        print("sortie1")
                        print(sortie)
                        break
                    if x.loc[i,"UpperBand"] >= x.loc[i,"low"]  and x.loc[i,"UpperBand"] <= x.loc[i,"high"]  :
                        sortie = 2
                        print("sortie2")
                        print(sortie)
                        break
                else :
                    sortie = 0
                    break
            return sortie

    @staticmethod
    def last_time_step_mse(Y_true, Y_pred):
        return tf.keras.metrics.mean_squared_error(Y_true[:, -1], Y_pred[:, -1])

    @staticmethod
    def wavenet_residual_block(inputs, n_filters, dilation_rate):
        """
        RESIDUAL BLOCK TO MODEL FUNCTION
        """
        z = Conv1D(
            2 * n_filters, kernel_size=1, padding="causal", dilation_rate=dilation_rate
        )(inputs)
        z = GatedActivationUnit()(z)
        z = Bidirectional(LSTM(n_filters, activation="relu", return_sequences=True))(z)
        z = GatedActivationUnit()(z)
        z = Conv1D(n_filters, kernel_size=1)(z)
        return tf.keras.layers.Add()([z, inputs]), z

    
    def create_model(self, X, y):
        """
         Model Tensorflow Wave net Bdirectionnal LSTM GRU CNN
        """
        tf.keras.backend.clear_session()
        np.random.seed(42)
        tf.random.set_seed(42)

        # create model
        # create model
        n_layers_per_block = 3  # 10 in the paper
        n_blocks = 1  # 3 in the paper
        n_filters = 32  # 128 in the paper

        visible1 = Input(shape=([X.shape[1], X.shape[2]]))
        z = Conv1D(filters=32, kernel_size=1, strides=2, padding="causal")(visible1)
        skip_to_last = []
        for dilation_rate in [2 ** i for i in range(n_layers_per_block)] * n_blocks:
            z, skip = self.wavenet_residual_block(z, n_filters, dilation_rate)
            skip_to_last.append(skip)
        z = tf.keras.activations.relu(tf.keras.layers.Add()(skip_to_last))
        pool11 = Dropout(rate=0.2)(z)
        pool12 = Bidirectional(LSTM(60,kernel_initializer="uniform" ,activation="relu", return_sequences=True))(pool11)
        pool13 = tf.keras.layers.Conv1D(n_filters, kernel_size=1, activation="relu")(pool12)
        pool14 = Flatten()(pool13)
        conc = Dense(64, activation="relu")(pool14)
        flat1 = tf.keras.layers.Dense(1)(conc)

        model = Model(inputs=[visible1], outputs=flat1)
        print('Model summary', model.summary())
        plot_model(model, to_file='wavenetBLSTM.png')
        model.compile(loss="mse", optimizer="adam", metrics=[self.last_time_step_mse])
        checkpoint_cb = ModelCheckpoint('Change',save_best_only=True)
        log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
        print(model.fit(
        X, y, epochs=1, batch_size=500, validation_split=0.2 , shuffle=False,
        callbacks=[checkpoint_cb,tensorboard_callback]))
    

    
        # save format tensoflow , format keras
        model.save("Change")
    
    def predict(self, input_data):
        """
        Return result of model predict.
        """
        request = self.keras_model.predict(input_data)
        #print('request')
        print(request[0])
        return request
  
    def TestScore(self,y_test,y_pred):
        score = np.sqrt(mean_squared_error(self.invers_transform(y_test),self.invers_transform(y_pred)))
        return score
    
