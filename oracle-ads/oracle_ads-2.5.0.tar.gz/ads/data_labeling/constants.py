#!/usr/bin/env python
# -*- coding: utf-8; -*-# Copyright (c) 2021 Oracle and/or its affiliates.

# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

class DatasetType:
    """DatasetType class which contains all the dataset
    types that data labeling service supports.
    """

    TEXT = "TEXT"
    IMAGE = "IMAGE"
    DOCUMENT = "DOCUMENT"


class AnnotationType:
    """AnnotationType class which contains all the annotation
    types that data labeling service supports.
    """

    SINGLE_LABEL = "SINGLE_LABEL"
    MULTI_LABEL = "MULTI_LABEL"
    ENTITY_EXTRACTION = "ENTITY_EXTRACTION"
    BOUNDING_BOX = "BOUNDING_BOX"
