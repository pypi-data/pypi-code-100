"""
Copyright (c) 2020-2021 Go2Market Insights, LLC
All rights reserved.
https://g2m.ai

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import os, sys, time, json
import pandas as pd
from copy import deepcopy

from .runner_base import BaseRunner
from .constants import *
from .utils import *

class PropensityRunner(BaseRunner):
    """
    Runs the propensity scoring pipeline

    """
    def __init__(self, client=None, base_url=None):
        """
        """
        super().__init__(client=client, base_url=base_url)
        self.__uri = '{}/analytics/'.format(self._base_url)
        return

    def predict(self, df, model_id=None, client_id=None, idx_var=None, categorical_vars=[], numerical_vars=[], bool_vars=[], buffer_batch_size=1000, verbose=False, timeout=600, step=2):
        """
        :param df:
        :param model_id:
        :param request_id:
        :param client_id:
        :param idx_var:
        :param categorical_vars:
        :param numerical_vars:
        :param buffer_batch_size:
        :param verbose:
        :return res5:
        """

        # Load encoding keys
        keys = self._keys_load(model_id=model_id, verbose=verbose)
        if keys is None:
            print('ERROR! Keys not found. ')
            return None
        request_id = self._get_request_id()

        # Encode data and save it to buffer
        data, xref, zref, rref, fref, fref_exp, bref = self._encode(df, keys=keys, categorical_vars=categorical_vars, numerical_vars=numerical_vars, bool_vars=bool_vars, record_id_var=idx_var, verbose=verbose)
        if verbose: print('Total rows encoded: {:,}'.format(len(data)))
        res = self._buffer_save(data, client_id=client_id, request_id=request_id, verbose=verbose, batch_size=buffer_batch_size)

        # Predict with propensity model and retrieve results
        if res['batches_saved']==res['total_batches']:
            self.__predict(
                request_id=res['request_id'], model_id=model_id, client_id=client_id, idx_field=fref['forward'][idx_var],
                categorical_fields=[ fref['forward'][var] for var in categorical_vars ],
                verbose=verbose
            )
            self._poll(payload={'request_id': res['request_id'], 'client_id': client_id, 'command': 'task-status'}, timeout=timeout, step=step, verbose=verbose)
            data2 = self.__retrieve_predict_results(request_id=request_id, client_id=client_id, rref=rref, verbose=verbose)
        else:
            print('ERROR! Buffer save failed: {}'.format(res))

        # Clear buffer
        res4 = self._buffer_clear(request_id=res['request_id'], client_id=client_id, verbose=verbose)

        # Decode data
        data2 = self._decode(data2, categorical_vars=categorical_vars, numerical_vars=numerical_vars, bool_vars=bool_vars, record_id_var=idx_var, xref=xref, zref=zref, rref=rref, fref=fref, bref=bref, verbose=verbose)

        # Compile results
        res5 = {}
        res5['data2'] = data2
        res5['model_id'] = model_id
        return res5

    def __predict(self, request_id=None, model_id=None, client_id=None, idx_field=None, categorical_fields=[], verbose=False):
        """
        :param request_id:
        :param model_id:
        :param client_id:
        :param idx_field:
        :param categorical_fields:
        :param verbose:
        :return:
        """
        if verbose: print('Predicting propensity model using data in buffer...')
        res = self._client._post(self.__uri, {
            'command': 'propensity-predict',
            'model_id': model_id,
            'request_id': request_id,
            'client_id': client_id,
            'idx_field': idx_field,
            'categorical_fields': categorical_fields,
        })
        return res

    def __retrieve_predict_results(self, request_id=None, client_id=None, rref={}, verbose=False):
        """
        :param request_id:
        :param client_id:
        :param verbose:
        :return data2:
        """
        data2 = self._buffer_read(request_id=request_id, client_id=client_id, dataframe_name='data2', verbose=verbose)
        return data2

    def train(self, df, client_id=None, idx_var=None, outcome_var=None, categorical_vars=[], numerical_vars=[], bool_vars=[], algorithm='random-forest-classifier', train_size=0.5, buffer_batch_size=1000, verbose=False, timeout=600, step=2):
        """
        :param df:
        :param client_id:
        :param idx_var:
        :param outcome_var:
        :param categorical_vars:
        :param numerical_vars:
        :param algorithm:
        :param train_size:
        :param buffer_batch_size:
        :param verbose:
        :return res5:
        """

        # Encode data and save it to buffer
        request_id = self._get_request_id()
        data, xref, zref, rref, fref, fref_exp, bref = self._encode(df, categorical_vars=categorical_vars, numerical_vars=numerical_vars, bool_vars=bool_vars, record_id_var=idx_var, verbose=verbose)
        res = self._buffer_save(data, client_id=client_id, request_id=request_id, verbose=verbose, batch_size=buffer_batch_size)

        # Train propensity model and retrieve results
        if res['batches_saved']==res['total_batches']:
            self.__train(
                request_id=res['request_id'], client_id=client_id, idx_field=fref['forward'][idx_var],
                outcome_var=fref['forward'][outcome_var],
                categorical_fields=[ fref['forward'][var] for var in categorical_vars ],
                algorithm=algorithm, train_size=train_size, verbose=verbose
            )
            self._poll(payload={'request_id': res['request_id'], 'client_id': client_id, 'command': 'task-status'}, timeout=timeout, step=step, verbose=verbose)
            features, confusion_matrix, stats, roc = self.__retrieve_train_results(request_id=request_id, client_id=client_id, fref=fref_exp, verbose=verbose)
        else:
            print('ERROR! Buffer save failed: {}'.format(res))

        # Clear buffer
        res4 = self._buffer_clear(request_id=res['request_id'], client_id=client_id, verbose=verbose)

        # Save encoding keys locally
        self._keys_save(model_id=request_id, keys={'xref': xref, 'zref': zref, 'rref': rref, 'fref': fref, 'fref_exp': fref_exp, 'bref': bref}, verbose=verbose)

        # Compile results
        res5 = {}
        res5['features'] = features
        res5['confusion_matrix'] = confusion_matrix
        res5['stats'] = stats
        res5['roc'] = roc
        res5['model_id'] = request_id
        return res5

    def __train(self, request_id=None, client_id=None, idx_field=None, outcome_var=None, categorical_fields=[], algorithm='random-forest-classifier', train_size=0.5, verbose=False):
        """
        :param request_id:
        :param client_id:
        :param idx_field:
        :param outcome_var:
        :param categorical_fields:
        :param algorithm:
        :param verbose:
        :return:
        """
        if verbose: print('Training propensity model using data in buffer...')
        res = self._client._post(self.__uri, {
            'command': 'propensity-train',
            'request_id': request_id,
            'client_id': client_id,
            'algorithm': algorithm,
            'train_size': train_size,
            'idx_field': idx_field,
            'outcome_var': outcome_var,
            'categorical_fields': categorical_fields,
        })
        return res

    def __retrieve_train_results(self, request_id=None, client_id=None, fref={}, verbose=False):
        """
        :param request_id:
        :param client_id:
        :param fref:
        :param verbose:
        :return features:
        :return confusion_matrix:
        :return stats:
        """

        # Features
        features = self._buffer_read(request_id=request_id, client_id=client_id, dataframe_name='features', verbose=verbose)
        features['Importance'] = features['Importance'].astype('float')
        features.sort_values(by=['Importance'], ascending=False, inplace=True)
        for idx, row in features.iterrows():
            features.loc[idx, 'Feature'] = fref_decode_value(features.loc[idx, 'Feature'], fref)

        # Confusion matrix
        confusion_matrix = self._buffer_read(request_id=request_id, client_id=client_id, dataframe_name='confusion_matrix', verbose=verbose)

        # Stats
        stats = self._buffer_read(request_id=request_id, client_id=client_id, dataframe_name='stats', verbose=verbose)
        stats['Value'] = stats['Value'].astype('float')

        # ROC
        roc = self._buffer_read(request_id=request_id, client_id=client_id, dataframe_name='roc', verbose=verbose)
        if 'TPR' in roc.keys():
            roc['TPR'] = roc['TPR'].astype(float)
        if 'FPR' in roc.keys():
            roc['FPR'] = roc['FPR'].astype(float)
            roc = roc.sort_values(by=['FPR'], ascending=True)

        return features, confusion_matrix, stats, roc
