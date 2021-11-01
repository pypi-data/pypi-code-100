"""Support scikit-learn using object mode of Numba """
import itertools
import numbers
import types as pytypes
import warnings
import numba
import numpy as np
import pandas as pd
import sklearn.cluster
import sklearn.ensemble
import sklearn.feature_extraction
import sklearn.linear_model
import sklearn.metrics
import sklearn.model_selection
import sklearn.naive_bayes
import sklearn.svm
import sklearn.utils
from mpi4py import MPI
from numba.core import types
from numba.extending import NativeValue, box, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from sklearn.exceptions import UndefinedMetricWarning
from sklearn.metrics import hinge_loss, log_loss, mean_squared_error
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing._data import _handle_zeros_in_scale as sklearn_handle_zeros_in_scale
from sklearn.utils.extmath import _safe_accumulator_op as sklearn_safe_accumulator_op
from sklearn.utils.validation import _check_sample_weight, column_or_1d
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import NumericIndexType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.libs.csr_matrix_ext import CSRMatrixType
from bodo.libs.distributed_api import Reduce_Type, create_subcomm_mpi4py, get_host_ranks, get_nodes_first_ranks, get_num_nodes
from bodo.utils.typing import BodoError, BodoWarning, check_unsupported_args, get_overload_const_int, get_overload_const_str, is_overload_constant_str, is_overload_false, is_overload_none, is_overload_true


def check_sklearn_version():
    if not bodo.compiler._is_sklearn_supported_version:
        wcz__pmbbu = f""" Bodo requires at most version {bodo.compiler._max_sklearn_ver_str} of scikit-learn.
             Installed version is {sklearn.__version__}.
"""
        raise BodoError(wcz__pmbbu)


def random_forest_model_fit(m, X, y):
    car__gbdbh = m.n_estimators
    eew__uxpto = MPI.Get_processor_name()
    ymls__kbvmy = get_host_ranks()
    kdki__nzcsf = len(ymls__kbvmy)
    fkzdl__dmifb = bodo.get_rank()
    m.n_estimators = bodo.libs.distributed_api.get_node_portion(car__gbdbh,
        kdki__nzcsf, fkzdl__dmifb)
    if fkzdl__dmifb == ymls__kbvmy[eew__uxpto][0]:
        m.n_jobs = len(ymls__kbvmy[eew__uxpto])
        if m.random_state is None:
            m.random_state = np.random.RandomState()
        from sklearn.utils import parallel_backend
        with parallel_backend('threading'):
            m.fit(X, y)
        m.n_jobs = 1
    with numba.objmode(first_rank_node='int32[:]'):
        first_rank_node = get_nodes_first_ranks()
    spr__houk = create_subcomm_mpi4py(first_rank_node)
    if spr__houk != MPI.COMM_NULL:
        imj__ehhkn = 10
        nxr__ktc = bodo.libs.distributed_api.get_node_portion(car__gbdbh,
            kdki__nzcsf, 0)
        efwmn__els = nxr__ktc // imj__ehhkn
        if nxr__ktc % imj__ehhkn != 0:
            efwmn__els += 1
        usoi__rzvjz = []
        for hyb__mhk in range(efwmn__els):
            dwltu__dpaut = spr__houk.gather(m.estimators_[hyb__mhk *
                imj__ehhkn:hyb__mhk * imj__ehhkn + imj__ehhkn])
            if fkzdl__dmifb == 0:
                usoi__rzvjz += list(itertools.chain.from_iterable(dwltu__dpaut)
                    )
        if fkzdl__dmifb == 0:
            m.estimators_ = usoi__rzvjz
    ctnln__rtz = MPI.COMM_WORLD
    if fkzdl__dmifb == 0:
        for hyb__mhk in range(0, car__gbdbh, 10):
            ctnln__rtz.bcast(m.estimators_[hyb__mhk:hyb__mhk + 10])
        if isinstance(m, sklearn.ensemble.RandomForestClassifier):
            ctnln__rtz.bcast(m.n_classes_)
            ctnln__rtz.bcast(m.classes_)
        ctnln__rtz.bcast(m.n_outputs_)
    else:
        escr__zspa = []
        for hyb__mhk in range(0, car__gbdbh, 10):
            escr__zspa += ctnln__rtz.bcast(None)
        if isinstance(m, sklearn.ensemble.RandomForestClassifier):
            m.n_classes_ = ctnln__rtz.bcast(None)
            m.classes_ = ctnln__rtz.bcast(None)
        m.n_outputs_ = ctnln__rtz.bcast(None)
        m.estimators_ = escr__zspa
    assert len(m.estimators_) == car__gbdbh
    m.n_estimators = car__gbdbh
    m.n_features_ = X.shape[1]


class BodoRandomForestClassifierType(types.Opaque):

    def __init__(self):
        super(BodoRandomForestClassifierType, self).__init__(name=
            'BodoRandomForestClassifierType')


random_forest_classifier_type = BodoRandomForestClassifierType()
types.random_forest_classifier_type = random_forest_classifier_type
register_model(BodoRandomForestClassifierType)(models.OpaqueModel)


@typeof_impl.register(sklearn.ensemble.RandomForestClassifier)
def typeof_random_forest_classifier(val, c):
    return random_forest_classifier_type


@box(BodoRandomForestClassifierType)
def box_random_forest_classifier(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoRandomForestClassifierType)
def unbox_random_forest_classifier(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.ensemble.RandomForestClassifier, no_unliteral=True)
def sklearn_ensemble_RandomForestClassifier_overload(n_estimators=100,
    criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf
    =1, min_weight_fraction_leaf=0.0, max_features='auto', max_leaf_nodes=
    None, min_impurity_decrease=0.0, min_impurity_split=None, bootstrap=
    True, oob_score=False, n_jobs=None, random_state=None, verbose=0,
    warm_start=False, class_weight=None, ccp_alpha=0.0, max_samples=None):
    check_sklearn_version()

    def _sklearn_ensemble_RandomForestClassifier_impl(n_estimators=100,
        criterion='gini', max_depth=None, min_samples_split=2,
        min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features=
        'auto', max_leaf_nodes=None, min_impurity_decrease=0.0,
        min_impurity_split=None, bootstrap=True, oob_score=False, n_jobs=
        None, random_state=None, verbose=0, warm_start=False, class_weight=
        None, ccp_alpha=0.0, max_samples=None):
        with numba.objmode(m='random_forest_classifier_type'):
            if random_state is not None and get_num_nodes() > 1:
                print(
                    'With multinode, fixed random_state seed values are ignored.\n'
                    )
                random_state = None
            m = sklearn.ensemble.RandomForestClassifier(n_estimators=
                n_estimators, criterion=criterion, max_depth=max_depth,
                min_samples_split=min_samples_split, min_samples_leaf=
                min_samples_leaf, min_weight_fraction_leaf=
                min_weight_fraction_leaf, max_features=max_features,
                max_leaf_nodes=max_leaf_nodes, min_impurity_decrease=
                min_impurity_decrease, min_impurity_split=
                min_impurity_split, bootstrap=bootstrap, oob_score=
                oob_score, n_jobs=1, random_state=random_state, verbose=
                verbose, warm_start=warm_start, class_weight=class_weight,
                ccp_alpha=ccp_alpha, max_samples=max_samples)
        return m
    return _sklearn_ensemble_RandomForestClassifier_impl


def parallel_predict_regression(m, X):
    check_sklearn_version()

    def _model_predict_impl(m, X):
        with numba.objmode(result='float64[:]'):
            m.n_jobs = 1
            if len(X) == 0:
                result = np.empty(0, dtype=np.float64)
            else:
                result = m.predict(X).astype(np.float64).flatten()
        return result
    return _model_predict_impl


def parallel_predict(m, X):
    check_sklearn_version()

    def _model_predict_impl(m, X):
        with numba.objmode(result='int64[:]'):
            m.n_jobs = 1
            if X.shape[0] == 0:
                result = np.empty(0, dtype=np.int64)
            else:
                result = m.predict(X).astype(np.int64).flatten()
        return result
    return _model_predict_impl


def parallel_score(m, X, y, sample_weight=None, _is_data_distributed=False):
    check_sklearn_version()

    def _model_score_impl(m, X, y, sample_weight=None, _is_data_distributed
        =False):
        with numba.objmode(result='float64[:]'):
            result = m.score(X, y, sample_weight=sample_weight)
            if _is_data_distributed:
                result = np.full(len(y), result)
            else:
                result = np.array([result])
        if _is_data_distributed:
            result = bodo.allgatherv(result)
        return result.mean()
    return _model_score_impl


@overload_method(BodoRandomForestClassifierType, 'predict', no_unliteral=True)
def overload_model_predict(m, X):
    check_sklearn_version()
    """Overload Random Forest Classifier predict. (Data parallelization)"""
    return parallel_predict(m, X)


@overload_method(BodoRandomForestClassifierType, 'score', no_unliteral=True)
def overload_model_score(m, X, y, sample_weight=None, _is_data_distributed=
    False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


def precision_recall_fscore_support_helper(MCM, average):

    def multilabel_confusion_matrix(y_true, y_pred, *, sample_weight=None,
        labels=None, samplewise=False):
        return MCM
    pni__bpf = sklearn.metrics._classification.multilabel_confusion_matrix
    result = -1.0
    try:
        sklearn.metrics._classification.multilabel_confusion_matrix = (
            multilabel_confusion_matrix)
        result = (sklearn.metrics._classification.
            precision_recall_fscore_support([], [], average=average))
    finally:
        sklearn.metrics._classification.multilabel_confusion_matrix = pni__bpf
    return result


@numba.njit
def precision_recall_fscore_parallel(y_true, y_pred, operation, average=
    'binary'):
    labels = bodo.libs.array_kernels.unique(y_true, parallel=True)
    labels = bodo.allgatherv(labels, False)
    labels = bodo.libs.array_kernels.sort(labels, ascending=True, inplace=False
        )
    cob__rxjzm = len(labels)
    uuez__kjlwv = np.zeros(cob__rxjzm, np.int64)
    var__sci = np.zeros(cob__rxjzm, np.int64)
    vhlws__hwkw = np.zeros(cob__rxjzm, np.int64)
    vlmm__arqh = (bodo.hiframes.pd_categorical_ext.
        get_label_dict_from_categories(labels))
    for hyb__mhk in range(len(y_true)):
        var__sci[vlmm__arqh[y_true[hyb__mhk]]] += 1
        if y_pred[hyb__mhk] not in vlmm__arqh:
            continue
        elly__wel = vlmm__arqh[y_pred[hyb__mhk]]
        vhlws__hwkw[elly__wel] += 1
        if y_true[hyb__mhk] == y_pred[hyb__mhk]:
            uuez__kjlwv[elly__wel] += 1
    uuez__kjlwv = bodo.libs.distributed_api.dist_reduce(uuez__kjlwv, np.
        int32(Reduce_Type.Sum.value))
    var__sci = bodo.libs.distributed_api.dist_reduce(var__sci, np.int32(
        Reduce_Type.Sum.value))
    vhlws__hwkw = bodo.libs.distributed_api.dist_reduce(vhlws__hwkw, np.
        int32(Reduce_Type.Sum.value))
    aqeva__ktzjg = vhlws__hwkw - uuez__kjlwv
    ojmc__twe = var__sci - uuez__kjlwv
    zek__wjqzz = uuez__kjlwv
    zfsxu__jzpdd = y_true.shape[0] - zek__wjqzz - aqeva__ktzjg - ojmc__twe
    with numba.objmode(result='float64[:]'):
        MCM = np.array([zfsxu__jzpdd, aqeva__ktzjg, ojmc__twe, zek__wjqzz]
            ).T.reshape(-1, 2, 2)
        if operation == 'precision':
            result = precision_recall_fscore_support_helper(MCM, average)[0]
        elif operation == 'recall':
            result = precision_recall_fscore_support_helper(MCM, average)[1]
        elif operation == 'f1':
            result = precision_recall_fscore_support_helper(MCM, average)[2]
        if average is not None:
            result = np.array([result])
    return result


@overload(sklearn.metrics.precision_score, no_unliteral=True)
def overload_precision_score(y_true, y_pred, average='binary',
    _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_none(average):
        if is_overload_false(_is_data_distributed):

            def _precision_score_impl(y_true, y_pred, average='binary',
                _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                with numba.objmode(score='float64[:]'):
                    score = sklearn.metrics.precision_score(y_true, y_pred,
                        average=average)
                return score
            return _precision_score_impl
        else:

            def _precision_score_impl(y_true, y_pred, average='binary',
                _is_data_distributed=False):
                return precision_recall_fscore_parallel(y_true, y_pred,
                    'precision', average=average)
            return _precision_score_impl
    elif is_overload_false(_is_data_distributed):

        def _precision_score_impl(y_true, y_pred, average='binary',
            _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            with numba.objmode(score='float64'):
                score = sklearn.metrics.precision_score(y_true, y_pred,
                    average=average)
            return score
        return _precision_score_impl
    else:

        def _precision_score_impl(y_true, y_pred, average='binary',
            _is_data_distributed=False):
            score = precision_recall_fscore_parallel(y_true, y_pred,
                'precision', average=average)
            return score[0]
        return _precision_score_impl


@overload(sklearn.metrics.recall_score, no_unliteral=True)
def overload_recall_score(y_true, y_pred, average='binary',
    _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_none(average):
        if is_overload_false(_is_data_distributed):

            def _recall_score_impl(y_true, y_pred, average='binary',
                _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                with numba.objmode(score='float64[:]'):
                    score = sklearn.metrics.recall_score(y_true, y_pred,
                        average=average)
                return score
            return _recall_score_impl
        else:

            def _recall_score_impl(y_true, y_pred, average='binary',
                _is_data_distributed=False):
                return precision_recall_fscore_parallel(y_true, y_pred,
                    'recall', average=average)
            return _recall_score_impl
    elif is_overload_false(_is_data_distributed):

        def _recall_score_impl(y_true, y_pred, average='binary',
            _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            with numba.objmode(score='float64'):
                score = sklearn.metrics.recall_score(y_true, y_pred,
                    average=average)
            return score
        return _recall_score_impl
    else:

        def _recall_score_impl(y_true, y_pred, average='binary',
            _is_data_distributed=False):
            score = precision_recall_fscore_parallel(y_true, y_pred,
                'recall', average=average)
            return score[0]
        return _recall_score_impl


@overload(sklearn.metrics.f1_score, no_unliteral=True)
def overload_f1_score(y_true, y_pred, average='binary',
    _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_none(average):
        if is_overload_false(_is_data_distributed):

            def _f1_score_impl(y_true, y_pred, average='binary',
                _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                with numba.objmode(score='float64[:]'):
                    score = sklearn.metrics.f1_score(y_true, y_pred,
                        average=average)
                return score
            return _f1_score_impl
        else:

            def _f1_score_impl(y_true, y_pred, average='binary',
                _is_data_distributed=False):
                return precision_recall_fscore_parallel(y_true, y_pred,
                    'f1', average=average)
            return _f1_score_impl
    elif is_overload_false(_is_data_distributed):

        def _f1_score_impl(y_true, y_pred, average='binary',
            _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            with numba.objmode(score='float64'):
                score = sklearn.metrics.f1_score(y_true, y_pred, average=
                    average)
            return score
        return _f1_score_impl
    else:

        def _f1_score_impl(y_true, y_pred, average='binary',
            _is_data_distributed=False):
            score = precision_recall_fscore_parallel(y_true, y_pred, 'f1',
                average=average)
            return score[0]
        return _f1_score_impl


def mse_mae_dist_helper(y_true, y_pred, sample_weight, multioutput, squared,
    metric):
    if metric == 'mse':
        ruvi__tpgz = sklearn.metrics.mean_squared_error(y_true, y_pred,
            sample_weight=sample_weight, multioutput='raw_values', squared=True
            )
    elif metric == 'mae':
        ruvi__tpgz = sklearn.metrics.mean_absolute_error(y_true, y_pred,
            sample_weight=sample_weight, multioutput='raw_values')
    else:
        raise RuntimeError(
            f"Unrecognized metric {metric}. Must be one of 'mae' and 'mse'")
    ctnln__rtz = MPI.COMM_WORLD
    tmx__jhwou = ctnln__rtz.Get_size()
    if sample_weight is not None:
        bblz__ijf = np.sum(sample_weight)
    else:
        bblz__ijf = np.float64(y_true.shape[0])
    gli__iuiin = np.zeros(tmx__jhwou, dtype=type(bblz__ijf))
    ctnln__rtz.Allgather(bblz__ijf, gli__iuiin)
    dtcei__wfsic = np.zeros((tmx__jhwou, *ruvi__tpgz.shape), dtype=
        ruvi__tpgz.dtype)
    ctnln__rtz.Allgather(ruvi__tpgz, dtcei__wfsic)
    tarb__bhoqb = np.average(dtcei__wfsic, weights=gli__iuiin, axis=0)
    if metric == 'mse' and not squared:
        tarb__bhoqb = np.sqrt(tarb__bhoqb)
    if isinstance(multioutput, str) and multioutput == 'raw_values':
        return tarb__bhoqb
    elif isinstance(multioutput, str) and multioutput == 'uniform_average':
        return np.average(tarb__bhoqb)
    else:
        return np.average(tarb__bhoqb, weights=multioutput)


@overload(sklearn.metrics.mean_squared_error, no_unliteral=True)
def overload_mean_squared_error(y_true, y_pred, sample_weight=None,
    multioutput='uniform_average', squared=True, _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_constant_str(multioutput) and get_overload_const_str(
        multioutput) == 'raw_values':
        if is_overload_none(sample_weight):

            def _mse_impl(y_true, y_pred, sample_weight=None, multioutput=
                'uniform_average', squared=True, _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                with numba.objmode(err='float64[:]'):
                    if _is_data_distributed:
                        err = mse_mae_dist_helper(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput, squared=squared, metric='mse')
                    else:
                        err = sklearn.metrics.mean_squared_error(y_true,
                            y_pred, sample_weight=sample_weight,
                            multioutput=multioutput, squared=squared)
                return err
            return _mse_impl
        else:

            def _mse_impl(y_true, y_pred, sample_weight=None, multioutput=
                'uniform_average', squared=True, _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                sample_weight = bodo.utils.conversion.coerce_to_array(
                    sample_weight)
                with numba.objmode(err='float64[:]'):
                    if _is_data_distributed:
                        err = mse_mae_dist_helper(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput, squared=squared, metric='mse')
                    else:
                        err = sklearn.metrics.mean_squared_error(y_true,
                            y_pred, sample_weight=sample_weight,
                            multioutput=multioutput, squared=squared)
                return err
            return _mse_impl
    elif is_overload_none(sample_weight):

        def _mse_impl(y_true, y_pred, sample_weight=None, multioutput=
            'uniform_average', squared=True, _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            with numba.objmode(err='float64'):
                if _is_data_distributed:
                    err = mse_mae_dist_helper(y_true, y_pred, sample_weight
                        =sample_weight, multioutput=multioutput, squared=
                        squared, metric='mse')
                else:
                    err = sklearn.metrics.mean_squared_error(y_true, y_pred,
                        sample_weight=sample_weight, multioutput=
                        multioutput, squared=squared)
            return err
        return _mse_impl
    else:

        def _mse_impl(y_true, y_pred, sample_weight=None, multioutput=
            'uniform_average', squared=True, _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            sample_weight = bodo.utils.conversion.coerce_to_array(sample_weight
                )
            with numba.objmode(err='float64'):
                if _is_data_distributed:
                    err = mse_mae_dist_helper(y_true, y_pred, sample_weight
                        =sample_weight, multioutput=multioutput, squared=
                        squared, metric='mse')
                else:
                    err = sklearn.metrics.mean_squared_error(y_true, y_pred,
                        sample_weight=sample_weight, multioutput=
                        multioutput, squared=squared)
            return err
        return _mse_impl


@overload(sklearn.metrics.mean_absolute_error, no_unliteral=True)
def overload_mean_absolute_error(y_true, y_pred, sample_weight=None,
    multioutput='uniform_average', _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_constant_str(multioutput) and get_overload_const_str(
        multioutput) == 'raw_values':
        if is_overload_none(sample_weight):

            def _mae_impl(y_true, y_pred, sample_weight=None, multioutput=
                'uniform_average', _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                with numba.objmode(err='float64[:]'):
                    if _is_data_distributed:
                        err = mse_mae_dist_helper(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput, squared=True, metric='mae')
                    else:
                        err = sklearn.metrics.mean_absolute_error(y_true,
                            y_pred, sample_weight=sample_weight,
                            multioutput=multioutput)
                return err
            return _mae_impl
        else:

            def _mae_impl(y_true, y_pred, sample_weight=None, multioutput=
                'uniform_average', _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                sample_weight = bodo.utils.conversion.coerce_to_array(
                    sample_weight)
                with numba.objmode(err='float64[:]'):
                    if _is_data_distributed:
                        err = mse_mae_dist_helper(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput, squared=True, metric='mae')
                    else:
                        err = sklearn.metrics.mean_absolute_error(y_true,
                            y_pred, sample_weight=sample_weight,
                            multioutput=multioutput)
                return err
            return _mae_impl
    elif is_overload_none(sample_weight):

        def _mae_impl(y_true, y_pred, sample_weight=None, multioutput=
            'uniform_average', _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            with numba.objmode(err='float64'):
                if _is_data_distributed:
                    err = mse_mae_dist_helper(y_true, y_pred, sample_weight
                        =sample_weight, multioutput=multioutput, squared=
                        True, metric='mae')
                else:
                    err = sklearn.metrics.mean_absolute_error(y_true,
                        y_pred, sample_weight=sample_weight, multioutput=
                        multioutput)
            return err
        return _mae_impl
    else:

        def _mae_impl(y_true, y_pred, sample_weight=None, multioutput=
            'uniform_average', _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            sample_weight = bodo.utils.conversion.coerce_to_array(sample_weight
                )
            with numba.objmode(err='float64'):
                if _is_data_distributed:
                    err = mse_mae_dist_helper(y_true, y_pred, sample_weight
                        =sample_weight, multioutput=multioutput, squared=
                        True, metric='mae')
                else:
                    err = sklearn.metrics.mean_absolute_error(y_true,
                        y_pred, sample_weight=sample_weight, multioutput=
                        multioutput)
            return err
        return _mae_impl


def accuracy_score_dist_helper(y_true, y_pred, normalize, sample_weight):
    score = sklearn.metrics.accuracy_score(y_true, y_pred, normalize=False,
        sample_weight=sample_weight)
    ctnln__rtz = MPI.COMM_WORLD
    score = ctnln__rtz.allreduce(score, op=MPI.SUM)
    if normalize:
        rkfgv__mkv = np.sum(sample_weight
            ) if sample_weight is not None else len(y_true)
        rkfgv__mkv = ctnln__rtz.allreduce(rkfgv__mkv, op=MPI.SUM)
        score = score / rkfgv__mkv
    return score


@overload(sklearn.metrics.accuracy_score, no_unliteral=True)
def overload_accuracy_score(y_true, y_pred, normalize=True, sample_weight=
    None, _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_false(_is_data_distributed):
        if is_overload_none(sample_weight):

            def _accuracy_score_impl(y_true, y_pred, normalize=True,
                sample_weight=None, _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                with numba.objmode(score='float64'):
                    score = sklearn.metrics.accuracy_score(y_true, y_pred,
                        normalize=normalize, sample_weight=sample_weight)
                return score
            return _accuracy_score_impl
        else:

            def _accuracy_score_impl(y_true, y_pred, normalize=True,
                sample_weight=None, _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                sample_weight = bodo.utils.conversion.coerce_to_array(
                    sample_weight)
                with numba.objmode(score='float64'):
                    score = sklearn.metrics.accuracy_score(y_true, y_pred,
                        normalize=normalize, sample_weight=sample_weight)
                return score
            return _accuracy_score_impl
    elif is_overload_none(sample_weight):

        def _accuracy_score_impl(y_true, y_pred, normalize=True,
            sample_weight=None, _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            with numba.objmode(score='float64'):
                score = accuracy_score_dist_helper(y_true, y_pred,
                    normalize=normalize, sample_weight=sample_weight)
            return score
        return _accuracy_score_impl
    else:

        def _accuracy_score_impl(y_true, y_pred, normalize=True,
            sample_weight=None, _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            sample_weight = bodo.utils.conversion.coerce_to_array(sample_weight
                )
            with numba.objmode(score='float64'):
                score = accuracy_score_dist_helper(y_true, y_pred,
                    normalize=normalize, sample_weight=sample_weight)
            return score
        return _accuracy_score_impl


def check_consistent_length_parallel(*arrays):
    ctnln__rtz = MPI.COMM_WORLD
    kjafy__yzlp = True
    gjkqi__itu = [len(ocdl__bgkr) for ocdl__bgkr in arrays if ocdl__bgkr is not
        None]
    if len(np.unique(gjkqi__itu)) > 1:
        kjafy__yzlp = False
    kjafy__yzlp = ctnln__rtz.allreduce(kjafy__yzlp, op=MPI.LAND)
    return kjafy__yzlp


def r2_score_dist_helper(y_true, y_pred, sample_weight, multioutput):
    ctnln__rtz = MPI.COMM_WORLD
    if y_true.ndim == 1:
        y_true = y_true.reshape((-1, 1))
    if y_pred.ndim == 1:
        y_pred = y_pred.reshape((-1, 1))
    if not check_consistent_length_parallel(y_true, y_pred, sample_weight):
        raise ValueError(
            'y_true, y_pred and sample_weight (if not None) have inconsistent number of samples'
            )
    vklt__yjmm = y_true.shape[0]
    dca__bydsx = ctnln__rtz.allreduce(vklt__yjmm, op=MPI.SUM)
    if dca__bydsx < 2:
        warnings.warn(
            'R^2 score is not well-defined with less than two samples.',
            UndefinedMetricWarning)
        return np.array([float('nan')])
    if sample_weight is not None:
        sample_weight = column_or_1d(sample_weight)
        vun__bcf = sample_weight[:, np.newaxis]
    else:
        sample_weight = np.float64(y_true.shape[0])
        vun__bcf = 1.0
    cbieh__ctdc = (vun__bcf * (y_true - y_pred) ** 2).sum(axis=0, dtype=np.
        float64)
    oce__cvgc = np.zeros(cbieh__ctdc.shape, dtype=cbieh__ctdc.dtype)
    ctnln__rtz.Allreduce(cbieh__ctdc, oce__cvgc, op=MPI.SUM)
    mvmxm__hzmr = np.nansum(y_true * vun__bcf, axis=0, dtype=np.float64)
    fehnc__nnnv = np.zeros_like(mvmxm__hzmr)
    ctnln__rtz.Allreduce(mvmxm__hzmr, fehnc__nnnv, op=MPI.SUM)
    ffkpz__flyo = np.nansum(sample_weight, dtype=np.float64)
    jczs__wdlnf = ctnln__rtz.allreduce(ffkpz__flyo, op=MPI.SUM)
    ofzv__xnvpx = fehnc__nnnv / jczs__wdlnf
    cpbd__dglo = (vun__bcf * (y_true - ofzv__xnvpx) ** 2).sum(axis=0, dtype
        =np.float64)
    htq__yck = np.zeros(cpbd__dglo.shape, dtype=cpbd__dglo.dtype)
    ctnln__rtz.Allreduce(cpbd__dglo, htq__yck, op=MPI.SUM)
    tkfr__bqs = htq__yck != 0
    ckx__mwzmc = oce__cvgc != 0
    xcu__fudpb = tkfr__bqs & ckx__mwzmc
    zic__rqsi = np.ones([y_true.shape[1] if len(y_true.shape) > 1 else 1])
    zic__rqsi[xcu__fudpb] = 1 - oce__cvgc[xcu__fudpb] / htq__yck[xcu__fudpb]
    zic__rqsi[ckx__mwzmc & ~tkfr__bqs] = 0.0
    if isinstance(multioutput, str):
        if multioutput == 'raw_values':
            return zic__rqsi
        elif multioutput == 'uniform_average':
            qngk__jda = None
        elif multioutput == 'variance_weighted':
            qngk__jda = htq__yck
            if not np.any(tkfr__bqs):
                if not np.any(ckx__mwzmc):
                    return np.array([1.0])
                else:
                    return np.array([0.0])
    else:
        qngk__jda = multioutput
    return np.array([np.average(zic__rqsi, weights=qngk__jda)])


@overload(sklearn.metrics.r2_score, no_unliteral=True)
def overload_r2_score(y_true, y_pred, sample_weight=None, multioutput=
    'uniform_average', _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_constant_str(multioutput) and get_overload_const_str(
        multioutput) not in ['raw_values', 'uniform_average',
        'variance_weighted']:
        raise BodoError(
            f"Unsupported argument {get_overload_const_str(multioutput)} specified for 'multioutput'"
            )
    if is_overload_constant_str(multioutput) and get_overload_const_str(
        multioutput) == 'raw_values':
        if is_overload_none(sample_weight):

            def _r2_score_impl(y_true, y_pred, sample_weight=None,
                multioutput='uniform_average', _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                with numba.objmode(score='float64[:]'):
                    if _is_data_distributed:
                        score = r2_score_dist_helper(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput)
                    else:
                        score = sklearn.metrics.r2_score(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput)
                return score
            return _r2_score_impl
        else:

            def _r2_score_impl(y_true, y_pred, sample_weight=None,
                multioutput='uniform_average', _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                sample_weight = bodo.utils.conversion.coerce_to_array(
                    sample_weight)
                with numba.objmode(score='float64[:]'):
                    if _is_data_distributed:
                        score = r2_score_dist_helper(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput)
                    else:
                        score = sklearn.metrics.r2_score(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput)
                return score
            return _r2_score_impl
    elif is_overload_none(sample_weight):

        def _r2_score_impl(y_true, y_pred, sample_weight=None, multioutput=
            'uniform_average', _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            with numba.objmode(score='float64'):
                if _is_data_distributed:
                    score = r2_score_dist_helper(y_true, y_pred,
                        sample_weight=sample_weight, multioutput=multioutput)
                    score = score[0]
                else:
                    score = sklearn.metrics.r2_score(y_true, y_pred,
                        sample_weight=sample_weight, multioutput=multioutput)
            return score
        return _r2_score_impl
    else:

        def _r2_score_impl(y_true, y_pred, sample_weight=None, multioutput=
            'uniform_average', _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            sample_weight = bodo.utils.conversion.coerce_to_array(sample_weight
                )
            with numba.objmode(score='float64'):
                if _is_data_distributed:
                    score = r2_score_dist_helper(y_true, y_pred,
                        sample_weight=sample_weight, multioutput=multioutput)
                    score = score[0]
                else:
                    score = sklearn.metrics.r2_score(y_true, y_pred,
                        sample_weight=sample_weight, multioutput=multioutput)
            return score
        return _r2_score_impl


class BodoSGDRegressorType(types.Opaque):

    def __init__(self):
        super(BodoSGDRegressorType, self).__init__(name='BodoSGDRegressorType')


sgd_regressor_type = BodoSGDRegressorType()
types.sgd_regressor_type = sgd_regressor_type
register_model(BodoSGDRegressorType)(models.OpaqueModel)


@typeof_impl.register(sklearn.linear_model.SGDRegressor)
def typeof_sgd_regressor(val, c):
    return sgd_regressor_type


@box(BodoSGDRegressorType)
def box_sgd_regressor(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoSGDRegressorType)
def unbox_sgd_regressor(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.linear_model.SGDRegressor, no_unliteral=True)
def sklearn_linear_model_SGDRegressor_overload(loss='squared_loss', penalty
    ='l2', alpha=0.0001, l1_ratio=0.15, fit_intercept=True, max_iter=1000,
    tol=0.001, shuffle=True, verbose=0, epsilon=0.1, random_state=None,
    learning_rate='invscaling', eta0=0.01, power_t=0.25, early_stopping=
    False, validation_fraction=0.1, n_iter_no_change=5, warm_start=False,
    average=False):
    check_sklearn_version()

    def _sklearn_linear_model_SGDRegressor_impl(loss='squared_loss',
        penalty='l2', alpha=0.0001, l1_ratio=0.15, fit_intercept=True,
        max_iter=1000, tol=0.001, shuffle=True, verbose=0, epsilon=0.1,
        random_state=None, learning_rate='invscaling', eta0=0.01, power_t=
        0.25, early_stopping=False, validation_fraction=0.1,
        n_iter_no_change=5, warm_start=False, average=False):
        with numba.objmode(m='sgd_regressor_type'):
            m = sklearn.linear_model.SGDRegressor(loss=loss, penalty=
                penalty, alpha=alpha, l1_ratio=l1_ratio, fit_intercept=
                fit_intercept, max_iter=max_iter, tol=tol, shuffle=shuffle,
                verbose=verbose, epsilon=epsilon, random_state=random_state,
                learning_rate=learning_rate, eta0=eta0, power_t=power_t,
                early_stopping=early_stopping, validation_fraction=
                validation_fraction, n_iter_no_change=n_iter_no_change,
                warm_start=warm_start, average=average)
        return m
    return _sklearn_linear_model_SGDRegressor_impl


@overload_method(BodoSGDRegressorType, 'fit', no_unliteral=True)
def overload_sgdr_model_fit(m, X, y, _is_data_distributed=False):
    check_sklearn_version()

    def _model_sgdr_fit_impl(m, X, y, _is_data_distributed=False):
        with numba.objmode(m='sgd_regressor_type'):
            m = fit_sgd(m, X, y, _is_data_distributed)
        bodo.barrier()
        return m
    return _model_sgdr_fit_impl


@overload_method(BodoSGDRegressorType, 'predict', no_unliteral=True)
def overload_sgdr_model_predict(m, X):
    return parallel_predict_regression(m, X)


@overload_method(BodoSGDRegressorType, 'score', no_unliteral=True)
def overload_sgdr_model_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


class BodoSGDClassifierType(types.Opaque):

    def __init__(self):
        super(BodoSGDClassifierType, self).__init__(name=
            'BodoSGDClassifierType')


sgd_classifier_type = BodoSGDClassifierType()
types.sgd_classifier_type = sgd_classifier_type
register_model(BodoSGDClassifierType)(models.OpaqueModel)


@typeof_impl.register(sklearn.linear_model.SGDClassifier)
def typeof_sgd_classifier(val, c):
    return sgd_classifier_type


@box(BodoSGDClassifierType)
def box_sgd_classifier(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoSGDClassifierType)
def unbox_sgd_classifier(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.linear_model.SGDClassifier, no_unliteral=True)
def sklearn_linear_model_SGDClassifier_overload(loss='hinge', penalty='l2',
    alpha=0.0001, l1_ratio=0.15, fit_intercept=True, max_iter=1000, tol=
    0.001, shuffle=True, verbose=0, epsilon=0.1, n_jobs=None, random_state=
    None, learning_rate='optimal', eta0=0.0, power_t=0.5, early_stopping=
    False, validation_fraction=0.1, n_iter_no_change=5, class_weight=None,
    warm_start=False, average=False):
    check_sklearn_version()

    def _sklearn_linear_model_SGDClassifier_impl(loss='hinge', penalty='l2',
        alpha=0.0001, l1_ratio=0.15, fit_intercept=True, max_iter=1000, tol
        =0.001, shuffle=True, verbose=0, epsilon=0.1, n_jobs=None,
        random_state=None, learning_rate='optimal', eta0=0.0, power_t=0.5,
        early_stopping=False, validation_fraction=0.1, n_iter_no_change=5,
        class_weight=None, warm_start=False, average=False):
        with numba.objmode(m='sgd_classifier_type'):
            m = sklearn.linear_model.SGDClassifier(loss=loss, penalty=
                penalty, alpha=alpha, l1_ratio=l1_ratio, fit_intercept=
                fit_intercept, max_iter=max_iter, tol=tol, shuffle=shuffle,
                verbose=verbose, epsilon=epsilon, n_jobs=n_jobs,
                random_state=random_state, learning_rate=learning_rate,
                eta0=eta0, power_t=power_t, early_stopping=early_stopping,
                validation_fraction=validation_fraction, n_iter_no_change=
                n_iter_no_change, class_weight=class_weight, warm_start=
                warm_start, average=average)
        return m
    return _sklearn_linear_model_SGDClassifier_impl


def fit_sgd(m, X, y, y_classes=None, _is_data_distributed=False):
    ctnln__rtz = MPI.COMM_WORLD
    xvx__hrhav = ctnln__rtz.allreduce(len(X), op=MPI.SUM)
    bwkdk__dkezq = len(X) / xvx__hrhav
    znkj__kjxm = ctnln__rtz.Get_size()
    m.n_jobs = 1
    m.early_stopping = False
    jqiq__jca = np.inf
    cywct__iebx = 0
    if m.loss == 'hinge':
        xiz__ykoxg = hinge_loss
    elif m.loss == 'log':
        xiz__ykoxg = log_loss
    elif m.loss == 'squared_loss':
        xiz__ykoxg = mean_squared_error
    else:
        raise ValueError('loss {} not supported'.format(m.loss))
    nvwj__lhm = False
    if isinstance(m, sklearn.linear_model.SGDRegressor):
        nvwj__lhm = True
    for fjtg__wmkxy in range(m.max_iter):
        if nvwj__lhm:
            m.partial_fit(X, y)
        else:
            m.partial_fit(X, y, classes=y_classes)
        m.coef_ = m.coef_ * bwkdk__dkezq
        m.coef_ = ctnln__rtz.allreduce(m.coef_, op=MPI.SUM)
        m.intercept_ = m.intercept_ * bwkdk__dkezq
        m.intercept_ = ctnln__rtz.allreduce(m.intercept_, op=MPI.SUM)
        if nvwj__lhm:
            y_pred = m.predict(X)
            pph__tbau = xiz__ykoxg(y, y_pred)
        else:
            y_pred = m.decision_function(X)
            pph__tbau = xiz__ykoxg(y, y_pred, labels=y_classes)
        oetcd__wfpug = ctnln__rtz.allreduce(pph__tbau, op=MPI.SUM)
        pph__tbau = oetcd__wfpug / znkj__kjxm
        if m.tol > np.NINF and pph__tbau > jqiq__jca - m.tol * xvx__hrhav:
            cywct__iebx += 1
        else:
            cywct__iebx = 0
        if pph__tbau < jqiq__jca:
            jqiq__jca = pph__tbau
        if cywct__iebx >= m.n_iter_no_change:
            break
    return m


@overload_method(BodoSGDClassifierType, 'fit', no_unliteral=True)
def overload_sgdc_model_fit(m, X, y, _is_data_distributed=False):
    check_sklearn_version()
    """
    Provide implementations for the fit function.
    In case input is replicated, we simply call sklearn,
    else we use partial_fit on each rank then use we re-compute the attributes using MPI operations.
    """
    if is_overload_true(_is_data_distributed):

        def _model_sgdc_fit_impl(m, X, y, _is_data_distributed=False):
            y_classes = bodo.libs.array_kernels.unique(y)
            y_classes = bodo.allgatherv(y_classes, False)
            with numba.objmode(m='sgd_classifier_type'):
                m = fit_sgd(m, X, y, y_classes, _is_data_distributed)
            return m
        return _model_sgdc_fit_impl
    else:

        def _model_sgdc_fit_impl(m, X, y, _is_data_distributed=False):
            with numba.objmode(m='sgd_classifier_type'):
                m = m.fit(X, y)
            return m
        return _model_sgdc_fit_impl


@overload_method(BodoSGDClassifierType, 'predict', no_unliteral=True)
def overload_sgdc_model_predict(m, X):
    return parallel_predict(m, X)


@overload_method(BodoSGDClassifierType, 'score', no_unliteral=True)
def overload_sgdc_model_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


@overload_attribute(BodoSGDClassifierType, 'coef_')
def get_sgdc_coef(m):

    def impl(m):
        with numba.objmode(result='float64[:,:]'):
            result = m.coef_
        return result
    return impl


class BodoKMeansClusteringType(types.Opaque):

    def __init__(self):
        super(BodoKMeansClusteringType, self).__init__(name=
            'BodoKMeansClusteringType')


kmeans_clustering_type = BodoKMeansClusteringType()
types.kmeans_clustering_type = kmeans_clustering_type
register_model(BodoKMeansClusteringType)(models.OpaqueModel)


@typeof_impl.register(sklearn.cluster.KMeans)
def typeof_kmeans_clustering(val, c):
    return kmeans_clustering_type


@box(BodoKMeansClusteringType)
def box_kmeans_clustering(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoKMeansClusteringType)
def unbox_kmeans_clustering(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.cluster.KMeans, no_unliteral=True)
def sklearn_cluster_kmeans_overload(n_clusters=8, init='k-means++', n_init=
    10, max_iter=300, tol=0.0001, precompute_distances='deprecated',
    verbose=0, random_state=None, copy_x=True, n_jobs='deprecated',
    algorithm='auto'):
    check_sklearn_version()

    def _sklearn_cluster_kmeans_impl(n_clusters=8, init='k-means++', n_init
        =10, max_iter=300, tol=0.0001, precompute_distances='deprecated',
        verbose=0, random_state=None, copy_x=True, n_jobs='deprecated',
        algorithm='auto'):
        with numba.objmode(m='kmeans_clustering_type'):
            m = sklearn.cluster.KMeans(n_clusters=n_clusters, init=init,
                n_init=n_init, max_iter=max_iter, tol=tol,
                precompute_distances=precompute_distances, verbose=verbose,
                random_state=random_state, copy_x=copy_x, n_jobs=n_jobs,
                algorithm=algorithm)
        return m
    return _sklearn_cluster_kmeans_impl


def kmeans_fit_helper(m, len_X, all_X, all_sample_weight, _is_data_distributed
    ):
    ctnln__rtz = MPI.COMM_WORLD
    fkzdl__dmifb = ctnln__rtz.Get_rank()
    eew__uxpto = MPI.Get_processor_name()
    ymls__kbvmy = get_host_ranks()
    qrk__ybu = m.n_jobs if hasattr(m, 'n_jobs') else None
    pvas__aqnfo = m._n_threads if hasattr(m, '_n_threads') else None
    m.n_jobs = len(ymls__kbvmy[eew__uxpto])
    m._n_threads = len(ymls__kbvmy[eew__uxpto])
    if fkzdl__dmifb == 0:
        m.fit(X=all_X, y=None, sample_weight=all_sample_weight)
    if fkzdl__dmifb == 0:
        ctnln__rtz.bcast(m.cluster_centers_)
        ctnln__rtz.bcast(m.inertia_)
        ctnln__rtz.bcast(m.n_iter_)
    else:
        m.cluster_centers_ = ctnln__rtz.bcast(None)
        m.inertia_ = ctnln__rtz.bcast(None)
        m.n_iter_ = ctnln__rtz.bcast(None)
    if _is_data_distributed:
        lqh__mru = ctnln__rtz.allgather(len_X)
        if fkzdl__dmifb == 0:
            pdov__uji = np.empty(len(lqh__mru) + 1, dtype=int)
            np.cumsum(lqh__mru, out=pdov__uji[1:])
            pdov__uji[0] = 0
            qwc__ohdu = [m.labels_[pdov__uji[chjdp__rlk]:pdov__uji[
                chjdp__rlk + 1]] for chjdp__rlk in range(len(lqh__mru))]
            rwsyy__vyc = ctnln__rtz.scatter(qwc__ohdu)
        else:
            rwsyy__vyc = ctnln__rtz.scatter(None)
        m.labels_ = rwsyy__vyc
    elif fkzdl__dmifb == 0:
        ctnln__rtz.bcast(m.labels_)
    else:
        m.labels_ = ctnln__rtz.bcast(None)
    m.n_jobs = qrk__ybu
    m._n_threads = pvas__aqnfo
    return m


@overload_method(BodoKMeansClusteringType, 'fit', no_unliteral=True)
def overload_kmeans_clustering_fit(m, X, y=None, sample_weight=None,
    _is_data_distributed=False):

    def _cluster_kmeans_fit_impl(m, X, y=None, sample_weight=None,
        _is_data_distributed=False):
        if _is_data_distributed:
            all_X = bodo.gatherv(X)
            if sample_weight is not None:
                all_sample_weight = bodo.gatherv(sample_weight)
            else:
                all_sample_weight = None
        else:
            all_X = X
            all_sample_weight = sample_weight
        with numba.objmode(m='kmeans_clustering_type'):
            m = kmeans_fit_helper(m, len(X), all_X, all_sample_weight,
                _is_data_distributed)
        return m
    return _cluster_kmeans_fit_impl


def kmeans_predict_helper(m, X, sample_weight):
    pvas__aqnfo = m._n_threads if hasattr(m, '_n_threads') else None
    qrk__ybu = m.n_jobs if hasattr(m, 'n_jobs') else None
    m._n_threads = 1
    m.n_jobs = 1
    if len(X) == 0:
        preds = np.empty(0, dtype=np.int64)
    else:
        preds = m.predict(X, sample_weight).astype(np.int64).flatten()
    m._n_threads = pvas__aqnfo
    m.n_jobs = qrk__ybu
    return preds


@overload_method(BodoKMeansClusteringType, 'predict', no_unliteral=True)
def overload_kmeans_clustering_predict(m, X, sample_weight=None):

    def _cluster_kmeans_predict(m, X, sample_weight=None):
        with numba.objmode(preds='int64[:]'):
            preds = kmeans_predict_helper(m, X, sample_weight)
        return preds
    return _cluster_kmeans_predict


@overload_method(BodoKMeansClusteringType, 'score', no_unliteral=True)
def overload_kmeans_clustering_score(m, X, y=None, sample_weight=None,
    _is_data_distributed=False):

    def _cluster_kmeans_score(m, X, y=None, sample_weight=None,
        _is_data_distributed=False):
        with numba.objmode(result='float64'):
            pvas__aqnfo = m._n_threads if hasattr(m, '_n_threads') else None
            qrk__ybu = m.n_jobs if hasattr(m, 'n_jobs') else None
            m._n_threads = 1
            m.n_jobs = 1
            if len(X) == 0:
                result = 0
            else:
                result = m.score(X, y=y, sample_weight=sample_weight)
            if _is_data_distributed:
                ctnln__rtz = MPI.COMM_WORLD
                result = ctnln__rtz.allreduce(result, op=MPI.SUM)
            m._n_threads = pvas__aqnfo
            m.n_jobs = qrk__ybu
        return result
    return _cluster_kmeans_score


@overload_method(BodoKMeansClusteringType, 'transform', no_unliteral=True)
def overload_kmeans_clustering_transform(m, X):

    def _cluster_kmeans_transform(m, X):
        with numba.objmode(X_new='float64[:,:]'):
            pvas__aqnfo = m._n_threads if hasattr(m, '_n_threads') else None
            qrk__ybu = m.n_jobs if hasattr(m, 'n_jobs') else None
            m._n_threads = 1
            m.n_jobs = 1
            if len(X) == 0:
                X_new = np.empty((0, m.n_clusters), dtype=np.int64)
            else:
                X_new = m.transform(X).astype(np.float64)
            m._n_threads = pvas__aqnfo
            m.n_jobs = qrk__ybu
        return X_new
    return _cluster_kmeans_transform


class BodoMultinomialNBType(types.Opaque):

    def __init__(self):
        super(BodoMultinomialNBType, self).__init__(name=
            'BodoMultinomialNBType')


multinomial_nb_type = BodoMultinomialNBType()
types.multinomial_nb_type = multinomial_nb_type
register_model(BodoMultinomialNBType)(models.OpaqueModel)


@typeof_impl.register(sklearn.naive_bayes.MultinomialNB)
def typeof_multinomial_nb(val, c):
    return multinomial_nb_type


@box(BodoMultinomialNBType)
def box_multinomial_nb(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoMultinomialNBType)
def unbox_multinomial_nb(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.naive_bayes.MultinomialNB, no_unliteral=True)
def sklearn_naive_bayes_multinomialnb_overload(alpha=1.0, fit_prior=True,
    class_prior=None):
    check_sklearn_version()

    def _sklearn_naive_bayes_multinomialnb_impl(alpha=1.0, fit_prior=True,
        class_prior=None):
        with numba.objmode(m='multinomial_nb_type'):
            m = sklearn.naive_bayes.MultinomialNB(alpha=alpha, fit_prior=
                fit_prior, class_prior=class_prior)
        return m
    return _sklearn_naive_bayes_multinomialnb_impl


@overload_method(BodoMultinomialNBType, 'fit', no_unliteral=True)
def overload_multinomial_nb_model_fit(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    if is_overload_false(_is_data_distributed):

        def _naive_bayes_multinomial_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            with numba.objmode():
                m.fit(X, y, sample_weight)
            return m
        return _naive_bayes_multinomial_impl
    else:
        nzxqb__mnjn = 'def _model_multinomial_nb_fit_impl(\n'
        nzxqb__mnjn += (
            '    m, X, y, sample_weight=None, _is_data_distributed=False\n')
        nzxqb__mnjn += '):  # pragma: no cover\n'
        nzxqb__mnjn += '    y = bodo.utils.conversion.coerce_to_ndarray(y)\n'
        if isinstance(X, DataFrameType):
            nzxqb__mnjn += '    X = X.to_numpy()\n'
        else:
            nzxqb__mnjn += (
                '    X = bodo.utils.conversion.coerce_to_ndarray(X)\n')
        nzxqb__mnjn += '    my_rank = bodo.get_rank()\n'
        nzxqb__mnjn += '    nranks = bodo.get_size()\n'
        nzxqb__mnjn += '    total_cols = X.shape[1]\n'
        nzxqb__mnjn += '    for i in range(nranks):\n'
        nzxqb__mnjn += """        start = bodo.libs.distributed_api.get_start(total_cols, nranks, i)
"""
        nzxqb__mnjn += (
            '        end = bodo.libs.distributed_api.get_end(total_cols, nranks, i)\n'
            )
        nzxqb__mnjn += '        if i == my_rank:\n'
        nzxqb__mnjn += (
            '            X_train = bodo.gatherv(X[:, start:end:1], root=i)\n')
        nzxqb__mnjn += '        else:\n'
        nzxqb__mnjn += '            bodo.gatherv(X[:, start:end:1], root=i)\n'
        nzxqb__mnjn += '    y_train = bodo.allgatherv(y, False)\n'
        nzxqb__mnjn += '    with numba.objmode(m="multinomial_nb_type"):\n'
        nzxqb__mnjn += '        m = fit_multinomial_nb(\n'
        nzxqb__mnjn += """            m, X_train, y_train, sample_weight, total_cols, _is_data_distributed
"""
        nzxqb__mnjn += '        )\n'
        nzxqb__mnjn += '    bodo.barrier()\n'
        nzxqb__mnjn += '    return m\n'
        dqmyz__nzoms = {}
        exec(nzxqb__mnjn, globals(), dqmyz__nzoms)
        pffxw__welk = dqmyz__nzoms['_model_multinomial_nb_fit_impl']
        return pffxw__welk


def fit_multinomial_nb(m, X_train, y_train, sample_weight=None, total_cols=
    0, _is_data_distributed=False):
    m._check_X_y(X_train, y_train)
    fjtg__wmkxy, n_features = X_train.shape
    m.n_features_ = n_features
    ovd__nkir = LabelBinarizer()
    xkmez__zkrfg = ovd__nkir.fit_transform(y_train)
    m.classes_ = ovd__nkir.classes_
    if xkmez__zkrfg.shape[1] == 1:
        xkmez__zkrfg = np.concatenate((1 - xkmez__zkrfg, xkmez__zkrfg), axis=1)
    if sample_weight is not None:
        xkmez__zkrfg = xkmez__zkrfg.astype(np.float64, copy=False)
        sample_weight = _check_sample_weight(sample_weight, X_train)
        sample_weight = np.atleast_2d(sample_weight)
        xkmez__zkrfg *= sample_weight.T
    class_prior = m.class_prior
    qrbq__bofn = xkmez__zkrfg.shape[1]
    m._init_counters(qrbq__bofn, n_features)
    m._count(X_train.astype('float64'), xkmez__zkrfg)
    alpha = m._check_alpha()
    m._update_class_log_prior(class_prior=class_prior)
    wfn__spee = m.feature_count_ + alpha
    wzlmu__uisab = wfn__spee.sum(axis=1)
    ctnln__rtz = MPI.COMM_WORLD
    znkj__kjxm = ctnln__rtz.Get_size()
    harg__mosnz = np.zeros(qrbq__bofn)
    ctnln__rtz.Allreduce(wzlmu__uisab, harg__mosnz, op=MPI.SUM)
    icqrd__pgpi = np.log(wfn__spee) - np.log(harg__mosnz.reshape(-1, 1))
    agl__lmbc = icqrd__pgpi.T.reshape(n_features * qrbq__bofn)
    znm__fzra = np.ones(znkj__kjxm) * (total_cols // znkj__kjxm)
    neu__hcgxc = total_cols % znkj__kjxm
    for qxcti__pfw in range(neu__hcgxc):
        znm__fzra[qxcti__pfw] += 1
    znm__fzra *= qrbq__bofn
    awkyz__uzjuc = np.zeros(znkj__kjxm, dtype=np.int32)
    awkyz__uzjuc[1:] = np.cumsum(znm__fzra)[:-1]
    zmp__cqjq = np.zeros((total_cols, qrbq__bofn), dtype=np.float64)
    ctnln__rtz.Allgatherv(agl__lmbc, [zmp__cqjq, znm__fzra, awkyz__uzjuc,
        MPI.DOUBLE_PRECISION])
    m.feature_log_prob_ = zmp__cqjq.T
    m.n_features_ = m.feature_log_prob_.shape[1]
    return m


@overload_method(BodoMultinomialNBType, 'predict', no_unliteral=True)
def overload_multinomial_nb_model_predict(m, X):
    return parallel_predict(m, X)


@overload_method(BodoMultinomialNBType, 'score', no_unliteral=True)
def overload_multinomial_nb_model_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


class BodoLogisticRegressionType(types.Opaque):

    def __init__(self):
        super(BodoLogisticRegressionType, self).__init__(name=
            'BodoLogisticRegressionType')


logistic_regression_type = BodoLogisticRegressionType()
types.logistic_regression_type = logistic_regression_type
register_model(BodoLogisticRegressionType)(models.OpaqueModel)


@typeof_impl.register(sklearn.linear_model.LogisticRegression)
def typeof_logistic_regression(val, c):
    return logistic_regression_type


@box(BodoLogisticRegressionType)
def box_logistic_regression(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoLogisticRegressionType)
def unbox_logistic_regression(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.linear_model.LogisticRegression, no_unliteral=True)
def sklearn_linear_model_logistic_regression_overload(penalty='l2', dual=
    False, tol=0.0001, C=1.0, fit_intercept=True, intercept_scaling=1,
    class_weight=None, random_state=None, solver='lbfgs', max_iter=100,
    multi_class='auto', verbose=0, warm_start=False, n_jobs=None, l1_ratio=None
    ):
    check_sklearn_version()

    def _sklearn_linear_model_logistic_regression_impl(penalty='l2', dual=
        False, tol=0.0001, C=1.0, fit_intercept=True, intercept_scaling=1,
        class_weight=None, random_state=None, solver='lbfgs', max_iter=100,
        multi_class='auto', verbose=0, warm_start=False, n_jobs=None,
        l1_ratio=None):
        with numba.objmode(m='logistic_regression_type'):
            m = sklearn.linear_model.LogisticRegression(penalty=penalty,
                dual=dual, tol=tol, C=C, fit_intercept=fit_intercept,
                intercept_scaling=intercept_scaling, class_weight=
                class_weight, random_state=random_state, solver=solver,
                max_iter=max_iter, multi_class=multi_class, verbose=verbose,
                warm_start=warm_start, n_jobs=n_jobs, l1_ratio=l1_ratio)
        return m
    return _sklearn_linear_model_logistic_regression_impl


@register_jitable
def _raise_SGD_warning(sgd_name):
    with numba.objmode:
        warnings.warn(
            f'Data is distributed so Bodo will fit model with SGD solver optimization ({sgd_name})'
            , BodoWarning)


@overload_method(BodoLogisticRegressionType, 'fit', no_unliteral=True)
def overload_logistic_regression_fit(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    if is_overload_false(_is_data_distributed):

        def _logistic_regression_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            with numba.objmode():
                m.fit(X, y, sample_weight)
            return m
        return _logistic_regression_fit_impl
    else:

        def _sgdc_logistic_regression_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            if bodo.get_rank() == 0:
                _raise_SGD_warning('SGDClassifier')
            with numba.objmode(clf='sgd_classifier_type'):
                if m.l1_ratio is None:
                    l1_ratio = 0.15
                else:
                    l1_ratio = m.l1_ratio
                clf = sklearn.linear_model.SGDClassifier(loss='log',
                    penalty=m.penalty, tol=m.tol, fit_intercept=m.
                    fit_intercept, class_weight=m.class_weight,
                    random_state=m.random_state, max_iter=m.max_iter,
                    verbose=m.verbose, warm_start=m.warm_start, n_jobs=m.
                    n_jobs, l1_ratio=l1_ratio)
            clf.fit(X, y, _is_data_distributed=True)
            with numba.objmode():
                m.coef_ = clf.coef_
                m.intercept_ = clf.intercept_
                m.n_iter_ = clf.n_iter_
                m.classes_ = clf.classes_
            return m
        return _sgdc_logistic_regression_fit_impl


@overload_method(BodoLogisticRegressionType, 'predict', no_unliteral=True)
def overload_logistic_regression_predict(m, X):
    return parallel_predict(m, X)


@overload_method(BodoLogisticRegressionType, 'score', no_unliteral=True)
def overload_logistic_regression_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


@overload_attribute(BodoLogisticRegressionType, 'coef_')
def get_logisticR_coef(m):

    def impl(m):
        with numba.objmode(result='float64[:,:]'):
            result = m.coef_
        return result
    return impl


class BodoLinearRegressionType(types.Opaque):

    def __init__(self):
        super(BodoLinearRegressionType, self).__init__(name=
            'BodoLinearRegressionType')


linear_regression_type = BodoLinearRegressionType()
types.linear_regression_type = linear_regression_type
register_model(BodoLinearRegressionType)(models.OpaqueModel)


@typeof_impl.register(sklearn.linear_model.LinearRegression)
def typeof_linear_regression(val, c):
    return linear_regression_type


@box(BodoLinearRegressionType)
def box_linear_regression(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoLinearRegressionType)
def unbox_linear_regression(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.linear_model.LinearRegression, no_unliteral=True)
def sklearn_linear_model_linear_regression_overload(fit_intercept=True,
    normalize=False, copy_X=True, n_jobs=None):
    check_sklearn_version()

    def _sklearn_linear_model_linear_regression_impl(fit_intercept=True,
        normalize=False, copy_X=True, n_jobs=None):
        with numba.objmode(m='linear_regression_type'):
            m = sklearn.linear_model.LinearRegression(fit_intercept=
                fit_intercept, normalize=normalize, copy_X=copy_X, n_jobs=
                n_jobs)
        return m
    return _sklearn_linear_model_linear_regression_impl


@overload_method(BodoLinearRegressionType, 'fit', no_unliteral=True)
def overload_linear_regression_fit(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    if is_overload_false(_is_data_distributed):

        def _linear_regression_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            with numba.objmode():
                m.fit(X, y, sample_weight)
            return m
        return _linear_regression_fit_impl
    else:

        def _sgdc_linear_regression_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            if bodo.get_rank() == 0:
                _raise_SGD_warning('SGDRegressor')
            with numba.objmode(clf='sgd_regressor_type'):
                clf = sklearn.linear_model.SGDRegressor(loss='squared_loss',
                    penalty=None, fit_intercept=m.fit_intercept)
            clf.fit(X, y, _is_data_distributed=True)
            with numba.objmode():
                m.coef_ = clf.coef_
                m.intercept_ = clf.intercept_
            return m
        return _sgdc_linear_regression_fit_impl


@overload_method(BodoLinearRegressionType, 'predict', no_unliteral=True)
def overload_linear_regression_predict(m, X):
    return parallel_predict_regression(m, X)


@overload_method(BodoLinearRegressionType, 'score', no_unliteral=True)
def overload_linear_regression_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


@overload_attribute(BodoLinearRegressionType, 'coef_')
def get_lr_coef(m):

    def impl(m):
        with numba.objmode(result='float64[:]'):
            result = m.coef_
        return result
    return impl


class BodoLassoType(types.Opaque):

    def __init__(self):
        super(BodoLassoType, self).__init__(name='BodoLassoType')


lasso_type = BodoLassoType()
types.lasso_type = lasso_type
register_model(BodoLassoType)(models.OpaqueModel)


@typeof_impl.register(sklearn.linear_model.Lasso)
def typeof_lasso(val, c):
    return lasso_type


@box(BodoLassoType)
def box_lasso(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoLassoType)
def unbox_lasso(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.linear_model.Lasso, no_unliteral=True)
def sklearn_linear_model_lasso_overload(alpha=1.0, fit_intercept=True,
    normalize=False, precompute=False, copy_X=True, max_iter=1000, tol=
    0.0001, warm_start=False, positive=False, random_state=None, selection=
    'cyclic'):
    check_sklearn_version()

    def _sklearn_linear_model_lasso_impl(alpha=1.0, fit_intercept=True,
        normalize=False, precompute=False, copy_X=True, max_iter=1000, tol=
        0.0001, warm_start=False, positive=False, random_state=None,
        selection='cyclic'):
        with numba.objmode(m='lasso_type'):
            m = sklearn.linear_model.Lasso(alpha=alpha, fit_intercept=
                fit_intercept, normalize=normalize, precompute=precompute,
                copy_X=copy_X, max_iter=max_iter, tol=tol, warm_start=
                warm_start, positive=positive, random_state=random_state,
                selection=selection)
        return m
    return _sklearn_linear_model_lasso_impl


@overload_method(BodoLassoType, 'fit', no_unliteral=True)
def overload_lasso_fit(m, X, y, sample_weight=None, check_input=True,
    _is_data_distributed=False):
    if is_overload_false(_is_data_distributed):

        def _lasso_fit_impl(m, X, y, sample_weight=None, check_input=True,
            _is_data_distributed=False):
            with numba.objmode():
                m.fit(X, y, sample_weight, check_input)
            return m
        return _lasso_fit_impl
    else:

        def _sgdc_lasso_fit_impl(m, X, y, sample_weight=None, check_input=
            True, _is_data_distributed=False):
            if bodo.get_rank() == 0:
                _raise_SGD_warning('SGDRegressor')
            with numba.objmode(clf='sgd_regressor_type'):
                clf = sklearn.linear_model.SGDRegressor(loss='squared_loss',
                    penalty='l1', alpha=m.alpha, fit_intercept=m.
                    fit_intercept, max_iter=m.max_iter, tol=m.tol,
                    warm_start=m.warm_start, random_state=m.random_state)
            clf.fit(X, y, _is_data_distributed=True)
            with numba.objmode():
                m.coef_ = clf.coef_
                m.intercept_ = clf.intercept_
                m.n_iter_ = clf.n_iter_
            return m
        return _sgdc_lasso_fit_impl


@overload_method(BodoLassoType, 'predict', no_unliteral=True)
def overload_lass_predict(m, X):
    return parallel_predict_regression(m, X)


@overload_method(BodoLassoType, 'score', no_unliteral=True)
def overload_lasso_score(m, X, y, sample_weight=None, _is_data_distributed=
    False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


class BodoRidgeType(types.Opaque):

    def __init__(self):
        super(BodoRidgeType, self).__init__(name='BodoRidgeType')


ridge_type = BodoRidgeType()
types.ridge_type = ridge_type
register_model(BodoRidgeType)(models.OpaqueModel)


@typeof_impl.register(sklearn.linear_model.Ridge)
def typeof_ridge(val, c):
    return ridge_type


@box(BodoRidgeType)
def box_ridge(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoRidgeType)
def unbox_ridge(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.linear_model.Ridge, no_unliteral=True)
def sklearn_linear_model_ridge_overload(alpha=1.0, fit_intercept=True,
    normalize=False, copy_X=True, max_iter=None, tol=0.001, solver='auto',
    random_state=None):
    check_sklearn_version()

    def _sklearn_linear_model_ridge_impl(alpha=1.0, fit_intercept=True,
        normalize=False, copy_X=True, max_iter=None, tol=0.001, solver=
        'auto', random_state=None):
        with numba.objmode(m='ridge_type'):
            m = sklearn.linear_model.Ridge(alpha=alpha, fit_intercept=
                fit_intercept, normalize=normalize, copy_X=copy_X, max_iter
                =max_iter, tol=tol, solver=solver, random_state=random_state)
        return m
    return _sklearn_linear_model_ridge_impl


@overload_method(BodoRidgeType, 'fit', no_unliteral=True)
def overload_ridge_fit(m, X, y, sample_weight=None, _is_data_distributed=False
    ):
    if is_overload_false(_is_data_distributed):

        def _ridge_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            with numba.objmode():
                m.fit(X, y, sample_weight)
            return m
        return _ridge_fit_impl
    else:

        def _ridge_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            if bodo.get_rank() == 0:
                _raise_SGD_warning('SGDRegressor')
            with numba.objmode(clf='sgd_regressor_type'):
                if m.max_iter is None:
                    max_iter = 1000
                else:
                    max_iter = m.max_iter
                clf = sklearn.linear_model.SGDRegressor(loss='squared_loss',
                    penalty='l2', alpha=0.001, fit_intercept=m.
                    fit_intercept, max_iter=max_iter, tol=m.tol,
                    random_state=m.random_state)
            clf.fit(X, y, _is_data_distributed=True)
            with numba.objmode():
                m.coef_ = clf.coef_
                m.intercept_ = clf.intercept_
                m.n_iter_ = clf.n_iter_
            return m
        return _ridge_fit_impl


@overload_method(BodoRidgeType, 'predict', no_unliteral=True)
def overload_linear_regression_predict(m, X):
    return parallel_predict_regression(m, X)


@overload_method(BodoRidgeType, 'score', no_unliteral=True)
def overload_linear_regression_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


@overload_attribute(BodoRidgeType, 'coef_')
def get_ridge_coef(m):

    def impl(m):
        with numba.objmode(result='float64[:]'):
            result = m.coef_
        return result
    return impl


class BodoLinearSVCType(types.Opaque):

    def __init__(self):
        super(BodoLinearSVCType, self).__init__(name='BodoLinearSVCType')


linear_svc_type = BodoLinearSVCType()
types.linear_svc_type = linear_svc_type
register_model(BodoLinearSVCType)(models.OpaqueModel)


@typeof_impl.register(sklearn.svm.LinearSVC)
def typeof_linear_svc(val, c):
    return linear_svc_type


@box(BodoLinearSVCType)
def box_linear_svc(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoLinearSVCType)
def unbox_linear_svc(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.svm.LinearSVC, no_unliteral=True)
def sklearn_svm_linear_svc_overload(penalty='l2', loss='squared_hinge',
    dual=True, tol=0.0001, C=1.0, multi_class='ovr', fit_intercept=True,
    intercept_scaling=1, class_weight=None, verbose=0, random_state=None,
    max_iter=1000):
    check_sklearn_version()

    def _sklearn_svm_linear_svc_impl(penalty='l2', loss='squared_hinge',
        dual=True, tol=0.0001, C=1.0, multi_class='ovr', fit_intercept=True,
        intercept_scaling=1, class_weight=None, verbose=0, random_state=
        None, max_iter=1000):
        with numba.objmode(m='linear_svc_type'):
            m = sklearn.svm.LinearSVC(penalty=penalty, loss=loss, dual=dual,
                tol=tol, C=C, multi_class=multi_class, fit_intercept=
                fit_intercept, intercept_scaling=intercept_scaling,
                class_weight=class_weight, verbose=verbose, random_state=
                random_state, max_iter=max_iter)
        return m
    return _sklearn_svm_linear_svc_impl


@overload_method(BodoLinearSVCType, 'fit', no_unliteral=True)
def overload_linear_svc_fit(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    if is_overload_false(_is_data_distributed):

        def _svm_linear_svc_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            with numba.objmode():
                m.fit(X, y, sample_weight)
            return m
        return _svm_linear_svc_fit_impl
    else:

        def _svm_linear_svc_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            if bodo.get_rank() == 0:
                _raise_SGD_warning('SGDClassifier')
            with numba.objmode(clf='sgd_classifier_type'):
                clf = sklearn.linear_model.SGDClassifier(loss='hinge',
                    penalty=m.penalty, tol=m.tol, fit_intercept=m.
                    fit_intercept, class_weight=m.class_weight,
                    random_state=m.random_state, max_iter=m.max_iter,
                    verbose=m.verbose)
            clf.fit(X, y, _is_data_distributed=True)
            with numba.objmode():
                m.coef_ = clf.coef_
                m.intercept_ = clf.intercept_
                m.n_iter_ = clf.n_iter_
                m.classes_ = clf.classes_
            return m
        return _svm_linear_svc_fit_impl


@overload_method(BodoLinearSVCType, 'predict', no_unliteral=True)
def overload_svm_linear_svc_predict(m, X):
    return parallel_predict(m, X)


@overload_method(BodoLinearSVCType, 'score', no_unliteral=True)
def overload_svm_linear_svc_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


class BodoPreprocessingStandardScalerType(types.Opaque):

    def __init__(self):
        super(BodoPreprocessingStandardScalerType, self).__init__(name=
            'BodoPreprocessingStandardScalerType')


preprocessing_standard_scaler_type = BodoPreprocessingStandardScalerType()
types.preprocessing_standard_scaler_type = preprocessing_standard_scaler_type
register_model(BodoPreprocessingStandardScalerType)(models.OpaqueModel)


@typeof_impl.register(sklearn.preprocessing.StandardScaler)
def typeof_preprocessing_standard_scaler(val, c):
    return preprocessing_standard_scaler_type


@box(BodoPreprocessingStandardScalerType)
def box_preprocessing_standard_scaler(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoPreprocessingStandardScalerType)
def unbox_preprocessing_standard_scaler(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.preprocessing.StandardScaler, no_unliteral=True)
def sklearn_preprocessing_standard_scaler_overload(copy=True, with_mean=
    True, with_std=True):
    check_sklearn_version()

    def _sklearn_preprocessing_standard_scaler_impl(copy=True, with_mean=
        True, with_std=True):
        with numba.objmode(m='preprocessing_standard_scaler_type'):
            m = sklearn.preprocessing.StandardScaler(copy=copy, with_mean=
                with_mean, with_std=with_std)
        return m
    return _sklearn_preprocessing_standard_scaler_impl


def sklearn_preprocessing_standard_scaler_fit_dist_helper(m, X):
    ctnln__rtz = MPI.COMM_WORLD
    tmx__jhwou = ctnln__rtz.Get_size()
    hth__wxgj = m.with_std
    fusw__omm = m.with_mean
    m.with_std = False
    if hth__wxgj:
        m.with_mean = True
    m = m.fit(X)
    m.with_std = hth__wxgj
    m.with_mean = fusw__omm
    if not isinstance(m.n_samples_seen_, numbers.Integral):
        yggun__fis = False
    else:
        yggun__fis = True
        m.n_samples_seen_ = np.repeat(m.n_samples_seen_, X.shape[1]).astype(np
            .int64, copy=False)
    hhoft__jnpwh = np.zeros((tmx__jhwou, *m.n_samples_seen_.shape), dtype=m
        .n_samples_seen_.dtype)
    ctnln__rtz.Allgather(m.n_samples_seen_, hhoft__jnpwh)
    xlind__uynem = np.sum(hhoft__jnpwh, axis=0)
    m.n_samples_seen_ = xlind__uynem
    if m.with_mean or m.with_std:
        sdr__qzqka = np.zeros((tmx__jhwou, *m.mean_.shape), dtype=m.mean_.dtype
            )
        ctnln__rtz.Allgather(m.mean_, sdr__qzqka)
        sdr__qzqka[np.isnan(sdr__qzqka)] = 0
        xxq__zmbzv = np.average(sdr__qzqka, axis=0, weights=hhoft__jnpwh)
        m.mean_ = xxq__zmbzv
    if m.with_std:
        bhrt__erds = sklearn_safe_accumulator_op(np.nansum, (X - xxq__zmbzv
            ) ** 2, axis=0) / xlind__uynem
        fjbl__vvgyj = np.zeros_like(bhrt__erds)
        ctnln__rtz.Allreduce(bhrt__erds, fjbl__vvgyj, op=MPI.SUM)
        m.var_ = fjbl__vvgyj
        m.scale_ = sklearn_handle_zeros_in_scale(np.sqrt(m.var_))
    yggun__fis = ctnln__rtz.allreduce(yggun__fis, op=MPI.LAND)
    if yggun__fis:
        m.n_samples_seen_ = m.n_samples_seen_[0]
    return m


@overload_method(BodoPreprocessingStandardScalerType, 'fit', no_unliteral=True)
def overload_preprocessing_standard_scaler_fit(m, X, y=None,
    _is_data_distributed=False):

    def _preprocessing_standard_scaler_fit_impl(m, X, y=None,
        _is_data_distributed=False):
        with numba.objmode(m='preprocessing_standard_scaler_type'):
            if _is_data_distributed:
                m = sklearn_preprocessing_standard_scaler_fit_dist_helper(m, X)
            else:
                m = m.fit(X, y)
        return m
    return _preprocessing_standard_scaler_fit_impl


@overload_method(BodoPreprocessingStandardScalerType, 'transform',
    no_unliteral=True)
def overload_preprocessing_standard_scaler_transform(m, X, copy=None):

    def _preprocessing_standard_scaler_transform_impl(m, X, copy=None):
        with numba.objmode(transformed_X='float64[:,:]'):
            transformed_X = m.transform(X, copy=copy)
        return transformed_X
    return _preprocessing_standard_scaler_transform_impl


@overload_method(BodoPreprocessingStandardScalerType, 'inverse_transform',
    no_unliteral=True)
def overload_preprocessing_standard_scaler_inverse_transform(m, X, copy=None):

    def _preprocessing_standard_scaler_inverse_transform_impl(m, X, copy=None):
        with numba.objmode(inverse_transformed_X='float64[:,:]'):
            inverse_transformed_X = m.inverse_transform(X, copy=copy)
        return inverse_transformed_X
    return _preprocessing_standard_scaler_inverse_transform_impl


def get_data_slice_parallel(data, labels, len_train):
    gcpo__kwr = data[:len_train]
    lnp__gjy = data[len_train:]
    gcpo__kwr = bodo.rebalance(gcpo__kwr)
    lnp__gjy = bodo.rebalance(lnp__gjy)
    lhi__utk = labels[:len_train]
    bfaq__yoj = labels[len_train:]
    lhi__utk = bodo.rebalance(lhi__utk)
    bfaq__yoj = bodo.rebalance(bfaq__yoj)
    return gcpo__kwr, lnp__gjy, lhi__utk, bfaq__yoj


@numba.njit
def get_train_test_size(train_size, test_size):
    if train_size is None:
        train_size = -1.0
    if test_size is None:
        test_size = -1.0
    if train_size == -1.0 and test_size == -1.0:
        return 0.75, 0.25
    elif test_size == -1.0:
        return train_size, 1.0 - train_size
    elif train_size == -1.0:
        return 1.0 - test_size, test_size
    elif train_size + test_size > 1:
        raise ValueError(
            'The sum of test_size and train_size, should be in the (0, 1) range. Reduce test_size and/or train_size.'
            )
    else:
        return train_size, test_size


def set_labels_type(labels, label_type):
    return labels


@overload(set_labels_type, no_unliteral=True)
def overload_set_labels_type(labels, label_type):
    if get_overload_const_int(label_type) == 1:

        def _set_labels(labels, label_type):
            return pd.Series(labels)
        return _set_labels
    elif get_overload_const_int(label_type) == 2:

        def _set_labels(labels, label_type):
            return labels.values
        return _set_labels
    else:

        def _set_labels(labels, label_type):
            return labels
        return _set_labels


def reset_labels_type(labels, label_type):
    return labels


@overload(reset_labels_type, no_unliteral=True)
def overload_reset_labels_type(labels, label_type):
    if get_overload_const_int(label_type) == 1:

        def _reset_labels(labels, label_type):
            return labels.values
        return _reset_labels
    elif get_overload_const_int(label_type) == 2:

        def _reset_labels(labels, label_type):
            return pd.Series(labels, index=np.arange(len(labels)))
        return _reset_labels
    else:

        def _reset_labels(labels, label_type):
            return labels
        return _reset_labels


@overload(sklearn.model_selection.train_test_split, no_unliteral=True)
def overload_train_test_split(data, labels=None, train_size=None, test_size
    =None, random_state=None, shuffle=True, stratify=None,
    _is_data_distributed=False):
    check_sklearn_version()
    bpf__vbk = {'stratify': stratify}
    hzr__tneup = {'stratify': None}
    check_unsupported_args('train_test_split', bpf__vbk, hzr__tneup, 'ml')
    if is_overload_false(_is_data_distributed):
        urvfy__jfm = f'data_split_type_{numba.core.ir_utils.next_label()}'
        tpujt__ekop = f'labels_split_type_{numba.core.ir_utils.next_label()}'
        for rjy__ucgf, zxr__rzp in ((data, urvfy__jfm), (labels, tpujt__ekop)):
            if isinstance(rjy__ucgf, (DataFrameType, SeriesType)):
                ldote__wmy = rjy__ucgf.copy(index=NumericIndexType(types.int64)
                    )
                setattr(types, zxr__rzp, ldote__wmy)
            else:
                setattr(types, zxr__rzp, rjy__ucgf)
        nzxqb__mnjn = 'def _train_test_split_impl(\n'
        nzxqb__mnjn += '    data,\n'
        nzxqb__mnjn += '    labels=None,\n'
        nzxqb__mnjn += '    train_size=None,\n'
        nzxqb__mnjn += '    test_size=None,\n'
        nzxqb__mnjn += '    random_state=None,\n'
        nzxqb__mnjn += '    shuffle=True,\n'
        nzxqb__mnjn += '    stratify=None,\n'
        nzxqb__mnjn += '    _is_data_distributed=False,\n'
        nzxqb__mnjn += '):  # pragma: no cover\n'
        nzxqb__mnjn += (
            """    with numba.objmode(data_train='{}', data_test='{}', labels_train='{}', labels_test='{}'):
"""
            .format(urvfy__jfm, urvfy__jfm, tpujt__ekop, tpujt__ekop))
        nzxqb__mnjn += """        data_train, data_test, labels_train, labels_test = sklearn.model_selection.train_test_split(
"""
        nzxqb__mnjn += '            data,\n'
        nzxqb__mnjn += '            labels,\n'
        nzxqb__mnjn += '            train_size=train_size,\n'
        nzxqb__mnjn += '            test_size=test_size,\n'
        nzxqb__mnjn += '            random_state=random_state,\n'
        nzxqb__mnjn += '            shuffle=shuffle,\n'
        nzxqb__mnjn += '            stratify=stratify,\n'
        nzxqb__mnjn += '        )\n'
        nzxqb__mnjn += (
            '    return data_train, data_test, labels_train, labels_test\n')
        dqmyz__nzoms = {}
        exec(nzxqb__mnjn, globals(), dqmyz__nzoms)
        _train_test_split_impl = dqmyz__nzoms['_train_test_split_impl']
        return _train_test_split_impl
    else:
        global get_data_slice_parallel
        if isinstance(get_data_slice_parallel, pytypes.FunctionType):
            get_data_slice_parallel = bodo.jit(get_data_slice_parallel,
                all_args_distributed_varlength=True,
                all_returns_distributed=True)
        label_type = 0
        if isinstance(data, DataFrameType) and isinstance(labels, types.Array):
            label_type = 1
        elif isinstance(data, types.Array) and isinstance(labels, SeriesType):
            label_type = 2
        if is_overload_none(random_state):
            random_state = 42

        def _train_test_split_impl(data, labels=None, train_size=None,
            test_size=None, random_state=None, shuffle=True, stratify=None,
            _is_data_distributed=False):
            if data.shape[0] != labels.shape[0]:
                raise ValueError(
                    'Found input variables with inconsistent number of samples\n'
                    )
            train_size, test_size = get_train_test_size(train_size, test_size)
            xxnpq__dlpl = bodo.libs.distributed_api.dist_reduce(len(data),
                np.int32(Reduce_Type.Sum.value))
            len_train = int(xxnpq__dlpl * train_size)
            cqc__apn = xxnpq__dlpl - len_train
            if shuffle:
                labels = set_labels_type(labels, label_type)
                fkzdl__dmifb = bodo.get_rank()
                znkj__kjxm = bodo.get_size()
                zpy__vlod = np.empty(znkj__kjxm, np.int64)
                bodo.libs.distributed_api.allgather(zpy__vlod, len(data))
                eanah__rfqg = np.cumsum(zpy__vlod[0:fkzdl__dmifb + 1])
                wvxh__vxneu = np.full(xxnpq__dlpl, True)
                wvxh__vxneu[:cqc__apn] = False
                np.random.seed(42)
                np.random.permutation(wvxh__vxneu)
                if fkzdl__dmifb:
                    poblg__lnh = eanah__rfqg[fkzdl__dmifb - 1]
                else:
                    poblg__lnh = 0
                ixna__vcm = eanah__rfqg[fkzdl__dmifb]
                mosd__fpb = wvxh__vxneu[poblg__lnh:ixna__vcm]
                gcpo__kwr = data[mosd__fpb]
                lnp__gjy = data[~mosd__fpb]
                lhi__utk = labels[mosd__fpb]
                bfaq__yoj = labels[~mosd__fpb]
                gcpo__kwr = bodo.random_shuffle(gcpo__kwr, seed=
                    random_state, parallel=True)
                lnp__gjy = bodo.random_shuffle(lnp__gjy, seed=random_state,
                    parallel=True)
                lhi__utk = bodo.random_shuffle(lhi__utk, seed=random_state,
                    parallel=True)
                bfaq__yoj = bodo.random_shuffle(bfaq__yoj, seed=
                    random_state, parallel=True)
                lhi__utk = reset_labels_type(lhi__utk, label_type)
                bfaq__yoj = reset_labels_type(bfaq__yoj, label_type)
            else:
                gcpo__kwr, lnp__gjy, lhi__utk, bfaq__yoj = (
                    get_data_slice_parallel(data, labels, len_train))
            return gcpo__kwr, lnp__gjy, lhi__utk, bfaq__yoj
        return _train_test_split_impl


class BodoPreprocessingMinMaxScalerType(types.Opaque):

    def __init__(self):
        super(BodoPreprocessingMinMaxScalerType, self).__init__(name=
            'BodoPreprocessingMinMaxScalerType')


preprocessing_minmax_scaler_type = BodoPreprocessingMinMaxScalerType()
types.preprocessing_minmax_scaler_type = preprocessing_minmax_scaler_type
register_model(BodoPreprocessingMinMaxScalerType)(models.OpaqueModel)


@typeof_impl.register(sklearn.preprocessing.MinMaxScaler)
def typeof_preprocessing_minmax_scaler(val, c):
    return preprocessing_minmax_scaler_type


@box(BodoPreprocessingMinMaxScalerType)
def box_preprocessing_minmax_scaler(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoPreprocessingMinMaxScalerType)
def unbox_preprocessing_minmax_scaler(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.preprocessing.MinMaxScaler, no_unliteral=True)
def sklearn_preprocessing_minmax_scaler_overload(feature_range=(0, 1), copy
    =True, clip=False):
    check_sklearn_version()

    def _sklearn_preprocessing_minmax_scaler_impl(feature_range=(0, 1),
        copy=True, clip=False):
        with numba.objmode(m='preprocessing_minmax_scaler_type'):
            m = sklearn.preprocessing.MinMaxScaler(feature_range=
                feature_range, copy=copy, clip=clip)
        return m
    return _sklearn_preprocessing_minmax_scaler_impl


def sklearn_preprocessing_minmax_scaler_fit_dist_helper(m, X):
    ctnln__rtz = MPI.COMM_WORLD
    tmx__jhwou = ctnln__rtz.Get_size()
    m = m.fit(X)
    xlind__uynem = ctnln__rtz.allreduce(m.n_samples_seen_, op=MPI.SUM)
    m.n_samples_seen_ = xlind__uynem
    dlzvh__jhggq = np.zeros((tmx__jhwou, *m.data_min_.shape), dtype=m.
        data_min_.dtype)
    ctnln__rtz.Allgather(m.data_min_, dlzvh__jhggq)
    uidm__ojw = np.nanmin(dlzvh__jhggq, axis=0)
    wfczj__lefkc = np.zeros((tmx__jhwou, *m.data_max_.shape), dtype=m.
        data_max_.dtype)
    ctnln__rtz.Allgather(m.data_max_, wfczj__lefkc)
    uwj__eff = np.nanmax(wfczj__lefkc, axis=0)
    gxcb__jpal = uwj__eff - uidm__ojw
    m.scale_ = (m.feature_range[1] - m.feature_range[0]
        ) / sklearn_handle_zeros_in_scale(gxcb__jpal)
    m.min_ = m.feature_range[0] - uidm__ojw * m.scale_
    m.data_min_ = uidm__ojw
    m.data_max_ = uwj__eff
    m.data_range_ = gxcb__jpal
    return m


@overload_method(BodoPreprocessingMinMaxScalerType, 'fit', no_unliteral=True)
def overload_preprocessing_minmax_scaler_fit(m, X, y=None,
    _is_data_distributed=False):

    def _preprocessing_minmax_scaler_fit_impl(m, X, y=None,
        _is_data_distributed=False):
        with numba.objmode(m='preprocessing_minmax_scaler_type'):
            if _is_data_distributed:
                m = sklearn_preprocessing_minmax_scaler_fit_dist_helper(m, X)
            else:
                m = m.fit(X, y)
        return m
    return _preprocessing_minmax_scaler_fit_impl


@overload_method(BodoPreprocessingMinMaxScalerType, 'transform',
    no_unliteral=True)
def overload_preprocessing_minmax_scaler_transform(m, X):

    def _preprocessing_minmax_scaler_transform_impl(m, X):
        with numba.objmode(transformed_X='float64[:,:]'):
            transformed_X = m.transform(X)
        return transformed_X
    return _preprocessing_minmax_scaler_transform_impl


@overload_method(BodoPreprocessingMinMaxScalerType, 'inverse_transform',
    no_unliteral=True)
def overload_preprocessing_minmax_scaler_inverse_transform(m, X):

    def _preprocessing_minmax_scaler_inverse_transform_impl(m, X):
        with numba.objmode(inverse_transformed_X='float64[:,:]'):
            inverse_transformed_X = m.inverse_transform(X)
        return inverse_transformed_X
    return _preprocessing_minmax_scaler_inverse_transform_impl


class BodoPreprocessingLabelEncoderType(types.Opaque):

    def __init__(self):
        super(BodoPreprocessingLabelEncoderType, self).__init__(name=
            'BodoPreprocessingLabelEncoderType')


preprocessing_label_encoder_type = BodoPreprocessingLabelEncoderType()
types.preprocessing_label_encoder_type = preprocessing_label_encoder_type
register_model(BodoPreprocessingLabelEncoderType)(models.OpaqueModel)


@typeof_impl.register(sklearn.preprocessing.LabelEncoder)
def typeof_preprocessing_label_encoder(val, c):
    return preprocessing_label_encoder_type


@box(BodoPreprocessingLabelEncoderType)
def box_preprocessing_label_encoder(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoPreprocessingLabelEncoderType)
def unbox_preprocessing_label_encoder(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.preprocessing.LabelEncoder, no_unliteral=True)
def sklearn_preprocessing_label_encoder_overload():
    check_sklearn_version()

    def _sklearn_preprocessing_label_encoder_impl():
        with numba.objmode(m='preprocessing_label_encoder_type'):
            m = sklearn.preprocessing.LabelEncoder()
        return m
    return _sklearn_preprocessing_label_encoder_impl


@overload_method(BodoPreprocessingLabelEncoderType, 'fit', no_unliteral=True)
def overload_preprocessing_label_encoder_fit(m, y, _is_data_distributed=False):
    if is_overload_true(_is_data_distributed):

        def _sklearn_preprocessing_label_encoder_fit_impl(m, y,
            _is_data_distributed=False):
            y_classes = bodo.libs.array_kernels.unique(y, parallel=True)
            y_classes = bodo.allgatherv(y_classes, False)
            y_classes = bodo.libs.array_kernels.sort(y_classes, ascending=
                True, inplace=False)
            with numba.objmode:
                m.classes_ = y_classes
            return m
        return _sklearn_preprocessing_label_encoder_fit_impl
    else:

        def _sklearn_preprocessing_label_encoder_fit_impl(m, y,
            _is_data_distributed=False):
            with numba.objmode(m='preprocessing_label_encoder_type'):
                m = m.fit(y)
            return m
        return _sklearn_preprocessing_label_encoder_fit_impl


@overload_method(BodoPreprocessingLabelEncoderType, 'transform',
    no_unliteral=True)
def overload_preprocessing_label_encoder_transform(m, y,
    _is_data_distributed=False):

    def _preprocessing_label_encoder_transform_impl(m, y,
        _is_data_distributed=False):
        with numba.objmode(transformed_y='int64[:]'):
            transformed_y = m.transform(y)
        return transformed_y
    return _preprocessing_label_encoder_transform_impl


@numba.njit
def le_fit_transform(m, y):
    m = m.fit(y, _is_data_distributed=True)
    transformed_y = m.transform(y, _is_data_distributed=True)
    return transformed_y


@overload_method(BodoPreprocessingLabelEncoderType, 'fit_transform',
    no_unliteral=True)
def overload_preprocessing_label_encoder_fit_transform(m, y,
    _is_data_distributed=False):
    if is_overload_true(_is_data_distributed):

        def _preprocessing_label_encoder_fit_transform_impl(m, y,
            _is_data_distributed=False):
            transformed_y = le_fit_transform(m, y)
            return transformed_y
        return _preprocessing_label_encoder_fit_transform_impl
    else:

        def _preprocessing_label_encoder_fit_transform_impl(m, y,
            _is_data_distributed=False):
            with numba.objmode(transformed_y='int64[:]'):
                transformed_y = m.fit_transform(y)
            return transformed_y
        return _preprocessing_label_encoder_fit_transform_impl


class BodoFExtractHashingVectorizerType(types.Opaque):

    def __init__(self):
        super(BodoFExtractHashingVectorizerType, self).__init__(name=
            'BodoFExtractHashingVectorizerType')


f_extract_hashing_vectorizer_type = BodoFExtractHashingVectorizerType()
types.f_extract_hashing_vectorizer_type = f_extract_hashing_vectorizer_type
register_model(BodoFExtractHashingVectorizerType)(models.OpaqueModel)


@typeof_impl.register(sklearn.feature_extraction.text.HashingVectorizer)
def typeof_f_extract_hashing_vectorizer(val, c):
    return f_extract_hashing_vectorizer_type


@box(BodoFExtractHashingVectorizerType)
def box_f_extract_hashing_vectorizer(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoFExtractHashingVectorizerType)
def unbox_f_extract_hashing_vectorizer(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.feature_extraction.text.HashingVectorizer, no_unliteral=True)
def sklearn_hashing_vectorizer_overload(input='content', encoding='utf-8',
    decode_error='strict', strip_accents=None, lowercase=True, preprocessor
    =None, tokenizer=None, stop_words=None, token_pattern=
    '(?u)\\b\\w\\w+\\b', ngram_range=(1, 1), analyzer='word', n_features=2 **
    20, binary=False, norm='l2', alternate_sign=True, dtype=np.float64):
    check_sklearn_version()

    def _sklearn_hashing_vectorizer_impl(input='content', encoding='utf-8',
        decode_error='strict', strip_accents=None, lowercase=True,
        preprocessor=None, tokenizer=None, stop_words=None, token_pattern=
        '(?u)\\b\\w\\w+\\b', ngram_range=(1, 1), analyzer='word',
        n_features=2 ** 20, binary=False, norm='l2', alternate_sign=True,
        dtype=np.float64):
        with numba.objmode(m='f_extract_hashing_vectorizer_type'):
            m = sklearn.feature_extraction.text.HashingVectorizer(input=
                input, encoding=encoding, decode_error=decode_error,
                strip_accents=strip_accents, lowercase=lowercase,
                preprocessor=preprocessor, tokenizer=tokenizer, stop_words=
                stop_words, token_pattern=token_pattern, ngram_range=
                ngram_range, analyzer=analyzer, n_features=n_features,
                binary=binary, norm=norm, alternate_sign=alternate_sign,
                dtype=dtype)
        return m
    return _sklearn_hashing_vectorizer_impl


@overload_method(BodoFExtractHashingVectorizerType, 'fit_transform',
    no_unliteral=True)
def overload_hashing_vectorizer_fit_transform(m, X, y=None,
    _is_data_distributed=False):
    types.csr_matrix_float64_int64 = CSRMatrixType(types.float64, types.int64)

    def _hashing_vectorizer_fit_transform_impl(m, X, y=None,
        _is_data_distributed=False):
        with numba.objmode(transformed_X='csr_matrix_float64_int64'):
            transformed_X = m.fit_transform(X, y)
            transformed_X.indices = transformed_X.indices.astype(np.int64)
            transformed_X.indptr = transformed_X.indptr.astype(np.int64)
        return transformed_X
    return _hashing_vectorizer_fit_transform_impl


class BodoRandomForestRegressorType(types.Opaque):

    def __init__(self):
        super(BodoRandomForestRegressorType, self).__init__(name=
            'BodoRandomForestRegressorType')


random_forest_regressor_type = BodoRandomForestRegressorType()
types.random_forest_regressor_type = random_forest_regressor_type
register_model(BodoRandomForestRegressorType)(models.OpaqueModel)


@typeof_impl.register(sklearn.ensemble.RandomForestRegressor)
def typeof_random_forest_regressor(val, c):
    return random_forest_regressor_type


@box(BodoRandomForestRegressorType)
def box_random_forest_regressor(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoRandomForestRegressorType)
def unbox_random_forest_regressor(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.ensemble.RandomForestRegressor, no_unliteral=True)
def overload_sklearn_rf_regressor(n_estimators=100, criterion='mse',
    max_depth=None, min_samples_split=2, min_samples_leaf=1,
    min_weight_fraction_leaf=0.0, max_features='auto', max_leaf_nodes=None,
    min_impurity_decrease=0.0, min_impurity_split=None, bootstrap=True,
    oob_score=False, n_jobs=None, random_state=None, verbose=0, warm_start=
    False, ccp_alpha=0.0, max_samples=None):
    check_sklearn_version()

    def _sklearn_ensemble_RandomForestRegressor_impl(n_estimators=100,
        criterion='mse', max_depth=None, min_samples_split=2,
        min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features=
        'auto', max_leaf_nodes=None, min_impurity_decrease=0.0,
        min_impurity_split=None, bootstrap=True, oob_score=False, n_jobs=
        None, random_state=None, verbose=0, warm_start=False, ccp_alpha=0.0,
        max_samples=None):
        with numba.objmode(m='random_forest_regressor_type'):
            if random_state is not None and get_num_nodes() > 1:
                print(
                    'With multinode, fixed random_state seed values are ignored.\n'
                    )
                random_state = None
            m = sklearn.ensemble.RandomForestRegressor(n_estimators=
                n_estimators, criterion=criterion, max_depth=max_depth,
                min_samples_split=min_samples_split, min_samples_leaf=
                min_samples_leaf, min_weight_fraction_leaf=
                min_weight_fraction_leaf, max_features=max_features,
                max_leaf_nodes=max_leaf_nodes, min_impurity_decrease=
                min_impurity_decrease, min_impurity_split=
                min_impurity_split, bootstrap=bootstrap, oob_score=
                oob_score, n_jobs=1, random_state=random_state, verbose=
                verbose, warm_start=warm_start, ccp_alpha=ccp_alpha,
                max_samples=max_samples)
        return m
    return _sklearn_ensemble_RandomForestRegressor_impl


@overload_method(BodoRandomForestRegressorType, 'predict', no_unliteral=True)
def overload_rf_regressor_predict(m, X):
    return parallel_predict_regression(m, X)


@overload_method(BodoRandomForestRegressorType, 'score', no_unliteral=True)
def overload_rf_regressor_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


@overload_method(BodoRandomForestRegressorType, 'fit', no_unliteral=True)
@overload_method(BodoRandomForestClassifierType, 'fit', no_unliteral=True)
def overload_rf_classifier_model_fit(m, X, y, _is_data_distributed=False):

    def _model_fit_impl(m, X, y, _is_data_distributed=False):
        with numba.objmode(first_rank_node='int32[:]'):
            first_rank_node = get_nodes_first_ranks()
        if _is_data_distributed:
            kdki__nzcsf = len(first_rank_node)
            X = bodo.gatherv(X)
            y = bodo.gatherv(y)
            if kdki__nzcsf > 1:
                X = bodo.libs.distributed_api.bcast_comm(X, comm_ranks=
                    first_rank_node, nranks=kdki__nzcsf)
                y = bodo.libs.distributed_api.bcast_comm(y, comm_ranks=
                    first_rank_node, nranks=kdki__nzcsf)
        with numba.objmode:
            random_forest_model_fit(m, X, y)
        bodo.barrier()
        return m
    return _model_fit_impl


class BodoFExtractCountVectorizerType(types.Opaque):

    def __init__(self):
        super(BodoFExtractCountVectorizerType, self).__init__(name=
            'BodoFExtractCountVectorizerType')


f_extract_count_vectorizer_type = BodoFExtractCountVectorizerType()
types.f_extract_count_vectorizer_type = f_extract_count_vectorizer_type
register_model(BodoFExtractCountVectorizerType)(models.OpaqueModel)


@typeof_impl.register(sklearn.feature_extraction.text.CountVectorizer)
def typeof_f_extract_count_vectorizer(val, c):
    return f_extract_count_vectorizer_type


@box(BodoFExtractCountVectorizerType)
def box_f_extract_count_vectorizer(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoFExtractCountVectorizerType)
def unbox_f_extract_count_vectorizer(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.feature_extraction.text.CountVectorizer, no_unliteral=True)
def sklearn_count_vectorizer_overload(input='content', encoding='utf-8',
    decode_error='strict', strip_accents=None, lowercase=True, preprocessor
    =None, tokenizer=None, stop_words=None, token_pattern=
    '(?u)\\b\\w\\w+\\b', ngram_range=(1, 1), analyzer='word', max_df=1.0,
    max_features=None, vocabulary=None, binary=False, dtype=np.int64):
    check_sklearn_version()

    def _sklearn_count_vectorizer_impl(input='content', encoding='utf-8',
        decode_error='strict', strip_accents=None, lowercase=True,
        preprocessor=None, tokenizer=None, stop_words=None, token_pattern=
        '(?u)\\b\\w\\w+\\b', ngram_range=(1, 1), analyzer='word', max_df=
        1.0, max_features=None, vocabulary=None, binary=False, dtype=np.int64):
        with numba.objmode(m='f_extract_count_vectorizer_type'):
            m = sklearn.feature_extraction.text.CountVectorizer(input=input,
                encoding=encoding, decode_error=decode_error, strip_accents
                =strip_accents, lowercase=lowercase, preprocessor=
                preprocessor, tokenizer=tokenizer, stop_words=stop_words,
                token_pattern=token_pattern, ngram_range=ngram_range,
                analyzer=analyzer, max_df=max_df, max_features=max_features,
                vocabulary=vocabulary, binary=binary, dtype=dtype)
        return m
    return _sklearn_count_vectorizer_impl


@overload_attribute(BodoFExtractCountVectorizerType, 'vocabulary_')
def get_cv_vocabulary_(m):
    types.dict_string_int = types.DictType(types.unicode_type, types.int64)

    def impl(m):
        with numba.objmode(result='dict_string_int'):
            result = m.vocabulary_
        return result
    return impl


def _cv_fit_transform_helper(m, X):
    dath__yufb = False
    local_vocabulary = m.vocabulary
    if m.vocabulary is None:
        m.fit(X)
        local_vocabulary = m.vocabulary_
        dath__yufb = True
    return dath__yufb, local_vocabulary


@overload_method(BodoFExtractCountVectorizerType, 'fit_transform',
    no_unliteral=True)
def overload_count_vectorizer_fit_transform(m, X, y=None,
    _is_data_distributed=False):
    check_sklearn_version()
    types.csr_matrix_int64_int64 = CSRMatrixType(types.int64, types.int64)
    if is_overload_true(_is_data_distributed):
        types.dict_str_int = types.DictType(types.unicode_type, types.int64)

        def _count_vectorizer_fit_transform_impl(m, X, y=None,
            _is_data_distributed=False):
            with numba.objmode(local_vocabulary='dict_str_int', changeVoc=
                'bool_'):
                changeVoc, local_vocabulary = _cv_fit_transform_helper(m, X)
            if changeVoc:
                local_vocabulary = bodo.utils.conversion.coerce_to_array(list
                    (local_vocabulary.keys()))
                puagl__wupf = bodo.libs.array_kernels.unique(local_vocabulary,
                    parallel=True)
                puagl__wupf = bodo.allgatherv(puagl__wupf, False)
                puagl__wupf = bodo.libs.array_kernels.sort(puagl__wupf,
                    ascending=True, inplace=True)
                lkwo__usjys = {}
                for hyb__mhk in range(len(puagl__wupf)):
                    lkwo__usjys[puagl__wupf[hyb__mhk]] = hyb__mhk
            else:
                lkwo__usjys = local_vocabulary
            with numba.objmode(transformed_X='csr_matrix_int64_int64'):
                if changeVoc:
                    m.vocabulary = lkwo__usjys
                transformed_X = m.fit_transform(X, y)
                transformed_X.indices = transformed_X.indices.astype(np.int64)
                transformed_X.indptr = transformed_X.indptr.astype(np.int64)
            return transformed_X
        return _count_vectorizer_fit_transform_impl
    else:

        def _count_vectorizer_fit_transform_impl(m, X, y=None,
            _is_data_distributed=False):
            with numba.objmode(transformed_X='csr_matrix_int64_int64'):
                transformed_X = m.fit_transform(X, y)
                transformed_X.indices = transformed_X.indices.astype(np.int64)
                transformed_X.indptr = transformed_X.indptr.astype(np.int64)
            return transformed_X
        return _count_vectorizer_fit_transform_impl


@overload_method(BodoFExtractCountVectorizerType, 'get_feature_names',
    no_unliteral=True)
def overload_count_vectorizer_get_feature_names(m):
    check_sklearn_version()

    def impl(m):
        with numba.objmode(result=bodo.string_array_type):
            result = m.get_feature_names()
        return result
    return impl
