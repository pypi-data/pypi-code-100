#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

# Default lines separator
SEP = chr(10)

# STYLES
STYLE_PGADMIN3 = "pgadmin3"

def CheckPath(path):
    """
        Create folder structure if not exists
        @param path: Path to folder
    """
    result = []
    for p in path.split("/"):
        result.append(p)
        p = "/".join(result)

        if not os.path.exists(p):
            os.mkdir(p)
