#!/usr/bin/env python
# -*- coding: utf-8; -*-

# Copyright (c) 2021 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""
The module that contains classes to read labeled datasets.

Classes
-------
    LabeledDatasetReader
        The labeled dataset reader class.
    ExportReader
        The export reader class to read labeled dataset from the export.

Examples
--------
    >>> from ads.data_labeling import LabeledDatasetReader
    >>> from ads.common import auth as authutil
    >>> ds_reader = LabeledDatasetReader.from_export(
    ...    path="oci://bucket_name@namespace/dataset_metadata.jsonl",
    ...    auth=authutil.api_keys(),
    ...    materialize=True
    ... )
    >>> ds_reader.info()
    >>> ds_reader.read()
"""

from functools import lru_cache
from typing import Any, Dict, Generator, Tuple, Union

import pandas as pd
from ads.common import auth as authutil
from ads.common.helper import Serializable
from ads.data_labeling.interface.reader import Reader
from ads.data_labeling.reader.metadata_reader import Metadata, MetadataReader
from ads.data_labeling.reader.record_reader import RecordReader


class LabeledDatasetReader:
    """The labeled dataset reader class.

    Methods
    -------
    info(self) -> Metadata
        Gets labeled dataset metadata.
    read(self, iterator: bool = False) -> Union[Generator[Any, Any, Any], pd.DataFrame]
        Reads labeled dataset.
    from_export(cls, path: str, auth: Dict = None, encoding="utf-8", materialize: bool = False) -> "LabeledDatasetReader"
        Constructs a Labeled Dataset Reader instance.

    Examples
    --------
    >>> from ads.common import auth as authutil
    >>> from ads.data_labeling import LabeledDatasetReader
    >>> ds_reader = LabeledDatasetReader.from_export(
    ...    path="oci://bucket_name@namespace/dataset_metadata.jsonl",
    ...    auth=authutil.api_keys(),
    ...    materialize=True
    ... )
    >>> ds_reader.info()
        ------------------------------------------------------------------------
        annotation_type	                                            SINGLE_LABEL
        compartment_id	                                        TEST_COMPARTMENT
        dataset_id                                                  TEST_DATASET
        dataset_name                                           test_dataset_name
        dataset_type                                                        TEXT
        labels	                                                   ['yes', 'no']
        records_path                                             path/to/records
        source_path                                              path/to/dataset

    >>> ds_reader.read()
                                Path            Content            Annotations
        ----------------------------------------------------------------------
        0   path/to/the/content/file       file content                    yes
        1   path/to/the/content/file       file content                     no
    """

    def __init__(self, reader: Reader):
        """Initializes the labeled dataset reader instance.

        Parameters
        ----------
        reader: Reader
            The Reader instance which reads and extracts the labeled dataset.
        """
        self._reader = reader

    @classmethod
    def from_export(
        cls,
        path: str,
        auth: dict = None,
        encoding: str = "utf-8",
        materialize: bool = False,
        include_unlabeled: bool = False,
    ) -> "LabeledDatasetReader":
        """Constructs Labeled Dataset Reader instance.

        Parameters
        ----------
        path: str
            The metadata file path, can be either local or object storage path.
        auth: (dict, optional). Defaults to None.
            The default authetication is set using `ads.set_auth` API. If you need to override the
            default, use the `ads.common.auth.api_keys` or `ads.common.auth.resource_principal` to create appropriate
            authentication signer and kwargs required to instantiate IdentityClient object.
        encoding: (str, optional). Defaults to 'utf-8'.
            Encoding for files.
        materialize: (bool, optional). Defaults to False.
            Whether the content of the dataset file should be loaded or it should return the file path to the content.
            By default the content will not be loaded.

        Returns
        -------
        LabeledDatasetReader
            The LabeledDatasetReader instance.
        """
        auth = auth or authutil.default_signer()

        return cls(
            reader=ExportReader(
                path=path,
                auth=auth,
                encoding=encoding,
                materialize=materialize,
                include_unlabeled=include_unlabeled,
            )
        )

    def info(self) -> Serializable:
        """Gets the labeled dataset metadata.

        Returns
        -------
        Metadata
            The labeled dataset metadata.
        """
        return self._reader.info()

    def read(
        self, iterator: bool = False
    ) -> Union[Generator[Any, Any, Any], pd.DataFrame]:
        """Reads the labeled dataset records.

        Parameters
        ----------
        iterator: (bool, optional). Defaults to False.
            True if the result should be represented as a Generator.
            Fasle if the result should be represented as a Pandas DataFrame.

        Returns
        -------
        Union[Generator[Any, Any, Any], pd.DataFrame]
            The labeled dataset.
        """
        if iterator:
            return self._reader.read()

        return pd.DataFrame(
            self._reader.read(), columns=["Path", "Content", "Annotations"]
        )


class ExportReader(Reader):
    """The ExportReader class to read labeled dataset from the export.

    Methods
    -------
    info(self) -> Metadata
        Gets the labeled dataset metadata.
    read(self) -> Generator[Tuple, Any, Any]
        Reads the labeled dataset.
    """

    def __init__(
        self,
        path: str,
        auth: Dict = None,
        encoding="utf-8",
        materialize: bool = False,
        include_unlabeled: bool = False,
    ):
        """Initializes the labeled dataset export reader instance.

        Parameters
        ----------
        path: str
            The metadata file path, can be either local or object storage path.
        auth: (dict, optional). Defaults to None.
            The default authetication is set using `ads.set_auth` API. If you need to override the
            default, use the `ads.common.auth.api_keys` or `ads.common.auth.resource_principal` to create appropriate
            authentication signer and kwargs required to instantiate IdentityClient object.
        encoding: (str, optional). Defaults to 'utf-8'.
            Encoding for files. The encoding is used to extract the metadata information
            of the labeled dataset and also to extract the content of the text dataset records.
        materialize: (bool, optional). Defaults to False.
            Whether the content of dataset files should be loaded/materialized or not.
            By default the content will not be materialized.
        include_unlabeled: (bool, optional). Defaults to False.
            Whether to load the unlabeled records or not.

        Raises
        ------
            ValueError: When path is empty or not a string.
            TypeError: When path not a string.
        """

        if not path:
            raise ValueError("The path must be specified.")

        if not isinstance(path, str):
            raise TypeError("The path must be a string.")

        self.path = path
        self.auth = auth or authutil.default_signer()
        self.encoding = encoding
        self.materialize = materialize
        self.include_unlabeled = include_unlabeled

    @lru_cache(maxsize=1)
    def info(self) -> Metadata:
        """Gets the labeled dataset metadata.

        Returns
        -------
        Metadata
            The labeled dataset metadata.
        """
        return MetadataReader.from_export_file(
            path=self.path,
            auth=self.auth,
        ).read()

    def read(self) -> Generator[Tuple, Any, Any]:
        """Reads the labeled dataset records.

        Returns
        -------
        Generator[Tuple, Any, Any]
            The labeled dataset records.
        """
        metadata = self.info()

        records_reader = RecordReader.from_export_file(
            path=metadata.records_path,
            dataset_type=metadata.dataset_type,
            annotation_type=metadata.annotation_type,
            dataset_source_path=metadata.source_path,
            auth=self.auth,
            encoding=self.encoding,
            materialize=self.materialize,
            include_unlabeled=self.include_unlabeled,
        )
        return records_reader.read()
