# -*- coding: utf-8 -*-
__version__ = 'v1.0.0'
__author__ = ['Ouyang Ruofei']

import numpy as np
import pandas as pd
from termcolor import cprint
from joblib import Parallel, delayed
from sklearn.metrics import roc_auc_score, roc_curve

import statsmodels.api as sm
from sklearn.base import TransformerMixin, BaseEstimator, ClassifierMixin


class Benchmark(BaseEstimator, ClassifierMixin):
    def __init__(self):
        self.model = None
        self.model_detail = None
        self.select_detail = dict()
        self.selected_features = None
        self.removed_features = dict()
        self.coef_selector = None
        self.pvalue_selector = None

    def fit(self, df_xtrain, df_ytrain, **kwargs):
        positive_coef = kwargs.get('positive_coef', False)
        remove_method = kwargs.get('remove_method', 'iv')
        df_iv = kwargs.get('df_iv', None)
        n_jobs = kwargs.get('n_jobs', -1)

        pvalue_threshold = kwargs.get('pvalue_threshold', 0.05)

        feature_list = sorted(kwargs.get('feature_list', df_xtrain.columns.tolist()))
        self.selected_features = feature_list

        # remove variable with inconsistent trend between woe and coefficient
        coef_selector = CoefSelector()
        coef_selector.fit(df_xtrain[self.selected_features], df_ytrain,
                          positive_coef=positive_coef,
                          remove_method=remove_method,
                          df_iv=df_iv,
                          n_jobs=n_jobs)
        self.selected_features = coef_selector.selected_features
        self.coef_selector = coef_selector
        self.removed_features['by_coef'] = coef_selector.removed_features
        self.select_detail['by_coef'] = coef_selector.detail
        print(self.selected_features)

        # remove variable with insignificant p value
        pvalue_selector = PValueSelector()
        pvalue_selector.fit(df_xtrain[self.selected_features], df_ytrain,
                            pvalue_threshold=pvalue_threshold)
        self.selected_features = pvalue_selector.selected_features
        self.pvalue_selector = pvalue_selector
        self.removed_features['by_pvalue'] = pvalue_selector.removed_features
        self.select_detail['by_pvalue'] = pvalue_selector.detail
        print(self.selected_features)

        # run logit model
        model = Logistic()
        model.fit(df_xtrain[self.selected_features], df_ytrain)

        self.model = model
        self.model_detail = model.detail

        return self

    def predict(self, df_xtest, **kwargs):
        # sm.add_constant won't add a constant if there exists a column with variance 0
        df_xtest = sm.add_constant(df_xtest)
        df_xtest['const'] = 1
        return self.model.predict(df_xtest[['const'] + self.selected_features])

    def predict_proba(self, df_xtest, **kwargs):
        # sm.add_constant won't add a constant if there exists a column with variance 0
        df_xtest = sm.add_constant(df_xtest)
        df_xtest['const'] = 1
        yprob = self.model.predict(df_xtest[['const'] + self.selected_features])
        res = np.zeros((len(df_xtest), 2))
        res[:, 1] = yprob
        res[:, 0] = 1 - yprob
        return res

    def summary(self):
        print('\nselected features:')
        print(self.selected_features)
        print('\nremoved features by trend:')
        print(self.removed_features['by_trend'])
        print('\nremoved feature by pvalue:')
        print(self.removed_features['by_pvalue'])
        print('\nmodel summary:')
        print(self.model_detail)


class Logistic(BaseEstimator, ClassifierMixin):
    def __init__(self):
        self.version = 'v1.0.2'
        self.model = None
        self.detail = None
        self.selected_features = None

    def fit(self, df_xtrain, df_ytrain, **kwargs):
        self.selected_features = df_xtrain.columns.tolist()

        df_xtrain_const = sm.add_constant(df_xtrain)

        # model training. default using newton method, if fail use bfgs method
        try:
            self.model = sm.Logit(df_ytrain, df_xtrain_const).fit(method='newton', maxiter=100)
        except:
            cprint("warning:  exist strong correlated features, "
                   "got singular matrix in linear model, retry bfgs method instead.",
                   'red')
            self.model = sm.Logit(df_ytrain, df_xtrain_const).fit(method='bfgs', maxiter=100)

        # prepare model result
        self.detail = pd.DataFrame({'var': df_xtrain_const.columns.tolist(),
                                    'coef': self.model.params,
                                    'std_err': [round(v, 2) for v in self.model.bse],
                                    'z': [round(v, 2) for v in self.model.tvalues],
                                    'pvalue': [round(v, 2) for v in self.model.pvalues]})
        self.detail['std_var'] = df_xtrain.std()
        self.detail['std_var'] = self.detail['std_var'].apply(lambda x: round(x, 2))
        self.detail['feature_importance'] = abs(self.detail['coef']) * self.detail['std_var']
        self.detail['feature_importance'] = self.detail['feature_importance'] / self.detail['feature_importance'].sum()
        self.detail['feature_importance'] = self.detail['feature_importance'].apply(lambda x: round(x, 2))

        return self

    def predict(self, df_xtest, **kwargs):
        # sm.add_constant won't add a constant if there exists a column with variance 0
        df_xtest = sm.add_constant(df_xtest)
        df_xtest['const'] = 1
        return self.model.predict(df_xtest[['const'] + self.selected_features])

    def predict_proba(self, df_xtest, **kwargs):
        # sm.add_constant won't add a constant if there exists a column with variance 0
        df_xtest = sm.add_constant(df_xtest)
        df_xtest['const'] = 1
        yprob = self.model.predict(df_xtest[['const'] + self.selected_features])
        res = np.zeros((len(df_xtest), 2))
        res[:, 1] = yprob
        res[:, 0] = 1 - yprob
        return res

    def summary(self):
        print(self.detail)

    def get_importance(self):
        return self.detail.drop('const', axis=0)


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


class CoefSelector(TransformerMixin):
    def __init__(self):
        self.detail = None
        self.selected_features = list()
        self.removed_features = list()

    def fit(self, df_xtrain, df_ytrain, **kwargs):
        positive_coef = kwargs.get('positive_coef', False)
        remove_method = kwargs.get('remove_method', 'iv')
        df_iv = kwargs.get('df_iv', None)
        n_jobs = kwargs.get('n_jobs', -1)
        feature_list = sorted(kwargs.get('feature_list', df_xtrain.columns.tolist()))

        self.selected_features = feature_list
        self.detail = list()

        if remove_method == 'iv':
            if df_iv is None:
                if len(df_ytrain) > 10000000:
                    lst_iv = Parallel(n_jobs=n_jobs)(
                        delayed(Metrics.get_iv)(df_ytrain, df_xtrain[c]) for c in feature_list)
                else:
                    lst_iv = [Metrics.get_iv(df_ytrain, df_xtrain[c]) for c in feature_list]
                df_iv = pd.DataFrame({'var': feature_list, 'iv': lst_iv})

            df_iv = df_iv[['var', 'iv']]

        while True:
            model = Logistic()
            model.fit(df_xtrain[self.selected_features], df_ytrain)

            if remove_method == 'feature_importance':
                df_res = model.get_importance()[['var', 'coef', 'pvalue', 'feature_importance']]
                df_res = df_res.reset_index(drop=True)
                self.detail.append(df_res)
            else:
                df_res = model.get_importance()[['var', 'coef', 'pvalue']]
                df_res = df_res.reset_index(drop=True)
                df_res = df_res.merge(df_iv, on=['var'], how='left')
                self.detail.append(df_res)

            if df_res['pvalue'].isnull().sum() != 0:
                df_remove = df_res.loc[(df_res['pvalue'].isnull()), :]
                df_remove = df_remove.sort_values(by=f'{remove_method}', ascending=True)
                df_remove = df_remove.reset_index(drop=True)
                remove_var = df_remove.loc[0, 'var']
                self.selected_features.remove(remove_var)
                self.removed_features.append(remove_var)
            else:
                if positive_coef is True:
                    df_res['coef'] = - df_res['coef']

                df_remove = df_res.loc[(df_res['coef'] >= 0), :]
                if len(df_remove) != 0:
                    df_remove = df_remove.sort_values(by=f'{remove_method}', ascending=True)
                    df_remove = df_remove.reset_index(drop=True)
                    remove_var = df_remove.loc[0, 'var']
                    self.selected_features.remove(remove_var)
                    self.removed_features.append(remove_var)
                else:
                    break

            if len(self.selected_features) == 0:
                break

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
        for idx, df in enumerate(self.detail):
            print('iter:', idx)
            print(self.detail[idx])


class PValueSelector(TransformerMixin):
    def __init__(self):
        self.detail = None
        self.selected_features = list()
        self.removed_features = list()

    def fit(self, df_xtrain, df_ytrain, **kwargs):
        pvalue_threshold = kwargs.get('pvalue_threshold', 0.05)
        feature_list = sorted(kwargs.get('feature_list', df_xtrain.columns.tolist()))

        self.selected_features = feature_list
        self.detail = list()

        while True:
            model = Logistic()
            model.fit(df_xtrain[self.selected_features], df_ytrain)

            df_res = model.get_importance()[['var', 'coef', 'pvalue']]
            df_res = df_res.reset_index(drop=True)
            self.detail.append(df_res)

            df_remove = df_res.loc[(df_res['pvalue'] > pvalue_threshold), :]
            if len(df_remove) != 0:
                df_remove = df_remove.sort_values(by='pvalue', ascending=False)
                df_remove = df_remove.reset_index()
                remove_var = df_remove.loc[0, 'var']
                self.selected_features.remove(remove_var)
                self.removed_features.append(remove_var)
            else:
                break

            if len(self.selected_features) == 0:
                break
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
        for idx, df in enumerate(self.detail):
            print('iter:', idx)
            print(self.detail[idx])
