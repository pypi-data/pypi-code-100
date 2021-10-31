# coding=utf-8
import os
import configparser
from distutils.util import strtobool
from pkg_resources import resource_string, resource_filename

__all__ = [
    "configurable",
    "imaging",
    "lexical_discrete_choice",
    "lexical_relevance",
    "node",
    "parameter_node",
    "reparameterization",
    "trainable_node",
    "trainer",
    "transition_system",
    "worker_node",
]

MODELS_CONFIGURATIONS = configparser.ConfigParser()
MODELS_CONFIGURATIONS.read_string(
    resource_string("mammut.resources", "models.ini").decode("utf-8")
)
MODELS_CONFIGURATIONS.read(["data/models.ini", "models.ini"])
MODELS_CONFIGURATIONS_FILE_NAME = resource_filename("mammut.resources", "models.ini")
if os.path.exists("data/models.ini"):
    MODELS_CONFIGURATIONS_FILE_NAME = "data/models.ini"
if os.path.exists("models.ini"):
    MODELS_CONFIGURATIONS_FILE_NAME = "models.ini"

NGRAM_VIEWER_SMOOTHING = MODELS_CONFIGURATIONS["NGRAM_VIEWER"]["smoothing"]
NGRAM_VIEWER_YEAR_START = int(MODELS_CONFIGURATIONS["NGRAM_VIEWER"]["year_start"])
NGRAM_VIEWER_YEAR_END = int(MODELS_CONFIGURATIONS["NGRAM_VIEWER"]["year_end"])
NGRAM_VIEWER_CASE_INSENSITIVE = strtobool(
    MODELS_CONFIGURATIONS["NGRAM_VIEWER"]["case_insensitive"]
)
LEXICAL_RELEVANCE_INDEX_ESTIMATOR_USAGE_SOURCE = MODELS_CONFIGURATIONS[
    "LEXICAL_RELEVANCE_INDEX_ESTIMATOR"
]["usage_source"]
LEXICAL_RELEVANCE_INDEX_ESTIMATOR_CONSOLIDATE_STATS = strtobool(
    MODELS_CONFIGURATIONS["LEXICAL_RELEVANCE_INDEX_ESTIMATOR"]["consolidate_stats"]
)
LEXICAL_RELEVANCE_INDEX_ESTIMATOR_AUMENTATION = int(
    MODELS_CONFIGURATIONS["LEXICAL_RELEVANCE_INDEX_ESTIMATOR"]["aumentation"]
)

DISTRIBUTED_TRAINING = strtobool(MODELS_CONFIGURATIONS["TRAINING"]["distributed"])
