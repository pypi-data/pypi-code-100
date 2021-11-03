from config.core import config
from feature_engine.encoding import OrdinalEncoder
from feature_engine.selection import DropFeatures
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from model.processing import features as pp

pipe = Pipeline(
    [
        # == TEMPORAL VARIABLES ====
        (
            "Time Extraction",
            pp.DateTimeTransformer(
                reference_variable=config.model_config.ref_var,
            ),
        ),
        # == IP  Address cleaning ===
        (
            """ Categorizing the IP Addresses """,
            pp.IP_cleaning(
                variables=config.model_config.IP_vars,
            ),
        ),
        # == Flag  Address cleaning ===
        (
            """ Cleaning Flag values """,
            pp.Flag_cleaning(
                variables=config.model_config.flag_vars,
            ),
        ),
        # == Outlier Removal ===
        (
            """ Removing the Outliers """,
            pp.Outlier_removal(
                variables=config.model_config.vars_with_outlirs,
            ),
        ),
        # == To Category ===
        (
            """ Changing to Categorical """,
            pp.To_category(
                variables=config.model_config.categorical_vars,
            ),
        ),
        # == Feauture dropping ===
        ("drop_features", DropFeatures(features_to_drop=[config.model_config.ref_var])),
        # == CATEGORICAL ENCODING
        (
            """ Ordinal Encoding """,
            OrdinalEncoder(
                variables=config.model_config.categorical_vars,
            ),
        ),
        # ==Drop nan ==
        (
            "Dropnan",
            pp.Dropna(),
        ),
        # == Scaling ==
        (
            "scaler",
            StandardScaler(with_mean=False),
        ),
        # ==Drop nan ==
        (
            "Dropnan_array",
            pp.Dropna_array(),
        ),
        # == Decision Tree Classifier ==
        (
            """RandomForest""",
            RandomForestClassifier(
                oob_score=True,
                random_state=42,
                warm_start=False,
                n_jobs=-1,
                n_estimators=50,
                class_weight="balanced",
            ),
        ),
    ]
)
