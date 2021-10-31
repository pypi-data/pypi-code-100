# coding=utf-8
import os
import configparser
from distutils.util import strtobool
from pkg_resources import resource_string

__all__ = [
    "annotations",
    "annotations_validator",
    "basic_tokenizer",
    "corpus",
    "corpus_transformer",
    "google_api",
    "indexer",
    "lexicon",
    "mammutGraph",
    "mammut_api",
    "ngram",
    "package",
    "simulator",
    "ssh_commands",
    "storage",
    "universal_dependencies",
    "util",
]

FEATURES_CONFIGURATIONS = configparser.ConfigParser()
FEATURES_CONFIGURATIONS.read_string(
    resource_string("mammut.resources", "features.ini").decode("utf-8")
)
FEATURES_CONFIGURATIONS.read(["data/features.ini", "features.ini"])

WORD_LEXICAL_RELEVANCE_INDEX_ESTIMATOR_ADD_NEW_SAMPLE = strtobool(
    FEATURES_CONFIGURATIONS["BASIC_TOKENIZER"][
        "word_lexical_relevance_index_estimator_add_new_sample"
    ]
)
GOOGLE_API_AUTH_LOCAL_WEBSERVER = strtobool(
    FEATURES_CONFIGURATIONS["GOOGLE_API"]["auth_local_webserver"]
)
if os.environ.get("GOOGLE_API_AUTH_LOCAL_CREDENTIAL") is not None:
    GOOGLE_API_AUTH_LOCAL_CREDENTIAL = strtobool(
        os.environ.get("GOOGLE_API_AUTH_LOCAL_CREDENTIAL")
    )
else:
    GOOGLE_API_AUTH_LOCAL_CREDENTIAL = strtobool(
        FEATURES_CONFIGURATIONS["GOOGLE_API"]["auth_local_credential"]
    )

global_request_timeout = float(
    FEATURES_CONFIGURATIONS["INDEXING"]["global_request_timeout"]
)
index_creation_timeout = FEATURES_CONFIGURATIONS["INDEXING"]["index_creation_timeout"]
index_definition_timeout = FEATURES_CONFIGURATIONS["INDEXING"][
    "index_definition_timeout"
]
index_lemma_timeout = FEATURES_CONFIGURATIONS["INDEXING"]["index_lemma_timeout"]
