#!/usr/bin/env python
# -*- coding: utf-8; -*-# Copyright (c) 2021 Oracle and/or its affiliates.

# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

import os
from abc import abstractmethod
from typing import Dict, List, Union

from ads.data_labeling.boundingbox import BoundingBoxItem
from ads.data_labeling.constants import AnnotationType
from ads.data_labeling.interface.parser import Parser
from ads.data_labeling.ner import NERItem
from ads.data_labeling.record import Record


class EntityType:
    """Entity type class for supporting multiple types of entities."""

    GENERIC = "GENERIC"
    TEXTSELECTION = "TEXTSELECTION"
    IMAGEOBJECTSELECTION = "IMAGEOBJECTSELECTION"


class RecordParser(Parser):
    """RecordParser class which parses the labels from the record.

    Examples
    --------
    >>> from ads.data_labeling.parser.export_record_parser import SingleLabelRecordParser
    >>> from ads.data_labeling.parser.export_record_parser import MultiLabelRecordParser
    >>> from ads.data_labeling.parser.export_record_parser import NERRecordParser
    >>> from ads.data_labeling.parser.export_record_parser import BoundingBoxRecordParser
    >>> import fsspec
    >>> import json
    >>> from ads.common import auth as authutil
    >>> labels = []
    >>> with fsspec.open("/path/to/records_file.jsonl", **authutil.api_keys()) as f:
    >>>     for line in f:
    >>>         bounding_box_labels = BoundingBoxRecordParser("source_data_path").parse(json.loads(line))
    >>>         labels.append(bounding_box_labels)
    """

    def __init__(self, dataset_source_path: str) -> "RecordParser":
        """Initiates a RecordParser instance.

        Parameters
        ----------
        dataset_source_path: str
            Dataset source path.

        Returns
        -------
        RecordParser
            RecordParser instance.
        """
        self.dataset_source_path = dataset_source_path

    def parse(self, record: Dict) -> "Record":
        """Extracts the annotations from the record content, and then constructs
        and returns a Record instance which contains the file path and the labels.

        Parameters
        ----------
        record: Dict
            Content of the record from the record file.

        Returns
        -------
        Record
            Record instance which contains the file path as well as the annotations.
        """
        return Record(
            path=self.dataset_source_path + record["sourceDetails"]["path"],
            annotation=self._extract_annotations(record),
        )

    @abstractmethod
    def _extract_annotations(
        self, record: Dict
    ) -> Union[str, List[str], List[BoundingBoxItem], List[NERItem]]:
        """Extracts annotations from the record content. Each Parser class
        needs to implement this function.

        Parameters
        ----------
        record: Dict
            Content of the record from the record file.

        Returns
        -------
        Union[str, List[str], List[BoundingBoxItem], List[NERItem]]
            Label(s).
        """
        pass

    def _validate(self, record: Dict) -> None:
        """Validates the record to ensure it contains certain fields.

        Raises
        ------
        ValueError
            If record format is incorrect.
        """
        if (
            "annotations" not in record
            or not isinstance(record["annotations"], list)
            or "entities" not in record["annotations"][0]
            or not isinstance(record["annotations"][0]["entities"], list)
            or "entityType" not in record["annotations"][0]["entities"][0]
            or "labels" not in record["annotations"][0]["entities"][0]
        ):
            raise ValueError(
                "At least one of the dataset record is in the wrong format. "
                f"Use `.export()` function to export a new record file."
            )


class SingleLabelRecordParser(RecordParser):
    """SingleLabelRecordParser class which parses the label of Single label data."""

    def _extract_annotations(self, record: Dict) -> Union[str, None]:
        """Extract the labels of the single label annotation class.

        Parameters
        ----------
        record: Dict
            Content of the record from the record file.

        Returns
        -------
        Union[str, None]
            A label or None for the unlabeled record.
        """
        if "annotations" in record:
            self._validate(record)
            return record["annotations"][0]["entities"][0]["labels"][0]["label_name"]
        else:
            return None

    def _validate(self, record: Dict) -> None:
        """Validates the format of the single label record.

        Raises
        ------
        ValueError
            If record format is incorrect.
        """
        super()._validate(record)
        if record["annotations"][0]["entities"][0]["entityType"] != EntityType.GENERIC:
            raise ValueError(
                f"At least one of the dataset records contains the invalid entity type: "
                f"`{record['annotations'][0]['entities'][0]['entityType']}`. "
                f"The entity type of the Single Label annotation must be `{EntityType.GENERIC}`."
            )
        if len(record["annotations"][0]["entities"][0]["labels"]) != 1:
            raise ValueError(
                f"At least one of the dataset records contains invalid number of records: "
                f"`{len(record['annotations'][0]['entities'][0]['labels'])}`. "
                f"The Single Label annotation expects only one label for each record."
            )


class MultiLabelRecordParser(RecordParser):
    """MultiLabelRecordParser class which parses the label of Multiple label data."""

    def _extract_annotations(self, record: Dict) -> Union[List[str], None]:
        """Extract labels of the Multi label annotation class.

        Parameters
        ----------
        record: Dict
            Content of the record from the record file.

        Returns
        -------
        Union[List[str], None]
            List of labels or None for the unlabeled record.
        """
        if "annotations" in record:
            self._validate(record)
            return [
                label["label_name"]
                for label in record["annotations"][0]["entities"][0]["labels"]
            ]
        else:
            return None

    def _validate(self, record: Dict) -> None:
        """Validates the format of the multi label record.

        Raises
        ------
        ValueError
            If record format is incorrect.
        """
        super()._validate(record)
        if record["annotations"][0]["entities"][0]["entityType"] != EntityType.GENERIC:
            raise ValueError(
                f"At least one of the dataset records contains the invalid entity type: "
                f"`{record['annotations'][0]['entities'][0]['entityType']}`. "
                f"The entity type of the Multi Label annotation must be `{EntityType.GENERIC}`."
            )
        if len(record["annotations"][0]["entities"][0]["labels"]) < 1:
            raise ValueError(
                f"At least one of the dataset records contains invalid number of labels: "
                f"`{len(record['annotations'][0]['entities'][0]['labels'])}`. "
                f"The Multi Label annotation expects at least one label for each record."
            )


class NERRecordParser(RecordParser):
    """NERRecordParser class which parses the label of NER label data."""

    def _extract_annotations(self, record: Dict) -> Union[List[NERItem], None]:
        """Extracts the labels of the NER annotation class.

        Parameters
        ----------
        record: Dict
            Content of the record from the record file.

        Returns
        -------
        Union[List[NERItem], None]
            The list of NERItem objects.
        """
        if "annotations" in record:
            self._validate(record)
            items = []
            for entity in record["annotations"][0]["entities"]:
                label = entity["labels"][0]["label_name"]
                offset = entity["textSpan"]["offset"]
                length = entity["textSpan"]["length"]
                items.append(NERItem(label=label, offset=offset, length=length))
            return items
        else:
            return None

    def _validate(self, record: Dict) -> None:
        """Validates the format of the NER label record.

        Raises
        ------
        ValueError
            If record format is incorrect.
        """
        super()._validate(record)
        if (
            record["annotations"][0]["entities"][0]["entityType"]
            != EntityType.TEXTSELECTION
        ):
            raise ValueError(
                f"At least one of the dataset records contains the invalid entity type: "
                f"`{record['annotations'][0]['entities'][0]['entityType']}`. "
                f"The entity type of the Entity Extration annotation must be `{EntityType.TEXTSELECTION}`."
            )
        if os.path.splitext(record["sourceDetails"]["path"])[1].lower() != ".txt":
            raise ValueError(
                f"Invalid file type: {os.path.splitext(record['sourceDetails']['path'])[1].lower()}, must be a txt file."
            )


class BoundingBoxRecordParser(RecordParser):
    """BoundingBoxRecordParser class which parses the label of BoundingBox label data."""

    def _extract_annotations(self, record: Dict) -> Union[List[BoundingBoxItem], None]:
        """Extracts the labels of the Object Detection annotation class.

        Parameters
        ----------
        record: Dict
            Content of the record from the record file.

        Returns
        -------
        Union[List[BoundingBoxItem], None]
            The list of BoundingBoxItem objects.
        """
        if not "annotations" in record:
            return None

        self._validate(record)
        items = []
        for entity in record["annotations"][0]["entities"]:
            labels = [label["label_name"] for label in entity["labels"]]
            coords = entity["boundingPolygon"]["normalizedVertices"]
            top_left = (float(coords[0]["x"]), float(coords[0]["y"]))
            bottom_left = (float(coords[1]["x"]), float(coords[1]["y"]))
            bottom_right = (float(coords[2]["x"]), float(coords[2]["y"]))
            top_right = (float(coords[3]["x"]), float(coords[3]["y"]))
            items.append(
                BoundingBoxItem(
                    labels=labels,
                    bottom_left=bottom_left,
                    top_left=top_left,
                    top_right=top_right,
                    bottom_right=bottom_right,
                )
            )
        return items

    def _validate(self, record: Dict) -> None:
        """Validates the format of the image label record.

        Raises
        ------
        ValueError
            If record format is incorrect.
        """
        super()._validate(record)
        if (
            record["annotations"][0]["entities"][0]["entityType"]
            != EntityType.IMAGEOBJECTSELECTION
        ):
            raise ValueError(
                f"At least one of the dataset records contains the invalid entity type: "
                f"{record['annotations'][0]['entities'][0]['entityType']}. "
                f"The entity type of Object Detection annotation must be {EntityType.IMAGEOBJECTSELECTION}."
            )
        if os.path.splitext(record["sourceDetails"]["path"])[1].lower() not in [
            ".jpg",
            ".png",
            ".jpeg",
        ]:
            raise ValueError(
                f"Invalid file type: {os.path.splitext(record['sourceDetails']['path'])[1].lower()}. "
                f"Must be an image file. The supported types are jpg, png and jpeg files."
            )


class RecordParserFactory:
    """RecordParserFactory class which contains a list of registered parsers
    and allows to register new RecordParsers.

    Current parsers include:
        * SingleLabelRecordParser
        * MultiLabelRecordParser
        * NERRecordParser
        * BoundingBoxRecordParser
    """

    _parsers = {
        AnnotationType.SINGLE_LABEL: SingleLabelRecordParser,
        AnnotationType.MULTI_LABEL: MultiLabelRecordParser,
        AnnotationType.ENTITY_EXTRACTION: NERRecordParser,
        AnnotationType.BOUNDING_BOX: BoundingBoxRecordParser,
    }

    @staticmethod
    def parser(annotation_type: str, dataset_source_path: str) -> "RecordParser":
        """Gets the parser based on the annotation_type.

        Parameters
        ----------
        annotation_type: str
            Annotation type which can be SINGLE_LABEL, MULTI_LABEL, ENTITY_EXTRACTION
            and BOUNDING_BOX.
        dataset_source_path: str
            Dataset source path.

        Returns
        -------
        RecordParser
            RecordParser corresponding to the annotation type.

        Raises
        ------
        ValueError
            If annotation_type is not supported.
        """

        if not annotation_type in RecordParserFactory._parsers:
            raise ValueError(
                f"The {annotation_type} is not supported. Choose from "
                f"`{AnnotationType.SINGLE_LABEL}`, `{AnnotationType.MULTI_LABEL}`, "
                f"`{AnnotationType.ENTITY_EXTRACTION}` and `{AnnotationType.BOUNDING_BOX}`."
            )

        return RecordParserFactory._parsers[annotation_type](
            dataset_source_path=dataset_source_path
        )

    @classmethod
    def register(cls, annotation_type: str, parser) -> None:
        """Registers a new parser.

        Parameters
        ----------
        annotation_type: str
            Annotation type which can be SINGLE_LABEL, MULTI_LABEL, ENTITY_EXTRACTION
            and BOUNDING_BOX.
        parser: RecordParser
            A new Parser class to be registered.

        Returns
        -------
        None
            Nothing.
        """
        cls._parsers[annotation_type] = parser
