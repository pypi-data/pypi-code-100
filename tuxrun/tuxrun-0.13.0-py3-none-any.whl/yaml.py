# -*- coding: utf-8 -*-
# vim: set ts=4
#
# Copyright 2021-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import yaml


try:
    from yaml import CFullLoader as FullLoader  # type: ignore
except ImportError:  # pragma: no cover
    try:
        from yaml import FullLoader  # type: ignore
    except ImportError:
        from yaml import Loader as FullLoader  # type: ignore

    print("Warning: using python yaml loader")


def yaml_load(data):
    return yaml.load(data, Loader=FullLoader)
