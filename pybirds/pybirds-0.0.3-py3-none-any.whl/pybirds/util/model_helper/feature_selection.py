# -*- coding: utf-8 -*-
__version__ = 'v1.0.0'
__author__ = ['Ouyang Ruofei']

"""

"""

import numpy as np
import pandas as pd
from termcolor import cprint
from joblib import Parallel, delayed

import toad
import lightgbm as lgb
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.base import TransformerMixin
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve


class Metrics:
    @classmethod
    def get_auc(cls, ytrue, yprob, **kwargs):
        auc = roc_auc_score(ytrue, yprob)

        if kwargs.get('symmetry', False) is True:
            if auc < 0.5:
                auc = 1 - auc
        return auc

    @classmethod
    def get_ks(cls, ytrue, yprob):
        fpr, tpr, thr = roc_curve(ytrue, yprob)
        ks = max(abs(tpr - fpr))
        return ks

    @classmethod
    def get_gini(cls, ytrue, yprob, **kwargs):
        auc = cls.get_auc(ytrue, yprob, **kwargs)
        gini = 2 * auc - 1

        return gini

    @classmethod
    def get_stat(cls, df_label, df_feature):
        var = df_feature.name
        df_data = pd.DataFrame({'val': df_feature, 'label': df_label})

        # statistics of total count, total ratio, bad count, bad rate
        df_stat = df_data.groupby('val').agg(total=('label', 'count'),
                                             bad=('label', 'sum'),
                                             bad_rate=('label', 'mean'))
        df_stat['var'] = var
        df_stat['good'] = df_stat['total'] - df_stat['bad']
        df_stat['total_ratio'] = df_stat['total'] / df_stat['total'].sum()
        df_stat['good_density'] = df_stat['good'] / df_stat['good'].sum()
        df_stat['bad_density'] = df_stat['bad'] / df_stat['bad'].sum()

        eps = np.finfo(np.float32).eps
        df_stat.loc[:, 'iv'] = (df_stat['bad_density'] - df_stat['good_density']) * \
                               np.log((df_stat['bad_density'] + eps) / (df_stat['good_density'] + eps))

        cols = ['var', 'total', 'total_ratio', 'bad', 'bad_rate', 'iv', 'val']
        df_stat = df_stat.reset_index()[cols].set_index('var')
        return df_stat

    @classmethod
    def get_iv(cls, df_label, df_feature):
        df_stat = cls.get_stat(df_label, df_feature)
        return df_stat['iv'].sum()


class CorrSelector(TransformerMixin):
    def __init__(self):
        self.version = 'v2.0.2'
        self.detail = dict()
        self.selected_features = list()
        self.removed_features = list()

    def fit(self, df_xtrain, df_ytrain, **kwargs):
        corr_threshold = kwargs.get('corr_threshold', 0.95)
        method = kwargs.get('method', 'iv_descending')
        n_jobs = kwargs.get('n_jobs', -1)
        feature_list = sorted(kwargs.get('feature_list', df_xtrain.columns.tolist()))

        df_iv = kwargs.get('df_iv', None)
        if df_iv is None:
            if len(df_ytrain) > 100000:
                lst_iv = Parallel(n_jobs=n_jobs)(
                    delayed(Metrics.get_iv)(df_ytrain, df_xtrain[c]) for c in feature_list)
            else:
                lst_iv = [Metrics.get_iv(df_ytrain, df_xtrain[c]) for c in feature_list]
            df_iv = pd.DataFrame({'var': feature_list, 'iv': lst_iv})

        if method == 'iv_ascending':
            df_iv = df_iv.sort_values(by='iv', ascending=True).set_index('var')
            feature_list = df_iv.index.tolist()
            df_corr = df_xtrain[feature_list].corr()
            df_corr = abs(df_corr - pd.DataFrame(np.identity(len(df_corr)),
                                                 index=df_corr.index,
                                                 columns=df_corr.columns))  # remove self
            df_res = pd.concat([df_iv, df_corr], axis=1)
            self.detail['before'] = df_res

            for var in feature_list:
                if df_res[var].max() >= corr_threshold:
                    df_res = df_res.drop(var, axis=0)
                    df_res = df_res.drop(var, axis=1)
                else:
                    continue
            self.detail['after'] = df_res

        elif method == 'iv_descending':
            df_iv = df_iv.sort_values(by='iv', ascending=False).set_index('var')
            feature_list = df_iv.index.tolist()
            df_corr = df_xtrain[feature_list].corr()
            df_corr = abs(df_corr - pd.DataFrame(np.identity(len(df_corr)),
                                                 index=df_corr.index,
                                                 columns=df_corr.columns))  # remove self
            df_res = pd.concat([df_iv, df_corr], axis=1)
            self.detail['before'] = df_res

            for var in feature_list:
                if var not in df_res.index:
                    continue
                else:
                    lst_remove = df_res[df_res[var] >= corr_threshold].index.tolist()
                    df_res = df_res.drop(lst_remove, axis=0)
                    df_res = df_res.drop(lst_remove, axis=1)
            self.detail['after'] = df_res

        else:
            raise Exception(f'Unknown method {method}, please specify iv_descending or iv_ascending')

        self.selected_features = df_res.index.tolist()
        self.removed_features = sorted(set(feature_list) - set(self.selected_features))
        return self

    def transform(self, df_xtest, **kwargs):
        feature_list = kwargs.get('feature_list', df_xtest.columns.tolist())
        feature_list = sorted(set(feature_list) & set(self.selected_features))
        return df_xtest[feature_list]

    def summary(self):
        print('\nselected features:')
        print(self.selected_features)
        print('\nremoved features:')
        print(self.removed_features)
        print('\nsummary')
        print('\nbefore')
        print(self.detail['before'])
        print('\nafter')
        print(self.detail['after'])


class GINISelector(TransformerMixin):
    def __init__(self):
        self.version = 'v2.0.2'
        self.detail = None
        self.selected_features = list()
        self.removed_features = list()

    def fit(self, df_xtrain, df_ytrain, **kwargs):
        n_jobs = kwargs.get('n_jobs', -1)
        feature_list = sorted(kwargs.get('feature_list', df_xtrain.columns.tolist()))
        df_xtest = kwargs.get('df_xtest', df_xtrain)
        df_ytest = kwargs.get('df_ytest', df_ytrain)
        if df_xtrain is df_xtest:
            cprint("warning: need to provide train and test data to do gini based feature selection", "red")

        # compute gini on train data
        if len(df_ytrain) > 100000:
            lst_gini_train = Parallel(n_jobs=n_jobs)(
                delayed(Metrics.get_gini)(df_ytrain, df_xtrain[c]) for c in feature_list)
        else:
            lst_gini_train = [Metrics.get_gini(df_ytrain, df_xtrain[c]) for c in feature_list]

        # compute gini on test data
        if len(df_ytest) > 100000:
            lst_gini_test = Parallel(n_jobs=n_jobs)(
                delayed(Metrics.get_gini)(df_ytest, df_xtest[c]) for c in feature_list)
        else:
            lst_gini_test = [Metrics.get_gini(df_ytest, df_xtest[c]) for c in feature_list]

        # select feature with same gini sign in train and test data
        df_res = pd.DataFrame({'var': feature_list,
                               'gini_train': lst_gini_train,
                               'gini_test': lst_gini_test})
        df_res.loc[:, 'selected'] = df_res['gini_train'] * df_res['gini_test'] > 0

        self.detail = df_res
        self.selected_features = df_res.loc[(df_res['selected'] == True), 'var'].tolist()
        self.removed_features = df_res.loc[(df_res['selected'] == False), 'var'].tolist()

        return self

    def transform(self, df_xtest, **kwargs):
        feature_list = kwargs.get('feature_list', df_xtest.columns.tolist())
        feature_list = sorted(set(feature_list) & set(self.selected_features))
        return df_xtest[feature_list]

    def summary(self):
        print('\nselected features:')
        print(self.selected_features)
        print('\nremoved features:')
        print(self.removed_features)
        print('\nsummary')
        print(self.detail)


class PSISelector(TransformerMixin):
    def __init__(self):
        self.version = 'v2.0.2'
        self.detail = None
        self.selected_features = list()
        self.removed_features = list()

    def fit(self, df_xtrain, df_ytrain, **kwargs):
        psi_threshold = kwargs.get('psi_threshold', 0.1)
        feature_list = sorted(kwargs.get('feature_list', df_xtrain.columns.tolist()))
        df_xtest = kwargs.get('df_xtest', df_xtrain)
        df_ytest = kwargs.get('df_ytest', df_ytrain)
        if df_xtest is df_xtrain:
            cprint("warning: need to provide train and test data to do PSI based feature selection", "red")

        # compute PSI
        df_psi = kwargs.get('df_psi', None)
        if df_psi is None:
            sr_psi = toad.metrics.PSI(df_xtrain[feature_list], df_xtest[feature_list])
            sr_psi.name = 'psi'
            sr_psi.index.name = 'var'
            df_psi = sr_psi.reset_index()

        # select feature with PSI < psi_threshold
        df_psi.loc[:, 'selected'] = df_psi['psi'] < psi_threshold

        self.detail = df_psi
        self.selected_features = df_psi.loc[(df_psi['selected'] == True), 'var'].tolist()
        self.removed_features = df_psi.loc[(df_psi['selected'] == False), 'var'].tolist()

        return self

    def transform(self, df_xtest, **kwargs):
        feature_list = kwargs.get('feature_list', df_xtest.columns.tolist())
        feature_list = sorted(set(feature_list) & set(self.selected_features))
        return df_xtest[feature_list]

    def summary(self):
        print('\nselected features:')
        print(self.selected_features)
        print('\nremoved features:')
        print(self.removed_features)
        print('\nsummary')
        print(self.detail)


class IVSelector(TransformerMixin):
    def __init__(self):
        self.version = 'v2.0.2'
        self.detail = None
        self.selected_features = list()
        self.removed_features = list()

    def fit(self, df_xtrain, df_ytrain, **kwargs):
        iv_threshold = kwargs.get('iv_threshold', 0.02)
        n_jobs = kwargs.get('n_jobs', -1)
        feature_list = sorted(kwargs.get('feature_list', df_xtrain.columns.tolist()))

        # compute IV
        df_iv = kwargs.get('df_iv', None)
        if df_iv is None:
            if len(df_ytrain) > 100000:
                lst_iv = Parallel(n_jobs=n_jobs)(
                    delayed(Metrics.get_iv)(df_ytrain, df_xtrain[c]) for c in feature_list)
            else:
                lst_iv = [Metrics.get_iv(df_ytrain, df_xtrain[c]) for c in feature_list]
            df_iv = pd.DataFrame({'var': feature_list, 'iv': lst_iv})

        # select feature with IV >= iv_threshold
        df_iv.loc[:, 'selected'] = df_iv['iv'] >= iv_threshold

        self.detail = df_iv
        self.selected_features = df_iv.loc[(df_iv['selected'] == True), 'var'].tolist()
        self.removed_features = df_iv.loc[(df_iv['selected'] == False), 'var'].tolist()

        return self

    def transform(self, df_xtest, **kwargs):
        feature_list = kwargs.get('feature_list', df_xtest.columns.tolist())
        feature_list = sorted(set(feature_list) & set(self.selected_features))
        return df_xtest[feature_list]

    def summary(self):
        print('\nselected features:')
        print(self.selected_features)
        print('\nremoved feaures:')
        print(self.removed_features)
        print('\nsummary')
        print(self.detail)


class VIFSelector(TransformerMixin):
    def __init__(self):
        self.version = 'v2.0.2'
        self.detail = None
        self.selected_features = list()
        self.removed_features = list()

    def fit(self, df_xtrain, df_ytrain, **kwargs):
        vif_threshold = kwargs.get('vif_threshold', 10)
        n_jobs = kwargs.get('n_jobs', -1)
        feature_list = kwargs.get('feature_list', df_xtrain.columns.tolist())

        # compute VIF
        vif = Parallel(n_jobs=n_jobs)(
            delayed(variance_inflation_factor)(df_xtrain.values, i) for i in range(df_xtrain[feature_list].shape[1]))

        # select features with VIF < vif_threshold
        df_res = pd.DataFrame({'var': feature_list,
                               'vif': [round(v, 3) for v in vif]})
        df_res.loc[:, 'selected'] = df_res['vif'] < vif_threshold

        self.detail = df_res
        self.selected_features = df_res.loc[(df_res['selected'] == True), 'var'].tolist()
        self.removed_features = df_res.loc[(df_res['selected'] == False), 'var'].tolist()

        return self

    def transform(self, df_xtest, **kwargs):
        feature_list = kwargs.get('feature_list', df_xtest.columns.tolist())
        feature_list = sorted(set(feature_list) & set(self.selected_features))
        return df_xtest[feature_list]

    def summary(self):
        print('\nselected features:')
        print(self.selected_features)
        print('\nremoved features:')
        print(self.removed_features)
        print('\nsummary')
        print(self.detail)


class BoostingTreeSelector(TransformerMixin):
    def __init__(self):
        self.version = 'v2.0.2'
        self.detail = None
        self.selected_features = list()
        self.removed_features = list()

    def fit(self, df_xtrain, df_ytrain, **kwargs):
        feature_list = sorted(kwargs.get('feature_list', df_xtrain.columns.tolist()))

        df_xtest = kwargs.get('df_xtest', None)
        df_ytest = kwargs.get('df_ytest', None)
        select_frac = kwargs.get('select_frac', 0.9)

        model = lgb.LGBMClassifier(boosting_type='gbdt', num_leaves=31, max_depth=5,
                                   learning_rate=0.02, n_estimators=200,
                                   min_split_gain=0, min_child_weight=1e-3, min_child_samples=20,
                                   subsample=1., subsample_freq=0, colsample_bytree=1.,
                                   reg_alpha=0., reg_lambda=0., random_state=0,
                                   n_jobs=4, silent=True, importance_type='split')

        model.fit(df_xtrain, df_ytrain,
                  eval_metric='auc',
                  eval_set=[(df_xtrain, df_ytrain), (df_xtest, df_ytest)],
                  early_stopping_rounds=10,
                  verbose=10)

        df_res = pd.DataFrame({
            'feature': feature_list,
            'feature_importance': model.feature_importances_
        }).sort_values(by='feature_importance', ascending=False).reset_index(drop=True)

        select_num = int(select_frac * len(df_res[df_res['feature_importance'] != 0]))
        df_res['selected'] = False
        df_res.loc[0:select_num, 'selected'] = True

        self.detail = df_res
        self.selected_features = df_res.loc[(df_res['selected'] == True), 'feature'].tolist()
        self.removed_features = df_res.loc[(df_res['selected'] == False), 'feature'].tolist()

        return self

    def transform(self, df_xtest, **kwargs):
        feature_list = kwargs.get('feature_list', df_xtest.columns.tolist())
        feature_list = sorted(set(feature_list) & set(self.selected_features))
        return df_xtest[feature_list]

    def summary(self):
        print('\nselected features:')
        print(self.selected_features)
        print('\nremoved features:')
        print(self.removed_features)
        print('\nsummary')
        print(self.detail)
