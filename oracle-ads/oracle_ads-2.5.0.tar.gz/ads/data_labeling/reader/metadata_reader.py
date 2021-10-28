#!/usr/bin/env python
# -*- coding: utf-8; -*-# Copyright (c) 2021 Oracle and/or its affiliates.

# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from typing import Dict

from ads.data_labeling.interface.reader import Reader
from ads.data_labeling.metadata import Metadata
from ads.data_labeling.reader.jsonl_reader import JsonlReader
from ads.data_labeling.parser.export_metadata_parser import MetadataParser


class EmptyMetadata(Exception):
    """Empty Metadata."""

    pass


class MetadataReader:
    """MetadataReader class which reads and extracts the labeled dataset metadata.

    Examples
    --------
    >>> from ads.data_labeling import MetadataReader
    >>> import oci
    >>> import os
    >>> from ads.common import auth as authutil
    >>> reader = MetadataReader.from_export_file("metadata_export_file_path",
    ...                                 auth=authutil.api_keys())
    >>> reader.read()
    """

    def __init__(self, reader: Reader):
        """Initiate a MetadataReader instance.

        Parameters
        ----------
        reader: Reader
            Reader instance which reads and extracts the labeled dataset metadata.
        """
        self._reader = reader

    @classmethod
    def from_export_file(cls, path: str, auth: Dict = None) -> "MetadataReader":
        """Contructs a MetadataReader instance.

        Parameters
        ----------
        path: str
            metadata file path, can be either local or object storage path.
        auth: dict. Default None
            The default authetication is set using `ads.set_auth` API. If you need to override the
            default, use the `ads.common.auth.api_keys` or `ads.common.auth.resource_principal` to create appropriate
            authentication signer and kwargs required to instantiate IdentityClient object.

        Returns
        -------
        MetadataReader
            The MetadataReader instance whose reader is a ExportMetadataReader instance.
        """
        return cls(ExportMetadataReader(path=path, auth=auth))

    def read(self) -> Metadata:
        """Reads the content from the metadata file.

        Returns
        -------
        Metadata
            The metadata of the labeled dataset.
        """
        return self._reader.read()


class ExportMetadataReader(JsonlReader):
    """ExportMetadataReader class which reads the metadata jsonl file from local/object
    storage path."""

    def read(self) -> Metadata:
        """Reads the content from the metadata file.

        Returns
        -------
        Metadata
            The metadata of the labeled dataset.
        """

        try:
            return MetadataParser.parse(next(super().read()))
        except StopIteration:
            raise EmptyMetadata("Metadata file is empty.")
        except Exception as e:
            raise e
