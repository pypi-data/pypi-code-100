#!/usr/bin/env python
# code from fsleyes.controls.filetreemanager
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
#FSLeyes
#
#Copyright 2016-2020 University of Oxford, Oxford, UK.
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

import collections
import itertools as it


class FileGroup(object):
    """A ``FileGroup`` represents a single row in the file tree panel list.  It
    encapsulates a set of values for all varying variables, and a set of files
    and their associated fixed variable values. These are all accessible as
    attributes called ``varyings``, ``files``, and ``fixedvars``.

    Another attribute, ``fileIDs``, contains a unique ID for each file within
    one ``FileGroup``. This ID can be used to pair up files from different
    ``FileGroup`` objects.
    """


    def __init__(self, varyings, fixed, ftypes, files):
        """Create a ``FileGroup``.

        :arg varyings: Dict of ``{ var : val }`` mappings containing the
                       varying variable values.

        :arg fixed:    List containing ``{ var : val }`` mappings, each
                       containing the fixed variable values for each file.

        :arg ftypes:   List containing the file type for each file.

        :arg files:    List of file names, the same length as ``fixedvars``.
                       Missing files are represented as ``None``.
        """

        self.varyings = varyings
        self.fixed    = fixed
        self.ftypes   = ftypes
        self.files    = files
        self.fileIDs  = []

        # Generate an ID which uniquely identifies
        # each overlay by file type and fixed
        # variable values (i.e. a unique ID for each
        # row . This will be used as
        # the overlay name
        for fname, ftype, v in zip(files, ftypes, fixed):

            # The FileGroup may contain
            # non-existent files, and
            # we don't want to load files
            # that are already in the
            # overlay list
            if fname is None:
                self.fileIDs.append(None)
                continue

            if len(v) == 0:
                fid = ftype
            else:
                fid = ftype + '[' + ','.join(
                    ['{}={}'.format(var, val)
                     for var, val in sorted(v.items())]) + ']'

            self.fileIDs.append(fid)


    def __str__(self):
        """Return a string representation of this ``FileGroup``. """
        return 'FileGroup({}, {}, {}, {})'.format(self.varyings,
                                                  self.fixed,
                                                  self.ftypes,
                                                  self.files)


    def __repr__(self):
        """Return a string representation of this ``FileGroup``. """
        return str(self)


    def __eq__(self, other):
        """Return ``True`` if this ``FileGroup`` is equal to ``other``. """
        return (self.varyings == other.varyings and
                self.fixed    == other.fixed    and
                self.ftypes   == other.ftypes   and
                self.files    == other.files)


def prepareVaryings(query, ftypes, varyings):
    """Called by :meth:`FileTreeManager.update`. Prepares a dictionary which
    contains all possible values for each varying variable.

    :arg query:    :class:`.FileTreeQuery` object

    :arg ftypes:   List of file types to be displayed.

    :arg varyings: Dict of ``{ var : value }`` mappings. A value of ``'*'``
                   indicates that all possible values for this variable
                   should be used.

    :returns:      A dict of ``{ var : [value] }`` mappings, containing
                   every possible value for each varying variable.
    """

    allvars = query.variables()

    # Force a constsient ordering
    # of the varying variables
    _varyings = collections.OrderedDict()
    for var in sorted(varyings.keys()):
        _varyings[var] = varyings[var]
    varyings = _varyings

    # Expand the varying dict so that
    # it contains { var : [value] }
    # mappings - '*' is replaced with
    # a list of all possible values,
    # and a scalar value is replaced
    # with a list containing just that
    # value.
    for var, val in list(varyings.items()):

        # This variable is not relevant for
        # any of the specified file types.
        if not any([var in query.variables(ft) for ft in ftypes]):
            varyings.pop(var)
            continue

        elif val == '*': varyings[var] = allvars[var]
        else:            varyings[var] = [val]

    return varyings


def prepareFixed(query, ftypes, fixed):
    """Called by :meth:`.FileTreeManager.update`. Prepares a dictionary
    which contains all possible values for each fixed variable, and for
    each file type.

    :arg query:  :class:`.FileTreeQuery` object

    :arg ftypes: List of file types to be displayed

    :arg fixed:  List of fixed variables

    :returns:    A dict of ``{ ftype : { var : [value] } }`` mappings
                 which, for each file type, contains a dictionary of
                 all fixed variables and their possible values.
    """

    allvars = query.variables()

    # Create a dict for each file type
    # containing { var : [value] }
    # mappings for all fixed variables
    # which are relevant to that file
    # type.
    _fixed = {}
    for ftype in ftypes:
        ftvars        = query.variables(ftype)
        _fixed[ftype] = {}
        for var in fixed:
            if var in ftvars:
                _fixed[ftype][var] = allvars[var]
    fixed = _fixed

    return fixed


def genColumns(ftypes, varyings, fixed):
    """Determines all columns which need to be present in a file tree grid
    for the given file types, varying and fixed variables.

    :arg ftypes:   List of file types to be displayed

    :arg varyings: Dict of ``{ var : [value} }`` mappings, containing all
                   varying variables and their possible values (see
                   :func:`prepareVaryings`).

    :arg fixed:    Dict of ``{ ftype : { var : [value] } }`` mappings
                   which, for each file type, contains a dictionary of
                   all fixed variables and their possible values.

    :returns:      Two lists which, combined, represent all columns to be
                   displayed in the file tree grid:

                    - A list of varying variable names
                    - A list of tuples, with each tuple containing:

                      - A file type
                      - A dict of ``{var : value}`` mappings, containing
                        fixed variable values
    """

    varcols   = [var for var, vals in varyings.items()]
    fixedcols = []

    for ftype in ftypes:

        ftvars    = fixed[ftype]
        ftvarprod = list(it.product(*[vals for vals in ftvars.values()]))

        for ftvals in ftvarprod:
            ftvals = {var : val for var, val in zip(ftvars, ftvals)}
            fixedcols.append((ftype, ftvals))

    return varcols, fixedcols


def genFileGroups(query, varyings, fixed):
    """Generates a list of :class:`FileGroup` objects, each representing one
    row in a grid defined by the given set of varying and fixed variables.

    :arg query:    :class:`.FileTreeQuery` object

    :arg varyings: Dict of ``{ var : [value} }`` mappings, containing all
                   varying variables and their possible values (see
                   :func:`prepareVaryings`).

    :arg fixed:    List of tuples of ``(ftype, { var : value })`` mappings,
                   which each contain a file type and set of fixed variables
                   corresponding to one column in the grid.

    :returns:      A list of ``FileGroup`` objects.
    """

    if len(varyings) == 0:
        return []

    # Build a list of file groups - each
    # file group represents a group of
    # files to be displayed together,
    # corresponding to a combination of
    # varying values
    filegroups = []

    # loop through all possible
    # combinations of varying values
    for vals in it.product(*varyings.values()):

        groupVars   = {var : val for var, val in zip(varyings.keys(), vals)}
        groupFtypes = []
        groupFixed  = []
        groupFiles  = []

        for ftype, ftvars in fixed:

            fname = query.query(ftype, **groupVars, **ftvars)

            # There should only be one file for
            # each combination of varying+fixed
            # values
            if len(fname) == 1: fname = fname[0].filename
            else:               fname = None

            groupFtypes.append(ftype)
            groupFixed .append(ftvars)
            groupFiles .append(fname)

        grp = FileGroup(groupVars, groupFixed, groupFtypes, groupFiles)
        filegroups.append(grp)

    return filegroups
