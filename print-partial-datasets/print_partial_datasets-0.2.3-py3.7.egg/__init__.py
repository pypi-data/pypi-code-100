"""Top-level package for print_partial_datasets."""

__author__ = """Evan C Edmond"""
__email__ = "eedmond@gmail.com"
__version__ = '0.2.3'

from pathlib import Path

import pandas as pd
from fsl.utils.filetree import FileTree, FileTreeQuery

from .filetreemanager import (FileGroup, genColumns, genFileGroups,
                              prepareFixed, prepareVaryings)


def print_partial_datasets(datadir, filetree, short_name, variables, **kwargs):
    """Search a structured data directory using a ``FileTree``, producing a table
    of complete and partial datasets. Have a look at the filetree documentation to
    see how to specify a tree, including short_name and variables.

    https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.utils.filetree.html

    :arg datadir:       Path to data directory
    :arg filetree:      Path to .tree file. You can specify your own, or use the default
                        trees in fslpy, e.g. "bids_raw", "HCP_directory"
    :arg short_name:    A list of short names from file tree that will be searched for.
                        e.g. raw_T1, raw_bold.
    :arg variables:     A list of variable fields - a subset of those specified in
                        the file tree e.g. participant, session, run

    Additional keyword arguments (kwarg=["value1", "value2"]) can be passed to
    specify a subset of values for a given variable, the default behaviour is to allow
    all values found in the directory.
    """

    # Get FileTree object, and run FileTreeQuery
    tree = FileTree.read(filetree, Path(datadir))
    query = FileTreeQuery(tree)
    queryvars = query.variables().keys()

    # Prep variables for which all values are allowed
    _varyings = {}
    for x in variables:
        _varyings[x] = "*"
    varyings = prepareVaryings(query, short_name, _varyings)

    # Add variables for which value is specified
    for key, val in kwargs.items():
        if key in queryvars:
            varyings[key] = val

    # Remaining keys in query are fixed
    _fixed = [x for x in queryvars if x not in varyings.keys()]

    # Use FileTreeManager functions to prepare table
    fixed = prepareFixed(query, short_name, _fixed)
    varcols, fixedcols = genColumns(short_name, varyings, fixed)
    filegroups = genFileGroups(query, varyings, fixedcols)

    # Make column heading stub
    fixedcol_stub = [col[0] for col in fixedcols]

    # Map file present to x in table - consider adding other functions in future?
    x_file_present = lambda f: "x" if f is not None else " "

    # Separate complete and partial datasets (will miss empty datasets that *should*
    # be there, but this is not possible to know from file tree...
    complete = []
    partial = []
    for fg in filegroups:
        table_row = [x_file_present(f) for f in fg.files]
        if all(fg.files):
            complete.append(list(fg.varyings.values()) + table_row)
        elif any(fg.files):
            partial.append(list(fg.varyings.values()) + table_row)

    def print_table(headers, contents):
        format_row = ["{:>" + str(len(h) + 4) + "}" for h in headers]
        format_row = "".join(format_row)
        print(format_row.format(*headers))
        divider = "─" * len(format_row.format(*headers))
        print(divider)
        for row in contents:
            print(format_row.format(*row))
            print(divider)

    headers = varcols + fixedcol_stub
    print("Complete datasets")
    print_table(headers, complete)
    print("Partial datasets")
    print_table(headers, partial)

    alldata = complete + partial
    return pd.DataFrame(alldata, columns=headers)
