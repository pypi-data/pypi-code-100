#!/usr/bin/env python
# -*- coding: utf-8; -*-# Copyright (c) 2021 Oracle and/or its affiliates.

# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from dataclasses import asdict, dataclass, field
from typing import Dict, List

import pandas as pd
from ads.common.helper import Serializable


@dataclass
class Metadata(Serializable):
    """The class that representing the labeled dataset metadata.

    Attributes
    ----------
    source_path: str
        Contains information on where all the source data(image/text/document) stores.
    records_path: str
        Contains information on where records jsonl file stores.
    labels: List
        List of classes/labels for the dataset.
    dataset_name: str
        Dataset display name on the Data Labeling Service console.
    compartment_id: str
        Compartment id of the labeled dataset.
    dataset_id: str
        Dataset id.
    annotation_type: str
        Type of the labeling/annotation task. Currently supports SINGLE_LABEL,
        MULTI_LABEL, ENTITY_EXTRACTION, BOUNDING_BOX.
    dataset_type: str
        Type of the dataset. Currently supports Text and Image.
    """

    source_path: str = ""
    records_path: str = ""
    labels: List[str] = field(default_factory=list)
    dataset_name: str = ""
    compartment_id: str = ""
    dataset_id: str = ""
    annotation_type: str = ""
    dataset_type: str = ""

    def to_dict(self) -> Dict:
        """Converts to dictionary representation.

        Returns
        -------
        Dict
            The metadata in dictionary type.
        """
        return asdict(self)

    def __repr__(self):
        """Show the Metadata in yaml format."""
        return self.to_yaml()

    def to_dataframe(self) -> pd.DataFrame:
        """
        Converts the metadata to dataframe format.

        Returns
        -------
        pandas.DataFrame
            The metadata in Pandas dataframe format.
        """
        return pd.DataFrame({"": self.to_dict()})

    def _repr_html_(self):
        """Shows metadata in dataframe format."""
        return (
            self.to_dataframe().style.set_properties(**{"margin-left": "0px"}).render()
        )
