#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json5
import os.path

CONFIG_DIR = os.path.abspath("./config")

_cache = {}


def get(name, *paths, default=None):
    conf = _cache.get(name)
    if conf is None:
        conf = load(name)
        _cache[name] = conf
    curr = conf
    for p in paths:
        curr = curr.get(p)
        if curr is None:
            break
    return default if curr is None else curr


def load(name):
    paths = [
        os.path.join(CONFIG_DIR, f"{name}.json"),
        os.path.join(CONFIG_DIR, f"{name}.json5")
    ]
    for p in paths:
        try:
            with open(p, 'r', encoding="utf8") as fp:
                return json5.load(fp)
        except FileNotFoundError:
            pass
    raise FileNotFoundError(f"No such config file: {name}")
