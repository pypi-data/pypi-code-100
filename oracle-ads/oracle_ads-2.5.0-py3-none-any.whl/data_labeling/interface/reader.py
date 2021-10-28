#!/usr/bin/env python
# -*- coding: utf-8; -*-

# Copyright (c) 2021 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from abc import ABC, abstractmethod
from typing import Any
from ads.common.helper import Serializable


class Reader(ABC):
    """Data Reader Interface."""

    def info(self) -> Serializable:
        raise NotImplementedError("The `info` method is not implemented.")

    @abstractmethod
    def read(self) -> Any:
        pass
