from abc import abstractmethod, ABC
from itertools import compress
import numpy as np
import mlflow
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from sklearn.feature_selection import SequentialFeatureSelector
from skopt import forest_minimize


class MaskAbleList(list):
    def __getitem__(self, index):
        try:
            return super(MaskAbleList, self).__getitem__(index)
        except TypeError:
            return MaskAbleList(compress(self, index))


def what_should_i_use():
    answer, supervision, method_class = "", "", ""

    print("Does your problem have specific targets? [y, n]")
    while not (answer in ['y', 'n']):
        answer = str(input())

    if answer == 'y':
        print("Choose Supervised Methods. Unsupervised maybe would be useful to eliminate"
              " duplicated info, but supervised methods can do it as well.")
    else:
        print("Choose Unsupervised Methods")

    print("Do you already have a specific model in mind? [y, n]")
    while not (answer in ['y', 'n']):
        answer = str(input())

    if answer == 'y':
        print("Choose Filter Methods")
    else:
        print("Choose model based methods such as Intrinsic or Wrapper Models.")
        print("Do you have a lot of time to perform your analysis? [y, n]")
        while not (answer in ['y', 'n']):
            answer = str(input())

        if answer == 'y':
            print("Choose Wrapper Methods. They will perform better than Intrinsic Selectors.")
        else:
            print("Choose Intrinsic Methods. They will not perform as well as a wrapper methods"
                  " but they work really fast!")


class FeatureSelection(ABC):
    def __init__(self, experiment_path="./"):
        self.experiment_path = experiment_path

    @abstractmethod
    def _registry_experiment(self, run_name: str, parameters: dict = {}, metrics: dict = {}):
        with mlflow.start_run(run_name=run_name):
            for metric in list(metrics.keys()):
                mlflow.log_metric(metric, metrics[metric])

            for parameter in list(parameters.keys()):
                mlflow.log_param(parameter, parameters[parameter])


class SupervisedFeatureSelection(ABC, FeatureSelection):
    @abstractmethod
    def select(self, data, target):
        pass


class UnsupervisedFeatureSelection(ABC, FeatureSelection):
    @abstractmethod
    def select(self, data):
        pass


class WrapperSelection(ABC, FeatureSelection):
    @abstractmethod
    def _get_cross_validation_score(self, data, features, target, model, run_name,
                                    model_name, verbose=False):
        maes, r2s, rmses = [], [], []
        for fold in data['FOLD'].unique():
            train_data = data[data['FOLD'] != fold]
            validation_data = data[data['FOLD'] == fold]

            # model = LinearRegression(normalize=True)
            train_data.dropna(subset=features, inplace=True)
            train_data.dropna(subset=[target], inplace=True)

            validation_data.dropna(subset=features, inplace=True)
            validation_data.dropna(subset=[target], inplace=True)

            model.fit(train_data[features], train_data[target])
            y_predicted = model.predict(validation_data[features])

            maes.append(mean_absolute_error(validation_data[target], y_predicted))
            r2s.append(r2_score(validation_data[target], y_predicted))
            rmses.append(np.sqrt(mean_squared_error(validation_data[target], y_predicted)))

        if verbose:
            print(np.mean(maes), features)

        self._registry_experiment(run_name=run_name,
                                  parameters={"features": features, "model_name": model_name},
                                  metrics={"mae": np.mean(maes), "rmse": np.mean(rmses), "r2": np.mean(r2s)})
        return np.mean(maes)


class FilterSelection(ABC, FeatureSelection):
    @abstractmethod
    def select(self, data, target):
        pass


class IntrinsicSelection(ABC, FeatureSelection):
    @abstractmethod
    def select(self, data, target, model):
        pass


class RandomSearch(ABC, FeatureSelection, WrapperSelection):
    @abstractmethod
    def _transform_params_in_feature_set(self, params, all_features):
        feature_set = []
        for i in range(len(params)):
            if params[i] > 0.5:
                feature_set.append(all_features[i])
        return feature_set

    @staticmethod
    def _create_feature_space(features):
        space = []
        for i in range(len(features)):
            space.append([0, 1])

        return space


class BayesianSearch(RandomSearch):
    def search_feature_sets(self, features, target):
        def objective_function(params):
            nonlocal target
            feature_set = self._transform_params_in_feature_set(params)
            score = self._get_cross_validation_score(feature_set, target, run_name="bayesian_search")
            return score

        optimization_history = forest_minimize(objective_function, self._create_feature_space(features), n_calls=100,
                                               n_initial_points=50)

        return optimization_history


class ManualSearch(WrapperSelection, SupervisedFeatureSelection):
    def test_feature_set(self, data, features, target, model, run_name, model_name, verbose=False):
        self._get_cross_validation_score(data, features, target, model, run_name=run_name,
                                         model_name=model_name, verbose=verbose)


class RecursiveElimination(WrapperSelection, SupervisedFeatureSelection):
    pass


class ForwardSelection(WrapperSelection, SupervisedFeatureSelection):
    pass
