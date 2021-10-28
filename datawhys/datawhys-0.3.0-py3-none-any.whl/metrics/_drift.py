from typing import Dict, Union

import numpy as np
import pandas as pd
from scipy.stats import norm
from sklearn.preprocessing import StandardScaler


def data_drift(
    model_data: Union[pd.DataFrame, pd.Series, np.ndarray],
    test_data: Union[pd.DataFrame, pd.Series, np.ndarray],
    return_components: bool = False,
) -> Dict:
    """Test if there is data drift from the data a model was train on and any
        new unseen data. The test works only for continuous, non-binary data.

        Parameters
        ----------
        model_data : pd.DataFrame, pd.Series, np.ndarray
            The data a model was used to train on. The model will have weights or
            coefficients that are tuned to this data and its underlying distribution.

        test_data : pd.DataFrame, pd.Series, np.ndarray
            The new data your model has not yet seen. This data may have a distribution
            that is significantly different from the model data and may explain
            unexpected model results.

        return_components : boolean, default=False
            For multivariate data sets, return the component for both the model data and
            test data discovered by UMAP. For univariate data sets, the same data will
            be returned.

        Returns
        -------
        test_metrics: dict
            z-score of the test,
            p-value of the test,
            confidence of the test

            if returning the components, both model and test data components
            will be returned

        Examples
        --------
        >>> mondobrain.metrics.data_drift(model_data, test_data)
        {
            "z-score": -0.7067833851248948,
            "p-value": 0.7601494493749683,
            "confidence": 0.2398505506250317
        }

        In this example, there was not signficant indication that the test data
        was different than the model data. Any unexpected results of the model
        are likely not due to data drift with a confidence of 76% in this case
        due to rejection of the null hypothesis with insignificant p-value.
    """

    import umap

    if model_data.shape[1] != test_data.shape[1]:
        raise ValueError("Model and Test data must have same number of dimensions")

    if model_data.shape[0] > 1:
        df = np.concatenate((model_data, test_data), axis=0)
        scaler = StandardScaler()
        df = scaler.fit_transform(df)
        df_model = df[: model_data.shape[0]]
        df_test = df[model_data.shape[0] :]

        embedding_train = umap.UMAP(
            n_neighbors=5, min_dist=0.0, n_components=1, random_state=42,
        ).fit_transform(df_model)

        embedding_test = umap.UMAP(
            n_neighbors=5, min_dist=0.0, n_components=1, random_state=42,
        ).fit_transform(df_test)
    else:
        embedding_train = model_data
        embedding_test = test_data

    model_mean = embedding_train.mean()
    test_mean = embedding_test.mean()
    model_std = embedding_train.std()
    test_sqrt_n = np.sqrt(embedding_test.shape[0])

    z_score = test_sqrt_n * (test_mean - model_mean) / model_std
    p = norm.sf(z_score)
    confidence = 1 - p

    return_package = {"z_score": z_score, "p-value": p, "confidence": confidence}

    if return_components:
        return_package["components"] = {
            "model": embedding_train.tolist(),
            "test": embedding_test.tolist(),
        }

    return return_package
