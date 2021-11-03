# -*- coding: utf-8 -*-

__version__ = 'v1.0.0'

"""
file util functions
"""
import os
import joblib
import numpy as np
import pandas as pd
import pyarrow
import pygsheets
import re
import simplejson as json
from pathlib import Path
from datetime import date, datetime
from util import config
from xlrd import open_workbook
from contextlib import suppress


class Pickle:
    """ pickle io class """

    @classmethod
    def save(cls, obj, fp_path):
        """ pickle save """

        joblib.dump(obj, str(fp_path))

    @classmethod
    def load(cls, fp_path):
        """ pickle load """

        return joblib.load(str(fp_path))


class Json:
    """ json io class """

    @classmethod
    def json_serial(cls, obj):
        """json serializer for objects not serializable by default json code """

        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, np.int64):
            return int(obj)
        raise TypeError("type %s not serializable" % type(obj))

    @classmethod
    def save(cls, obj, fp_path):
        """ json save """

        with open(str(fp_path), 'w', encoding='utf-8') as fp_handler:
            json.dump(obj, fp_handler, indent=2, default=cls.json_serial)
            fp_handler.close()

    @classmethod
    def load(cls, fp_path):
        """ json load """

        with open(str(fp_path), 'r', encoding='utf-8') as fp_handler:
            obj = json.load(fp_handler)
            fp_handler.close()
            return obj


class Dir:
    @classmethod
    def get_or_create(cls, fp_path):
        if isinstance(fp_path, str):
            fp_path = Path(fp_path)
        if Path.exists(fp_path):
            return fp_path
        else:
            os.mkdir(fp_path)
            return fp_path

    @classmethod
    def get_tree_size_scandir(cls, path):
        """Return total size of all regular files in directory tree at *path*."""
        size = 0
        for entry in os.scandir(path):
            with suppress(OSError):  # ignore errors for entry & its children
                if entry.is_dir(follow_symlinks=False):  # directory
                    size += cls.get_tree_size_scandir(entry)
                elif entry.is_file(follow_symlinks=False):  # regular file
                    size += entry.stat(follow_symlinks=False).st_size
        return size
