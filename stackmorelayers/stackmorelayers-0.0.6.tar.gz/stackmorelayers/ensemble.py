from io import TextIOWrapper
from itertools import repeat
from operator import attrgetter
from os import makedirs, remove
from os.path import join as join_path
from pathlib import Path
from pickle import load
from tarfile import open as tar_open
from tempfile import TemporaryDirectory
from typing import Optional, Dict, Any, Callable, Literal, Union, List, Tuple, Iterable, overload, Sequence, Iterator

import numpy as np
import pandas as pd
from catboost import CatBoost, Pool, CatBoostClassifier
from scipy.stats import gmean
from sklearn.model_selection import BaseCrossValidator, BaseShuffleSplit
from tqdm import tqdm

from stackmorelayers.typing import (
    KWARGS_OR_ITERABLE, SPLITTER, DATASET, PATH, SPLIT_ITERABLE, KWARGS, COLUMN,
    ARRAY_INDEXER
)
from stackmorelayers.utils import string_to_tarfile, object_to_tarfile

__all__ = (
    "CatBoostEnsemble",
)

PICKLE_PROTOCOL: Literal[5] = 5

CB_BLENDING_DUMP_BASENAME = "catboost_blending_coefficients.txt"
CB_MODEL_KWARGS_DUMP_BASENAME = "catboost_model_kwargs.pkl"
CB_MODEL_VAL_SCORES_DUMP_BASENAME = "catboost_validation_scores.pkl"
CB_POOL_KWARGS_DUMP_BASENAME = "catboost_pool_constructor_kwargs.pkl"
CB_FIT_KWARGS_DUMP_BASENAME = "catboost_fit_kwargs.pkl"
CB_SPLIT_INDICES_DUMP_BASENAME = "catboost_split_indices.pkl"


class CatBoostEnsemble:
    """Ensemble of the CatBoost models"""
    __slots__ = (
        'model_factory',
        'model_kwargs',
        'n_models',
        'models',
        'blending_coefficients',
        'cat_features',
        'elapsed_iters',
        'validation_scores',
        'rng',
        'pool_constructor_kwargs',
        'split_indices',
        'fit_kwargs',
        'is_fit'
    )

    def __init__(
            self,
            model_factory: Callable[..., CatBoost] = CatBoostClassifier,
            *,
            cat_features: Optional[Union[Iterable[int], Iterable[str]]] = None,
            n_models: int = 5,
            model_kwargs: KWARGS_OR_ITERABLE = (),
            seed: Optional[int] = None
    ) -> None:
        """
        Ensemble of the CatBoost models.

        Args:
            model_factory:  model constructor
            cat_features:   list of categorical features
            n_models:       number of models to use
            model_kwargs:   keyword arguments passed to the model constructors
            seed:           RNG seed
        """

        if not hasattr(model_factory, '__call__'):
            raise TypeError("Parameter model_factory must be a Callable that returns a model instance")
        self.model_factory = model_factory

        if isinstance(model_kwargs, dict):
            self.model_kwargs: Tuple[KWARGS, ...] = tuple(repeat(model_kwargs, n_models))
        elif hasattr(model_kwargs, '__iter__'):
            self.model_kwargs = tuple(model_kwargs)
            if len(self.model_kwargs) == 0:
                self.model_kwargs = tuple(repeat({}, n_models))
            elif n_models != len(self.model_kwargs):
                raise IndexError(
                    f"Parameter model_kwargs, if iterable, should contain {n_models=} elements, "
                    f"not {len(self.model_kwargs)}"
                )
        else:
            raise TypeError("Parameter model_kwargs must be a dictionary or Callable that returns a dictionary")

        if not np.issubdtype(type(n_models), np.integer) or not 0 < n_models < 100_000:
            raise TypeError("Parameter n_models must be an int from [1, 99_999]")
        self.n_models = n_models

        if cat_features is not None:
            if not hasattr(cat_features, '__iter__'):
                raise TypeError("Parameter cat_features must be an Iterable of indices or feature names, or None")
            self.cat_features: Optional[Union[Tuple[str, ...], Tuple[int, ...]]] = tuple(cat_features)  # type: ignore
        else:
            self.cat_features = cat_features

        self.models: List[CatBoost] = []
        self.blending_coefficients: List[float] = []

        self.elapsed_iters = 0
        self.rng = np.random.default_rng(seed)
        self.validation_scores: List[Dict[str, Any]] = []

        self.pool_constructor_kwargs: Dict[str, Any] = {}
        self.fit_kwargs: Tuple[Dict[str, Any], ...] = ()
        self.split_indices: Tuple[Tuple[ARRAY_INDEXER, ARRAY_INDEXER], ...] = ()
        self.is_fit = False

    def _reset(self) -> None:
        self.is_fit = False
        self.elapsed_iters = 0
        self.models = []
        self.blending_coefficients = []
        self.validation_scores = []
        self.pool_constructor_kwargs = {}
        self.fit_kwargs = ()
        self.split_indices = ()

    @overload
    def fit(self,
            train_dataset: DATASET,
            eval_dataset: None,
            *,
            splitter: SPLIT_ITERABLE,
            groups: None,
            fit_kwargs: KWARGS_OR_ITERABLE,
            pool_constructor_kwargs: Optional[KWARGS],
            progress_bar: Callable[[Sequence], Iterator]) -> 'CatBoostEnsemble':
        pass

    @overload
    def fit(self,
            train_dataset: DATASET,
            eval_dataset: None,
            *,
            splitter: Union[BaseShuffleSplit, BaseCrossValidator],
            groups: Optional[COLUMN],
            fit_kwargs: KWARGS_OR_ITERABLE,
            pool_constructor_kwargs: Optional[KWARGS],
            progress_bar: Callable[[Sequence], Iterator]) -> 'CatBoostEnsemble':
        pass

    @overload
    def fit(self,
            train_dataset: DATASET,
            eval_dataset: DATASET,
            *,
            splitter: None,
            groups: None,
            fit_kwargs: KWARGS_OR_ITERABLE,
            pool_constructor_kwargs: Optional[KWARGS],
            progress_bar: Callable[[Sequence], Iterator]) -> 'CatBoostEnsemble':
        pass

    def fit(self,
            train_dataset: DATASET,
            eval_dataset: Optional[DATASET] = None,
            *,
            splitter: Optional[SPLITTER] = None,
            groups: Optional[COLUMN] = None,
            fit_kwargs: KWARGS_OR_ITERABLE = (),
            pool_constructor_kwargs: Optional[KWARGS] = None,
            progress_bar: Callable[[Sequence], Iterator] = tqdm) -> 'CatBoostEnsemble':
        """
        Fit models.

        Args:
            train_dataset:            fitting data
            eval_dataset:             model evaluation data
            splitter:                 index splitter
                                      (Iterable of indexer array pairs | sklearn CrossValidator / ShuffleSplit | None)
            groups:                   split groups
                                      (could only be used if split_iterator is sklearn CrossValidator or ShuffleSplit)
            fit_kwargs:               keyword arguments passed to the fit method of the CatBoost models
                                      (dict | Iterable[dict])
            pool_constructor_kwargs:  keyword arguments passed to the catboost.Pool constructors
                                      (dict)
            progress_bar:             progress bar class in a tqdm manner
        Returns:
            Self
        """
        self._reset()
        if pool_constructor_kwargs is None:
            pool_constructor_kwargs = {}
        self.pool_constructor_kwargs = pool_constructor_kwargs

        if isinstance(fit_kwargs, dict):
            fit_kwargs = tuple(repeat(fit_kwargs, self.n_models))
        elif hasattr(fit_kwargs, '__iter__'):
            fit_kwargs = tuple(fit_kwargs)
            if len(fit_kwargs) == 0:
                fit_kwargs = tuple(repeat({}, self.n_models))
            elif self.n_models != len(fit_kwargs):
                n_models = self.n_models
                raise IndexError(
                    f"Parameter fit_kwargs, if iterable, should contain {n_models=} elements, "
                    f"not {len(fit_kwargs)}"
                )
        else:
            raise TypeError("Parameter fit_kwargs must be a dictionary or Callable that returns a dictionary")
        self.fit_kwargs = fit_kwargs

        if splitter is None:
            if groups is not None:
                raise TypeError("Parameter groups cannot be set if splitter is not used")
            if not isinstance(train_dataset, Pool):
                features, labels = train_dataset
                train_dataset = Pool(features, labels, cat_features=self.cat_features, **pool_constructor_kwargs)
            if not isinstance(eval_dataset, Pool):
                if eval_dataset is None:
                    raise TypeError("Parameter eval_dataset should not be None if splitter is not used")
                features, labels = eval_dataset
                eval_dataset = Pool(features, labels, cat_features=self.cat_features, **pool_constructor_kwargs)

            def get_train_eval() -> Tuple[Pool, Pool]:
                return train_dataset, eval_dataset

        elif eval_dataset is not None:
            raise TypeError("Parameter eval_dataset should not be set if splitter is set")

        elif isinstance(train_dataset, Pool):
            raise TypeError("Parameter train_dataset cannot be a catboost.Pool if splitter is set")

        else:
            features, labels = train_dataset
            if isinstance(features, pd.DataFrame):
                features_idx_selector = features.iloc
            else:
                features_idx_selector = features
            if isinstance(labels, pd.Series):
                labels_idx_selector = labels.iloc
            else:
                labels_idx_selector = labels

            if isinstance(splitter, (BaseShuffleSplit, BaseCrossValidator)):
                try:
                    if splitter.random_state is None:
                        splitter.random_state = self.rng.integers(0, 2 ** 32)
                except AttributeError:
                    pass
                n_splits = splitter.get_n_splits(features, labels, groups)
                splitter = tuple(splitter.split(features, labels, groups))
                self.split_indices = splitter
            else:
                if groups is not None:
                    raise TypeError(
                        "Parameter groups cannot be set if splitter is not sklearn CrossValidator or ShuffleSplit"
                    )
                if not isinstance(splitter, tuple):
                    splitter = tuple(splitter)
                self.split_indices = splitter
                n_splits = len(splitter)
            splitter = iter(splitter)

            if n_splits != self.n_models:
                raise ValueError(f"The number of splits {n_splits} does not match the number of models {self.n_models}")
            del n_splits

            def get_train_eval() -> Tuple[Pool, Pool]:
                train_idx, eval_idx = next(splitter)  # type: ignore
                train_split = Pool(
                    features_idx_selector[train_idx],
                    labels_idx_selector[train_idx],
                    cat_features=self.cat_features,
                    **pool_constructor_kwargs
                )
                eval_split = Pool(
                    features_idx_selector[eval_idx],
                    labels_idx_selector[eval_idx],
                    cat_features=self.cat_features,
                    **pool_constructor_kwargs
                )
                return train_split, eval_split

        try:
            del features, labels
        except NameError:
            pass

        for model_kwargs, fit_kwargs in zip(progress_bar(self.model_kwargs), fit_kwargs):

            model = self.model_factory(
                cat_features=self.cat_features,
                random_seed=self.rng.integers(0, 2 ** 63),
                **model_kwargs
            )
            train_set, eval_set = get_train_eval()
            model.fit(
                train_set,
                eval_set=eval_set,
                **fit_kwargs
            )
            self.models.append(model)
            self.blending_coefficients.append(1.0)
            self.validation_scores.append(model.get_best_score())

            self.elapsed_iters += 1

        self.is_fit = True
        return self

    def apply(self,
              dataset: Union[Pool, pd.DataFrame, np.ndarray],
              method: Literal['predict', 'predict_proba', 'predict_log_proba'] = 'predict',
              *,
              avg_method: Literal['mean', 'gmean', 'concat'] = 'mean') -> np.ndarray:
        """
        Apply models to data.

        Args:
            dataset:     input data
            method:      applying method. Possible values:
                         ('predict' | 'predict_proba' | 'predict_log_proba')
            avg_method:  ensemble prediction averaging method. Possible values:
                         ('mean' | 'gmean' | 'concat')
        Returns:
            Array of predictions
        """
        if not self.is_fit:
            raise RuntimeError("You should train your model before making any predictions")
        if avg_method not in {'mean', 'gmean', 'concat'}:
            raise NameError(f"Does not have such an option: {avg_method}")

        iterator = zip(self.models, self.blending_coefficients)
        if avg_method == 'mean':
            model, coeff = next(iterator)
            result = getattr(model, method)(dataset)
            if np.issubdtype(result.dtype, np.floating):
                result *= coeff
                for model, coeff in iterator:
                    model_pred = getattr(model, method)(dataset)
                    model_pred *= coeff
                    result += model_pred
            else:
                result = result * coeff
                for model, coeff in iterator:
                    result += getattr(model, method)(dataset) * coeff

            result *= (1 / len(self.models))
            return result

        result = np.array([
            getattr(model, method)(dataset) * coeff
            for model, coeff in iterator
        ])
        if avg_method == 'gmean':
            result = gmean(result)
        return result

    def save_models(self, path: PATH, *, exist_ok: bool = False) -> Path:
        """
        Save models and their meta info to disk. The resulting file can be read back using the load_models method.

        Args:
            path:      prefix of the save file
            exist_ok:  whether to rewrite possibly existing file at the path location
        Returns:
            Save file path
        """
        if not self.is_fit:
            raise RuntimeError("You should train your model before saving")
        path = Path(path)
        makedirs(path.parent, exist_ok=True)

        with tar_open(path, 'w:bz2' if exist_ok else 'x:bz2') as tar:
            with TemporaryDirectory() as tmp_path:
                model_path = join_path(tmp_path, 'tmp.cbm')
                for i, model in enumerate(self.models, 1):
                    model.save_model(model_path)
                    tar.add(model_path, f'catboost_{i:05}.cbm')

            fileobj, tar_info = string_to_tarfile(
                CB_BLENDING_DUMP_BASENAME,
                '\n'.join(map(str, self.blending_coefficients))
            )
            tar.addfile(tar_info, fileobj=fileobj)

            fileobj, tar_info = object_to_tarfile(
                CB_MODEL_KWARGS_DUMP_BASENAME,
                self.model_kwargs,
                protocol=PICKLE_PROTOCOL
            )
            tar.addfile(tar_info, fileobj=fileobj)

            fileobj, tar_info = object_to_tarfile(
                CB_MODEL_VAL_SCORES_DUMP_BASENAME,
                self.validation_scores,
                protocol=PICKLE_PROTOCOL
            )
            tar.addfile(tar_info, fileobj=fileobj)

            fileobj, tar_info = object_to_tarfile(
                CB_POOL_KWARGS_DUMP_BASENAME,
                self.pool_constructor_kwargs,
                protocol=PICKLE_PROTOCOL
            )
            tar.addfile(tar_info, fileobj=fileobj)

            fileobj, tar_info = object_to_tarfile(
                CB_FIT_KWARGS_DUMP_BASENAME,
                self.fit_kwargs,
                protocol=PICKLE_PROTOCOL
            )
            tar.addfile(tar_info, fileobj=fileobj)

            fileobj, tar_info = object_to_tarfile(
                CB_SPLIT_INDICES_DUMP_BASENAME,
                self.split_indices,
                protocol=PICKLE_PROTOCOL
            )
            tar.addfile(tar_info, fileobj=fileobj)
        return path

    def load_models(self, path: PATH) -> 'CatBoostEnsemble':
        """
        Load previously saved CatBoostEnsemble from disk.

        Args:
            path:  save file path
        Returns:
            Self
        """
        self._reset()
        with tar_open(path, 'r:bz2') as tar:
            files = sorted(tar, key=attrgetter('name'))
            for member in files:
                if member.name == CB_MODEL_KWARGS_DUMP_BASENAME:
                    content = tar.extractfile(member)
                    if content is None:
                        raise RuntimeError(f"Cannot parse {CB_MODEL_KWARGS_DUMP_BASENAME} from the archive")
                    self.model_kwargs = load(content)
                    break
            else:
                raise RuntimeError(f"Cannot find {CB_MODEL_KWARGS_DUMP_BASENAME} file in the archive")

            model_kwargs = iter(self.model_kwargs)
            with TemporaryDirectory() as tmp_path:
                for member in files:
                    member_name = member.name
                    if member_name.endswith('.cbm'):
                        tar.extract(member, tmp_path)
                        try:
                            model = self.model_factory(
                                cat_features=self.cat_features,
                                random_seed=self.rng.integers(0, 2 ** 63),
                                **next(model_kwargs)
                            )
                        except StopIteration:
                            raise IndexError("The number of model kwargs does not match the number of models")
                        model_path = join_path(tmp_path, member_name)
                        model.load_model(model_path)
                        remove(model_path)
                        self.models.append(model)
                    elif member_name == CB_BLENDING_DUMP_BASENAME:
                        content = tar.extractfile(member)
                        if content is None:
                            raise RuntimeError(f"Cannot parse {CB_BLENDING_DUMP_BASENAME} from the archive")
                        try:
                            for i, cf in enumerate(map(str.strip, TextIOWrapper(content)), 1):
                                self.blending_coefficients.append(float(cf))
                        except ValueError as e:
                            raise ValueError(f"Cannot parse to float {i} line in {member_name}") from e
                    elif member_name == CB_MODEL_VAL_SCORES_DUMP_BASENAME:
                        content = tar.extractfile(member)
                        if content is None:
                            raise RuntimeError(f"Cannot parse {CB_MODEL_VAL_SCORES_DUMP_BASENAME} from the archive")
                        self.validation_scores = load(content)
                    elif member_name == CB_POOL_KWARGS_DUMP_BASENAME:
                        content = tar.extractfile(member)
                        if content is None:
                            raise RuntimeError(f"Cannot parse {CB_POOL_KWARGS_DUMP_BASENAME} from the archive")
                        self.pool_constructor_kwargs = load(content)
                    elif member_name == CB_FIT_KWARGS_DUMP_BASENAME:
                        content = tar.extractfile(member)
                        if content is None:
                            raise RuntimeError(f"Cannot parse {CB_FIT_KWARGS_DUMP_BASENAME} from the archive")
                        self.fit_kwargs = load(content)
                    elif member_name == CB_SPLIT_INDICES_DUMP_BASENAME:
                        content = tar.extractfile(member)
                        if content is None:
                            raise RuntimeError(f"Cannot parse {CB_SPLIT_INDICES_DUMP_BASENAME} from the archive")
                        self.split_indices = load(content)

        self.n_models = len(self.models)
        if self.n_models != len(self.blending_coefficients):
            raise IndexError("The number of blending coefficients does not match the number of models")
        if self.n_models != len(self.validation_scores):
            raise IndexError("The number of validation scores does not match the number of models")
        if self.n_models != len(self.fit_kwargs):
            raise IndexError("The number of fit kwargs does not match the number of models")

        self.elapsed_iters = self.n_models
        self.is_fit = True
        return self

    def reseed(self, seed: Optional[int] = None) -> 'CatBoostEnsemble':
        """
        Reseed random number generator.

        Args:
            seed:  rng seed
        Returns:
            Self
        """
        self.rng = np.random.default_rng(seed)
        return self

    def get_mean_feature_importance(self,
                                    feature_names: Optional[Iterable[str]] = None,
                                    *,
                                    drop_null: bool = True,
                                    sort: bool = True) -> pd.Series:
        """
        Calculate mean feature importance across all models.

        Args:
            feature_names:  feature names
            drop_null:      whether to drop unimportant features
            sort:           whether to sort the resulting series by the importance scores
        Returns:
            Series with feature importance
        """
        models = iter(self.models)
        try:
            result = pd.Series(next(models).get_feature_importance(), feature_names, dtype=float)
        except StopIteration:
            raise RuntimeError("You should train the ensemble before getting feature importance")
        for model in models:
            result += model.get_feature_importance()
        if drop_null:
            result = result[~np.isclose(result, 0)]
        if sort:
            result.sort_values(inplace=True)
        result *= 1 / len(self.models)
        return result
