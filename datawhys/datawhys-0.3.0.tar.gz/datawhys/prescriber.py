from io import BytesIO
import json

import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, train_test_split

import datawhys as dw
from datawhys.core.frame import DataWhysFrame
from datawhys.core.meta import BaseExploration
from datawhys.core.series import DataWhysSeries
from datawhys.dd_transformer import DDTransformer
from datawhys.error import NotEnoughPointsError
from datawhys.utils import meta as meta_utils, utilities


class Solver:
    """
    DataWhys Solver object.

    Applies a stochastic search for the global maximum Z-score with respect to
    a defined dependent variable and target class, in cases of "discrete" variables
    or target min/max mean in the cases of "continuous" variables.

    Parameters
    ----------
    min_size_frac: float (optional), default=0.2
        Value between 0.0 and 1.0 that defines the minimum number of points needed
        for a valid rule discovered by the DataWhys solver.

    min_purity: float (optional), default=0.0
        Value between 0.0 and 1.0 that defines the minimum purity needed for a valid
        rule discovered by the DataWhys solver.

        Purity here is defined as the mean of the target variable distribution.

    max_cycles: int (optional), default=90
        Value greater than 0 that defines the total cycles the DataWhys solver should
        commit in order to find a valid rule.

    Examples
    --------
    Using the solver to find a rule

    >>> dw.api_key = "<API KEY>"
    >>> dw.api_secret = "<API SECRET>"
    >>> solver = dw.Solver()
    >>> solver.fit(dwf_explorable, dwf_outcome)
    >>> solver.rule
    {
        'sex': {'low': 'male', 'high': 'male'},
        'class': {'low': 2, 'high': 3},
        'parch': {'low': 0, 'high': 0},
        'ticketnumber': {'low': 2152.0, 'high': 3101281.0}
    }
    >>> solver.score
    12.974682681486312


    """

    def __init__(
        self, min_size_frac=0.2, min_purity=0.0, max_cycles=90,
    ):
        self.min_size_frac = min_size_frac
        self.min_purity = min_purity
        self.max_cycles = max_cycles

    @staticmethod
    def _is_one_dim_solve(explorable_vars):
        return explorable_vars.shape[1] == 1

    @staticmethod
    def _get_timeout(n_points, n_features, lg_coefficient=3.5, max_cycles=90):

        lg_timeout = int(lg_coefficient * np.sqrt(n_points * n_features / 2))
        min_timeout = np.minimum(lg_timeout, max_cycles)

        return int(np.maximum(1, min_timeout))

    @staticmethod
    def _get_dataset_buffer(df: pd.DataFrame):
        buffer = BytesIO()
        df.to_parquet(buffer)
        buffer.seek(0)
        return buffer

    def get_min_size_from_frac(self, data, outcome, target):
        if data[outcome].dtype == np.object:
            return self.min_size_frac * data.loc[data[outcome] == target, outcome].size
        else:
            return self.min_size_frac * data[outcome].size

    def set_min_size_frac_from_size(self, data, outcome, target, size):
        try:
            if data[outcome].dtype == np.object:
                self.min_size_frac = min(
                    0.95, size / data.loc[data[outcome] == target, outcome].size
                )
            else:
                self.min_size_frac = min(0.95, size / data[outcome].size)
        except ZeroDivisionError:
            pass

    def _run_solve(self, dwf: DataWhysFrame, outcome: str, target: str):
        encoder = DDTransformer(dwf)
        edf = utilities.encode_dataframe(dwf, encoder)
        target_encoded = utilities.encode_value(dwf, outcome, target, encoder)
        outcome_encoded = encoder.original_to_encoded_column(outcome)

        edf, _ = utilities.sample_if_needed(edf, target_encoded, outcome_encoded)

        enough_points = utilities.has_enough_values(
            edf, target_encoded, outcome_encoded
        )
        if not enough_points:
            raise NotEnoughPointsError(
                "Cannot run solver unless there are at least {0} points.".format(
                    utilities.MIN_SOLVER_SIZE
                )
            )

        # Solve Behavior isn't supported by file endpoint yet
        timeout = self._get_timeout(
            edf.shape[0], edf.shape[1] - 1, max_cycles=self.max_cycles
        )

        buf = Solver._get_dataset_buffer(edf)
        task = dw.api.solve_start_file(
            outcome=outcome_encoded,
            target=target_encoded,
            data=buf,
            timeout=timeout,
            min_size_frac=self.min_size_frac,
        )
        result = dw.api.solve_result(id=task["id"])

        rule_encoded = result["rule"]
        rule_decoded = utilities.decode_rule(rule_encoded, encoder)

        discarded_rules = result["diagnostics"].get("discarded_rules", None)
        discarded_rules_encoded = discarded_rules["rules"]
        discarded_rules_decoded = [
            utilities.decode_rule(rule_encoded, encoder)
            for rule_encoded in discarded_rules_encoded
        ]
        discarded_rules["rules"] = discarded_rules_decoded

        # Stats
        if dwf[outcome].var_type == "discrete":
            # Discrete Stats - operate in original space
            dwf_applied = utilities.apply_rule_to_df(dwf, rule_decoded)

            sample_stats = utilities.get_stats(dwf_applied, outcome, target)
            score = utilities.score_rule(dwf, rule_decoded, outcome, target)
        else:
            # Continous Stats - operate in encoded space
            edf_applied = utilities.apply_rule_to_df(edf, rule_encoded)

            sample_stats = utilities.get_stats(
                edf_applied, outcome_encoded, target_encoded
            )
            score = utilities.score_rule(
                edf, rule_encoded, outcome_encoded, target_encoded
            )

        return rule_decoded, sample_stats, score, discarded_rules

    @property
    def max_cycles(self):
        return self._max_cycles

    @max_cycles.setter
    def max_cycles(self, value):
        if value > 0:
            self._max_cycles = value
        else:
            raise ValueError("'max_cycles' must be greater than 0.")

    def get_rule_data(self, dataset=None, xrule=False):
        """
        Return a DataWhysFrame that is filtered or not filtered by a rule

        Parameters
        ----------
        dataset: DataWhysFrame of shape (n_samples, n_features)
            Where n_samples is the number of samples and n_features is the number of
            features.

        xrule: Bool, optional (default=False)
            Where `xrule` refers to `not rule` and, if True, returns the portion of the
            dataset not defined by the rule and False returns the portion of the dataset
            defined by the rule.

        """

        if xrule:
            idx = utilities.apply_rule_to_df(dataset, self.rule).index
            xidx = dataset.index[~np.in1d(dataset.index, idx)]
            return dataset.loc[xidx]
        else:
            return utilities.apply_rule_to_df(dataset, self.rule)

    def fit(self, m_X, m_y, cv=None):
        """
        Fit the Solver with the provided data.

        Parameters
        ----------
        m_X: DataWhysFrame of shape (n_samples, n_features)
            Where n_samples is the number of samples and n_features is the number
            of features

        m_y: DataWhysSeries of shape (n_samples,)
            Where n_samples is the number of samples and aligns with n_samples of m_X

        cv: int or sklearn.model_selection object, optional (default=None)
            The number of folds (n_splits) used in cross validation, or a Sci-Kit
            Learn model splitter, such as StratifiedKFold, ShuffleSplit, etc.  If a
            number is given, the KFold technique is used.  If the value is None,
            the rule does not get cross-validated.

        """

        explorable_vars = [col for col in m_X.columns if col != m_y.name]
        m_X = m_X[explorable_vars].copy()

        dwf = DataWhysFrame(pd.concat((DataWhysFrame(m_y), m_X), axis=1))

        self.outcome = m_y.name
        self.target = m_y.target_class

        self.rule, sample_stats, self.score, self.discarded_rules = self._run_solve(
            dwf, self.outcome, self.target
        )

        self.size = sample_stats["size"]
        self.mean = sample_stats["mean"]
        self.rule_data = self.get_rule_data(dwf)

        # adding this to store the dwf specific to this solve
        self.df = dwf

        if cv is not None:
            self.validation = utilities.cross_validate_rule(
                self.rule, m_X, m_y, cv=cv, score=self.score
            )

    def readable_rule(self):
        utilities.get_readable_rule(
            self.rule, self.score, self.size, self.outcome, self.target
        )

    def fit_predicted(
        self,
        m_X,
        m_y,
        m_y_predicted,
        predicted=False,
        max_depth=None,
        min_score=0,
        balance=False,
        balance_threshold=0.2,
    ):
        """
        Fit the Solver with the provided data but optimizing on the error between
        ground truth and the return values of any statistical model.

        Parameters
        ----------

        m_X: DataWhysFrame of shape (n_samples, n_features)
            Where n_samples is the number of samples and n_features is the number of
            features.

        m_y: DataWhysSeries of shape (n_samples,)
            Where n_samples is the number of samples and aligns with n_samples of m_X.

        m_y_predicted: DataWhysSeries, Series, or array (n_samples,), default=None
            Where n_samples is the number of samples and aligns with n_samples of m_y.
            * If provided, `m_y_predicted` will be compare against `m_y` to find a rule
            that explains differences between "correct" and "incorrect" predictions.

        predicted: Bool, optional (default=False)
            Defines the focus of the exploration. To find rules where the provided
            `m_y_predicted` is predicted or where it is not predicted.

        max_depth: Int, optional (default=None)
            Sets a maximum number of levels in to split rules and incidentally the
            subsamples defined by the rules.
            Default `None` allows maximum number of splits.

        min_score: Int, optional (default=0)
            Sets a minimum Z-score found by rules as a threshold for rejecting rules.
            If a rule is rejected, exploration down that branch will bet terminated.

        balance: Bool, optional (default=False)
            Allows the solver to create nested rules of roughly equal size in an
            effort to balance the overall size of rules. In this process, the
            Solver.min_size_frac is adjusted to allow subsequent rule size to
            match the prior rule size as much as possible while maintaining rule
            stability.

        balance_threshold: float, optional (default=0.2)
            If balance is set to True, the balance threshold allows setting how much
            of a relative difference a subsequent rules size should be with respect to
            the prior rule. This value can be as low as 0 to any multiple desired.

            Example: balance_threshold = 0.2 implies that the subsequent rule size
            should be within 20% (plus or minus) of the prior rule size

        """

        explorable_vars = [col for col in m_X.columns if col != m_y.name]
        m_X = m_X[explorable_vars].copy()

        if m_y.var_type == "discrete":
            cond = m_y_predicted == m_y
            y_error = DataWhysSeries(
                np.where(cond, "correct", "incorrect"),
                name="prediction",
                index=m_y.index,
            )
            y_error.target_class = "correct" if predicted else "incorrect"
        else:
            y_error = DataWhysSeries(
                np.abs(m_y_predicted - m_y), name="residual", index=m_y.index
            )
            y_error.target_class = "min" if predicted else "max"

        dwf = DataWhysFrame(pd.concat((DataWhysFrame(y_error), m_X), axis=1))

        self.outcome = outcome = y_error.name
        self.target = target = y_error.target_class

        min_size_frac_orig = self.min_size_frac

        self.rule_tree = dict()

        def evaluate(data, depth=0, current="IN", prior=(0, "IN")):
            def size_within_threshold(old_size, new_size, threshold=0.2):
                if old_size == 0:
                    return False
                else:
                    return np.abs(new_size / old_size - 1) <= threshold

            if all(
                (
                    data.shape[0] > 1,
                    data[outcome].unique().shape[0] > 1,
                    depth <= max_depth if max_depth is not None else depth <= 1e6,
                )
            ):
                min_size_orig = self.get_min_size_from_frac(data, outcome, target)
                (
                    self.rule,
                    sample_stats,
                    self.score,
                    self.discarded_rules,
                ) = self._run_solve(data, outcome, target)
                self.size = sample_stats["size"]
                self.mean = sample_stats["mean"]

                if self.score > min_score:
                    key = prior + (depth, current)
                    self.rule_tree[key] = {
                        "rule": self.rule,
                        "score": self.score,
                        "size": self.size,
                        "mean": self.mean,
                    }

                    rule_data = self.get_rule_data(data).copy()
                    xrule_data = self.get_rule_data(data, xrule=True).copy()

                    try:
                        if balance:
                            if size_within_threshold(
                                self.size, min_size_orig, balance_threshold
                            ):
                                self.set_min_size_frac_from_size(
                                    rule_data, outcome, target, min_size_orig
                                )
                                evaluate(rule_data, depth + 1, "IN", key)
                            else:
                                pass
                        else:
                            evaluate(rule_data, depth + 1, "IN", key)
                    except NotEnoughPointsError:
                        pass
                    try:
                        if balance:
                            if size_within_threshold(
                                self.size, min_size_orig, balance_threshold
                            ):
                                self.set_min_size_frac_from_size(
                                    xrule_data, outcome, target, min_size_orig
                                )
                                evaluate(xrule_data, depth + 1, "OUT", key)
                            else:
                                pass
                        else:
                            evaluate(xrule_data, depth + 1, "OUT", key)
                    except NotEnoughPointsError:
                        pass

        evaluate(dwf)
        self.min_size_frac = min_size_frac_orig

    def write_rule_tree(self, file_handle):
        """
        Export rule tree to json format.

        Parameters
        ----------
        file_handle: string
            Location of file to write the tree to.

        """
        if self.rule_tree:
            utilities.write_rule_tree(self.rule_tree, file_handle)
        else:
            raise ValueError("Rule Tree not yet set")

    def fit_meta(self, m_X, m_y, exp: BaseExploration):
        """
        Discover feature rules with the provided data.

        Parameters
        ----------
        m_X: DataWhysFrame of shape (n_samples, n_features)
            Where n_samples is the number of samples and n_features is the number
            of features

        m_y: DataWhysSeries of shape (n_samples,)
            Where n_samples is the number of samples and aligns with n_samples of m_X

        exp: an object that extends core.meta.BaseExploration
            The type of exploration used to discover feature rules

        """

        explorable_vars = [col for col in m_X.columns if col != m_y.name]
        m_X = m_X[explorable_vars].copy()

        dwf = DataWhysFrame(pd.concat((DataWhysFrame(m_y), m_X), axis=1))
        outcome = m_y.name

        encoder = DDTransformer(dwf)
        edf = utilities.encode_dataframe(dwf, encoder)
        outcome_encoded = encoder.original_to_encoded_column(outcome)
        exp.encode_options(dwf, outcome, encoder)

        edf, _ = utilities.sample_if_needed(edf, None, outcome_encoded)

        data = json.loads(edf.to_json(orient="records"))
        timeout = self._get_timeout(
            edf.shape[0], edf.shape[1] - 1, max_cycles=self.max_cycles
        )
        options = {
            "outcome": outcome_encoded,
            "data": data,
            "min_size_frac": self.min_size_frac,
            "timeout": timeout,
        }

        exp.explore(options)

        exp.decode_results(edf, outcome_encoded, encoder)

        rules = exp.result["rules"]
        meta_dwf = meta_utils.apply_meta_rules_to_df(rules, dwf)

        self.meta = {"rules": rules, "df": meta_dwf}

    def cross_validate(self, m_X, m_y, cv=3):
        """
        Cross validate rules against the provided data using a leave-one-out
            cross validation technique.

        Parameters
        ----------

        m_X: DataWhysFrame of shape (n_samples, n_features)
            Where n_samples is the number of samples and n_features is the
            number of features.

        m_y: DataWhysSeries of shape (n_samples,)
            Where n_samples is the number of samples and aligns with
            n_samples of m_X.

        cv: int or sklearn.model_selection object, optional (default=3)
            The number of folds (n_splits) used in cross validation, or a Sci-Kit
            Learn model splitter, such as StratifiedKFold, ShuffleSplit, etc.  If a
            number is given, the KFold technique is used.

        Returns
        -------

        scores: dict of float arrays of shape (n_splits,).  The possible keys for
            this dictionary are as follows:
            - train_scores: an array of rule scores that were learned on training sets
            - train_sizes: an array of rule sizes that were learned on training sets
            - test_scores: an array of rule scores when applied to the test set
            - test_sizes: an array of rule sizes when applied to the test set
            - validation_scores: an array of rule scores when applied to validation sets
            - validation_sizes: an array of rule sizes when applied to validation sets
            - rules: an array of rules (see solver.rule for object definition)
            - avg_loss: the mean squared error between train and test scores

        """

        def get_stats(df, rule, outcome, target):
            df_applied = utilities.apply_rule_to_df(df, rule)

            sample_stats = utilities.get_stats(df_applied, outcome, target)
            score = utilities.score_rule(df, rule, outcome, target)
            size = sample_stats["size"]

            return score, size

        if isinstance(cv, int) or isinstance(cv, float):
            cv = KFold(n_splits=cv, shuffle=True)

        explorable_vars = [col for col in m_X.columns if col != m_y.name]
        m_X = m_X[explorable_vars].copy()

        X_train, X_test, y_train, y_test = train_test_split(
            m_X, m_y, test_size=0.33, random_state=1337
        )
        y_train.target_class = y_test.target_class = m_y.target_class

        dwf = DataWhysFrame(pd.concat((DataWhysFrame(m_y), m_X), axis=1))
        dwf_test = DataWhysFrame(pd.concat((DataWhysFrame(y_test), X_test), axis=1))
        outcome = m_y.name
        target = m_y.target_class

        # For use in scoring later (_run_solve handles in-flight encoding)
        encoder = DDTransformer(dwf)
        edf_test = utilities.encode_dataframe(dwf_test, encoder)
        outcome_encoded = encoder.original_to_encoded_column(outcome)
        target_encoded = utilities.encode_value(dwf, outcome, target, encoder)

        train_scores, train_sizes = [], []
        test_scores, test_sizes = [], []
        val_scores, val_sizes = [], []
        rules = []

        for train_index, val_index in cv.split(X_train, y_train):
            X_train_curr = X_train.iloc[train_index]
            y_train_curr = y_train.iloc[train_index]

            dwf_train = DataWhysFrame(
                pd.concat((DataWhysFrame(y_train_curr), X_train_curr), axis=1)
            )

            X_val = X_train.iloc[val_index]
            y_val = y_train.iloc[val_index]

            dwf_val = DataWhysFrame(pd.concat((DataWhysFrame(y_val), X_val), axis=1))

            (
                train_rule,
                train_sample_stats,
                train_score,
                discarded_rules,
            ) = self._run_solve(dwf_train, outcome, target)
            train_size = train_sample_stats["size"]

            if m_y.var_type == "discrete":
                # Discrete Stats - operate in original space
                test_score, test_size = get_stats(dwf_test, train_rule, outcome, target)
                val_score, val_size = get_stats(dwf_val, train_rule, outcome, target)
            else:
                # Continous Stats - operate in encoded space
                train_rule_encoded = utilities.encode_rule(train_rule, encoder)
                edf_val = utilities.encode_dataframe(dwf_val, encoder)

                test_score, test_size = get_stats(
                    edf_test, train_rule_encoded, outcome_encoded, target_encoded
                )
                val_score, val_size = get_stats(
                    edf_val, train_rule_encoded, outcome_encoded, target_encoded
                )

            train_scores.append(train_score)
            train_sizes.append(train_size)
            test_scores.append(test_score)
            test_sizes.append(test_size)
            val_scores.append(val_score)
            val_sizes.append(val_size)
            rules.append(train_rule)

        mse = np.mean((np.array(train_scores) - np.array(test_scores)) ** 2)

        result = {
            "train_scores": train_scores,
            "train_sizes": train_sizes,
            "test_scores": test_scores,
            "test_sizes": test_sizes,
            "validation_scores": val_scores,
            "validation_sizes": val_sizes,
            "rules": rules,
            "avg_loss": mse,
        }

        return result

    def bias(self, vars, rule=None):
        """
        Evaluate bias along selected variables within the segment

        Calls function at datawhys.metrics._bias.bias_test with
        dataframe that was used to fit a rule

        Parameters
        ----------

        Returns
        -------
        """
        if not rule:
            rule = self.rule

        return dw.metrics.bias(self.df, vars, rule=rule)
