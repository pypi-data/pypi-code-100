#!/usr/bin/env python
# -*- coding: utf-8; -*-

# Copyright (c) 2021 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class BoundingBoxItem:
    """BoundingBoxItem class representing bounding box label.

    Attributes
    ----------
    labels: List[str]
        List of labels for this bounding box.
    top_left: Tuple[float, float]
        Top left corner of this bounding box.
    bottom_left: Tuple[float, float]
        Bottom left corner of this bounding box.
    bottom_right: Tuple[float, float]
        Bottom right corner of this bounding box.
    top_right: Tuple[float, float]
        Top right corner of this bounding box.

    Examples
    --------
    >>> item = BoundingBoxItem(
    ...     labels = ['cat','dog']
    ...     bottom_left=(0.2, 0.4),
    ...     top_left=(0.2, 0.2),
    ...     top_right=(0.8, 0.2),
    ...     bottom_right=(0.8, 0.4))
    >>> item.to_yolo(categories = ['cat','dog', 'horse'])
    """

    top_left: Tuple[float, float]
    bottom_left: Tuple[float, float]
    bottom_right: Tuple[float, float]
    top_right: Tuple[float, float]
    labels: List[str] = field(default_factory=list)

    def _validate(self):
        """Validates the instance.

        Raises
        ------
        ValueError
            If the bounding box coordinate is not between [0.0, 1.0].
        """
        if (
            not self.labels
            or not isinstance(self.labels, list)
            or len(self.labels) == 0
        ):
            raise ValueError(
                "At least one of the labels is in the wrong format. "
                f"The `BoundingBoxItem` should contain a non-empty list of the labels in a string format."
            )

        if any(
            (
                not isinstance(entity, Tuple)
                or len(entity) != 2
                or not isinstance(entity[0], float)
                or not isinstance(entity[1], float)
                or not 0.0 <= entity[0] <= 1.0
                or not 0.0 <= entity[1] <= 1.0
            )
            for entity in [
                self.bottom_left,
                self.top_left,
                self.top_right,
                self.bottom_right,
            ]
        ):
            raise ValueError(
                "At least one of the bounding box items contains invalid coordinates. The bounding box coordinates must be a `Tuple` of two float numbers between [0.0, 1.0]."
            )

    def __post_init__(self):
        self._validate()

    def to_yolo(
        self, categories: List[str]
    ) -> List[Tuple[int, float, float, float, float]]:
        """Converts BoundingBoxItem to the YOLO format.

        Parameters
        ----------
        categories: List[str]
            The list of object categories in proper order for model training.
            Example: ['cat','dog','horse']

        Returns
        -------
        List[Tuple[int, float, float, float, float]]
            The list of YOLO formatted bounding boxes.

        Raises
        ------
        ValueError
            When categories list not provided.
            When categories list not matched with the labels.
        TypeError
            When categories list has a wrong format.
        """
        if not categories:
            raise ValueError(
                "The categories must be provided. Call `.info()` to find the list of categories/labels for this dataset."
            )
        if not isinstance(categories, list):
            raise TypeError("The categories must be a List[str].")
        if not set(self.labels).issubset(categories):
            raise ValueError(
                "The wrong list of categories has been provided. The categories must be the list of all unique labels of this dataset."
            )

        category_map = {k: v for v, k in enumerate(categories)}
        coords = (
            (self.top_left[0] + self.top_right[0]) / 2,
            (self.top_left[1] + self.bottom_left[1]) / 2,
            self.top_right[0] - self.top_left[0],
            self.bottom_left[1] - self.top_left[1],
        )

        return [(category_map[label],) + coords for label in self.labels]


@dataclass
class BoundingBoxItems:
    """BoundingBoxItems class which consists of a list of BoundingBoxItem.

    Attributes
    ----------
    items: List[BoundingBoxItem]
        List of BoundingBoxItem.

    Examples
    --------
    >>> item = BoundingBoxItem(
    ...     labels = ['cat','dog']
    ...     bottom_left=(0.2, 0.4),
    ...     top_left=(0.2, 0.2),
    ...     top_right=(0.8, 0.2),
    ...     bottom_right=(0.8, 0.4))
    >>> items = BoundingBoxItems(items = [item])
    >>> items.to_yolo(categories = ['cat','dog', 'horse'])
    """

    items: List[BoundingBoxItem] = field(default_factory=list)

    def __getitem__(self, index: int) -> BoundingBoxItem:
        return self.items[index]

    def to_yolo(
        self, categories: List[str]
    ) -> List[Tuple[int, float, float, float, float]]:
        """Converts BoundingBoxItems to the YOLO format.

        Parameters
        ----------
        categories: List[str]
            The list of object categories in proper order for model training.
            Example: ['cat','dog','horse']

        Returns
        -------
        List[Tuple[int, float, float, float, float]]
            The list of YOLO formatted bounding boxes.

        Raises
        ------
        ValueError
            When categories list not provided.
            When categories list not matched with the labels.
        TypeError
            When categories list has a wrong format.
        """
        if not categories:
            raise ValueError(
                "The categories must be provided. Call `.info()` method to find the list of categories/labels for this dataset."
            )
        if not isinstance(categories, list):
            raise TypeError("The categories must be a List[str].")

        result = []
        for item in self.items:
            result.extend(item.to_yolo(categories))
        return result
