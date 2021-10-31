#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#    Wisteria Copyright (C) 2021 suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of Wisteria.
#    Wisteria is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Wisteria is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Wisteria.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
    Wisteria project : wisteria/serializers.py

    All known serializers are defined here, in the SERIALIZERS dict. Each serializer
    has its own serializer_xxx function.
    A reference to each module imported is added in the MODULES dict.

    ___________________________________________________________________________

    o  _len(obj)
    o  serializer_iaswn(action="serialize", obj=None, fingerprint="")
    o  serializer_json(action="serialize", obj=None, fingerprint="")
    o  serializer_jsonpickle(action="serialize", obj=None, fingerprint="")
    o  serializer_jsonpickle_keystrue(action="serialize", obj=None, fingerprint="")
    o  serializer_marshal(action="serialize", obj=None, fingerprint="")
    o  serializer_pickle(action="serialize", obj=None, fingerprint="")
    o  serializer_pyyaml(action="serialize", obj=None, fingerprint="")
    o  serializer_yajl(action="serialize", obj=None, fingerprint="")

    o  init_serializers()
"""
#   pylint: disable = wrong-import-position

import sys
import timeit

import wisteria.globs

if wisteria.globs.PLATFORM_SYSTEM == "Windows":
    # We have to import 'os' only for Windows systems, hence the useless
    # remark from Pylint when Pylint is used on non-Windows systems.
    #   pylint: disable=unused-import
    import os
    # We have to import 'WMI' only for Windows systems, hence the useless
    # remark from Pylint when Pylint is used on non-Windows systems.
    #   pylint: disable=import-error
    from wmi import WMI
else:
    # We have to import 'resource' only for non-Windows systems, hence the useless
    # remark from Pylint when Pylint is used on Windows systems.
    #   pylint: disable=import-error
    import resource

# MEMOVERUSE# --memoveruse C++ module:
# MEMOVERUSEimport cppyy

from wisteria.globs import TIMEITNUMBER, MODULES
from wisteria.globs import VERBOSITY_DEBUG, VERBOSITY_DETAILS
from wisteria.wisteriaerror import WisteriaError
from wisteria.utils import trytoimport
from wisteria.serializers_classes import SerializerData, SerializationResult
from wisteria.msg import msgdebug, msginfo

# MEMOVERUSE# --memoveruse C++ module:
# MEMOVERUSEcppyy.include("memoveruse_cpp/memoveruse_cpp.h")
# MEMOVERUSEcppyy.load_library("memoveruse_cpp/libmemoveruse_cpp")
# MEMOVERUSE#    pylint: disable=import-error,wrong-import-position,wrong-import-order
# MEMOVERUSE#    about noqa: https://pep8.readthedocs.io/en/latest/intro.html#configuration
# MEMOVERUSEfrom cppyy.gbl import MemOverUse  # noqa


def _len(obj):
    """
        _len()

        Return the length of <obj>

        _______________________________________________________________________

        ARGUMENT: (bytes|str)<obj>

        RETURNED VALUE: the length of <obj>
    """
    if isinstance(obj, str):
        return len(bytes(obj, "utf-8"))
    return len(obj)


def win_memory():
    """
        win_memory()

        Compute using WMI the quantity of memory used by the current process.

        _______________________________________________________________________

        RETURNED VALUE: (int)the number of bytes used by the current process.
    """
    wmi = WMI('.')
    result = wmi.query(
        "SELECT WorkingSet "
        f"FROM Win32_PerfRawData_PerfProc_Process WHERE IDProcess={os.getpid()}")
    res = int(result[0].WorkingSet)
    return res


def serializer_iaswn(action="serialize",
                     obj=None,
                     fingerprint="",
                     works_as_expected=None):
    """
        serializer_iaswn()

        Serializer for the Iaswn module.

        Like every serializer_xxx() function:
        * this function may return (action='version') the version of the concerned module.
        * this function may try (action='serialize') to encode/decode an <obj>ect.
        * if the serializer raises an error, this error is silently converted and no exception
          is raised. If an internal error happpens, a WisteriaError exception is raised.

        This function assumes that the concerned module has already be imported.

        _______________________________________________________________________

        ARGUMENTS:
        o  action           : (str) either "version" either "serialize"
        o  obj              : the object to be serialized
        o  fingerprint      : a string describing the operation (usefull to debug)
        o  works_as_expected: (None or callable)if not None, will be called to check
                              the reversibility of the de-serialized object.

        RETURNED VALUE:
           - None if an error occcured
           - if <action> is (str)"version", return a string.
           - if <action> is (str)"serialize", return a SerializationResult object.
    """
    module = MODULES["iaswn"]

    # -------------------
    # action == "version"
    # -------------------
    if action == "version":
        return module.__version__

    # ---------------------
    # action == "serialize"
    # ---------------------
    if action != "serialize":
        raise WisteriaError(f"(ERRORID030) Unknown 'action' keyword '{action}'.")

    # MEMOVERUSE# ---- --memoveruse ? -----------------------------------------------------
    # MEMOVERUSEif 'Python' in wisteria.globs.ARGS.memoveruse:
    # MEMOVERUSE    #   pylint: disable=possibly-unused-variable
    # MEMOVERUSE    dumbstr = "0123456789"*100000
    # MEMOVERUSEif 'C++' in wisteria.globs.ARGS.memoveruse:
    # MEMOVERUSE    MemOverUse().memoveruse()

    # ---- main computation ---------------------------------------------------
    res = SerializationResult()

    if wisteria.globs.PLATFORM_SYSTEM == "Windows":
        mem0 = win_memory()
    else:
        mem0 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    _error = False
    try:
        _res = module.encode(obj)
        _timeit = timeit.Timer('module.encode(obj)',
                               globals=locals())
        res.encoding_success = True
        res.encoding_strlen = _len(_res)
        res.encoding_time = _timeit.timeit(TIMEITNUMBER)

        if wisteria.globs.ARGS.verbosity >= VERBOSITY_DETAILS:
            msginfo(f"([{fingerprint}] '{module.__name__}' / '{type(obj)}') "
                    f"encoded string='{_res}'")

    except module.IaswnError as error:
        if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
            msgdebug(f"[{fingerprint}] '{module}': encoding failed ({error})")
        _error = True

    if not _error:
        try:
            _res2 = module.decode(_res)
            res.decoding_success = True
            _timeit = timeit.Timer("module.decode(_res)",
                                   globals=locals())
            res.decoding_time = _timeit.timeit(TIMEITNUMBER)

            if obj == _res2:
                res.reversibility = True
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"[{fingerprint}] res.reversibility (first part:obj == _res2) "
                         f"is {res.reversibility}")
            if res.reversibility and works_as_expected:
                res.reversibility = res.reversibility and works_as_expected(obj=_res2)
                if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                    msgdebug(f"[{fingerprint}] res.reversibility "
                             f"(second part:works_as_expected(_res2)) "
                             f"is {res.reversibility}.")

        except module.IaswnError as error:
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"[{fingerprint}] '{module}': decoding failed ({error})")
            res = None

    if res is not None and res.reversibility is True:
        if wisteria.globs.PLATFORM_SYSTEM == "Windows":
            res.mem_usage = win_memory() - mem0
        else:
            res.mem_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - mem0

    return res


def serializer_json(action="serialize",
                    obj=None,
                    fingerprint="",
                    works_as_expected=None):
    """
        serializer_json()

        Serializer for the json module.

        Like every serializer_xxx() function:
        * this function may return (action='version') the version of the concerned module.
        * this function may try (action='serialize') to encode/decode an <obj>ect.
        * if the serializer raises an error, this error is silently converted and no exception
          is raised. If an internal error happpens, a WisteriaError exception is raised.

        This function assumes that the concerned module has already be imported.

        _______________________________________________________________________

        ARGUMENTS:
        o  action           : (str) either "version" either "serialize"
        o  obj              : the object to be serialized
        o  fingerprint      : a string describing the operation (usefull to debug)
        o  works_as_expected: (None or callable)if not None, will be called to check
                              the reversibility of the de-serialized object.

        RETURNED VALUE:
           - None if an error occcured
           - if <action> is (str)"version", return a string.
           - if <action> is (str)"serialize", return a SerializationResult object.
    """
    module = MODULES["json"]

    # -------------------
    # action == "version"
    # -------------------
    if action == "version":
        return module.__version__

    # ---------------------
    # action == "serialize"
    # ---------------------
    if action != "serialize":
        raise WisteriaError(f"(ERRORID031) Unknown 'action' keyword '{action}'.")

    # MEMOVERUSE# ---- --memoveruse ? -----------------------------------------------------
    # MEMOVERUSEif 'Python' in wisteria.globs.ARGS.memoveruse:
    # MEMOVERUSE    #   pylint: disable=possibly-unused-variable
    # MEMOVERUSE    dumbstr = "0123456789"*100000
    # MEMOVERUSEif 'C++' in wisteria.globs.ARGS.memoveruse:
    # MEMOVERUSE    MemOverUse().memoveruse()

    # ---- main computation ---------------------------------------------------
    res = SerializationResult()

    if wisteria.globs.PLATFORM_SYSTEM == "Windows":
        mem0 = win_memory()
    else:
        mem0 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    _error = False
    try:
        _res = module.dumps(obj)
        _timeit = timeit.Timer('module.dumps(obj)',
                               globals=locals())
        res.encoding_success = True
        res.encoding_strlen = _len(_res)
        res.encoding_time = _timeit.timeit(TIMEITNUMBER)

        if wisteria.globs.ARGS.verbosity >= VERBOSITY_DETAILS:
            msginfo(f"([{fingerprint}] '{module.__name__}' / '{type(obj)}') "
                    f"encoded string='{_res}'")

    except TypeError as error:
        if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
            msgdebug(f"[{fingerprint}] '{module}': encoding failed ({error})")
        _error = True

    if not _error:
        try:
            _res2 = module.loads(_res)
            res.decoding_success = True
            _timeit = timeit.Timer("module.loads(_res)",
                                   globals=locals())
            res.decoding_time = _timeit.timeit(TIMEITNUMBER)

            if obj == _res2:
                res.reversibility = True
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"[{fingerprint}] res.reversibility (first part:obj == _res2) "
                         f"is {res.reversibility}")
            if res.reversibility and works_as_expected:
                res.reversibility = res.reversibility and works_as_expected(obj=_res2)
                if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                    msgdebug(f"[{fingerprint}] res.reversibility "
                             f"(second part:works_as_expected(_res2)) "
                             f"is {res.reversibility}.")

        except (TypeError, AttributeError) as error:
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"[{fingerprint}] '{module}': decoding failed ({error})")
            res = None

    if res is not None and res.reversibility is True:
        if wisteria.globs.PLATFORM_SYSTEM == "Windows":
            res.mem_usage = win_memory() - mem0
        else:
            res.mem_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - mem0

    return res


def serializer_jsonpickle(action="serialize",
                          obj=None,
                          fingerprint="",
                          works_as_expected=None):
    """
        serializer_jsonpickle()

        Serializer for the jsonpickle module.

        Like every serializer_xxx() function:
        * this function may return (action='version') the version of the concerned module.
        * this function may try (action='serialize') to encode/decode an <obj>ect.
        * if the serializer raises an error, this error is silently converted and no exception
          is raised. If an internal error happpens, a WisteriaError exception is raised.

        This function assumes that the concerned module has already be imported.

        _______________________________________________________________________

        ARGUMENTS:
        o  action           : (str) either "version" either "serialize"
        o  obj              : the object to be serialized
        o  fingerprint      : a string describing the operation (usefull to debug)
        o  works_as_expected: (None or callable)if not None, will be called to check
                              the reversibility of the de-serialized object.

        RETURNED VALUE:
           - None if an error occcured
           - if <action> is (str)"version", return a string.
           - if <action> is (str)"serialize", return a SerializationResult object.
    """
    module = MODULES["jsonpickle"]

    # -------------------
    # action == "version"
    # -------------------
    if action == "version":
        return module.__version__

    # ---------------------
    # action == "serialize"
    # ---------------------
    if action != "serialize":
        raise WisteriaError(f"(ERRORID032) Unknown 'action' keyword '{action}'.")

    # MEMOVERUSE# ---- --memoveruse ? -----------------------------------------------------
    # MEMOVERUSEif 'Python' in wisteria.globs.ARGS.memoveruse:
    # MEMOVERUSE    #   pylint: disable=possibly-unused-variable
    # MEMOVERUSE    dumbstr = "0123456789"*100000
    # MEMOVERUSEif 'C++' in wisteria.globs.ARGS.memoveruse:
    # MEMOVERUSE    MemOverUse().memoveruse()

    # ---- main computation ---------------------------------------------------
    res = SerializationResult()

    if wisteria.globs.PLATFORM_SYSTEM == "Windows":
        mem0 = win_memory()
    else:
        mem0 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    _error = False
    try:
        _res = module.dumps(obj)
        _timeit = timeit.Timer('module.dumps(obj)',
                               globals=locals())
        res.encoding_success = True
        res.encoding_strlen = _len(_res)
        res.encoding_time = _timeit.timeit(TIMEITNUMBER)

        if wisteria.globs.ARGS.verbosity >= VERBOSITY_DETAILS:
            msginfo(f"([{fingerprint}] '{module.__name__}' / '{type(obj)}') "
                    f"encoded string='{_res}'")

    except TypeError as error:
        if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
            msgdebug(f"[{fingerprint}] '{module}': encoding failed ({error})")
        _error = True

    if not _error:
        try:
            _res2 = module.loads(_res)
            res.decoding_success = True
            _timeit = timeit.Timer("module.loads(_res)",
                                   globals=locals())
            res.decoding_time = _timeit.timeit(TIMEITNUMBER)

            if obj == _res2:
                res.reversibility = True
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"[{fingerprint}] res.reversibility (first part:obj == _res2) "
                         f"is {res.reversibility}")
            if res.reversibility and works_as_expected:
                res.reversibility = res.reversibility and works_as_expected(obj=_res2)
                if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                    msgdebug(f"[{fingerprint}] res.reversibility "
                             f"(second part:works_as_expected(_res2)) "
                             f"is {res.reversibility}.")

        except (TypeError, AttributeError) as error:
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"[{fingerprint}] '{module}': decoding failed ({error})")
            res = None

    if res is not None and res.reversibility is True:
        if wisteria.globs.PLATFORM_SYSTEM == "Windows":
            res.mem_usage = win_memory() - mem0
        else:
            res.mem_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - mem0

    return res


def serializer_jsonpickle_keystrue(action="serialize",
                                   obj=None,
                                   fingerprint="",
                                   works_as_expected=None):
    """
        serializer_jsonpickle_keystrue()

        Serializer for the jsonpickle module (keys=True).

        Like every serializer_xxx() function:
        * this function may return (action='version') the version of the concerned module.
        * this function may try (action='serialize') to encode/decode an <obj>ect.
        * if the serializer raises an error, this error is silently converted and no exception
          is raised. If an internal error happpens, a WisteriaError exception is raised.

        This function assumes that the concerned module has already be imported.

        _______________________________________________________________________

        ARGUMENTS:
        o  action           : (str) either "version" either "serialize"
        o  obj              : the object to be serialized
        o  fingerprint      : a string describing the operation (usefull to debug)
        o  works_as_expected: (None or callable)if not None, will be called to check
                              the reversibility of the de-serialized object.

        RETURNED VALUE:
           - None if an error occcured
           - if <action> is (str)"version", return a string.
           - if <action> is (str)"serialize", return a SerializationResult object.
    """
    module = MODULES["jsonpickle"]

    # -------------------
    # action == "version"
    # -------------------
    if action == "version":
        return module.__version__

    # ---------------------
    # action == "serialize"
    # ---------------------
    if action != "serialize":
        raise WisteriaError(f"(ERRORID042) Unknown 'action' keyword '{action}'.")

    # MEMOVERUSE# ---- --memoveruse ? -----------------------------------------------------
    # MEMOVERUSEif 'Python' in wisteria.globs.ARGS.memoveruse:
    # MEMOVERUSE    #   pylint: disable=possibly-unused-variable
    # MEMOVERUSE    dumbstr = "0123456789"*100000
    # MEMOVERUSEif 'C++' in wisteria.globs.ARGS.memoveruse:
    # MEMOVERUSE    MemOverUse().memoveruse()

    # ---- main computation ---------------------------------------------------
    res = SerializationResult()

    if wisteria.globs.PLATFORM_SYSTEM == "Windows":
        mem0 = win_memory()
    else:
        mem0 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    _error = False
    try:
        _res = module.dumps(obj, keys=True)
        _timeit = timeit.Timer('module.dumps(obj, keys=True)',
                               globals=locals())
        res.encoding_success = True
        res.encoding_strlen = _len(_res)
        res.encoding_time = _timeit.timeit(TIMEITNUMBER)

        if wisteria.globs.ARGS.verbosity >= VERBOSITY_DETAILS:
            msginfo(f"([{fingerprint}] '{module.__name__}' / '{type(obj)}') "
                    f"encoded string='{_res}'")

    except TypeError as error:
        if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
            msgdebug(f"[{fingerprint}] '{module}': encoding failed ({error})")
        _error = True

    if not _error:
        try:
            _res2 = module.loads(_res, keys=True)
            res.decoding_success = True
            _timeit = timeit.Timer("module.loads(_res, keys=True)",
                                   globals=locals())
            res.decoding_time = _timeit.timeit(TIMEITNUMBER)

            if obj == _res2:
                res.reversibility = True
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"[{fingerprint}] res.reversibility (first part:obj == _res2) "
                         f"is {res.reversibility}")
            if res.reversibility and works_as_expected:
                res.reversibility = res.reversibility and works_as_expected(obj=_res2)
                if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                    msgdebug(f"[{fingerprint}] res.reversibility "
                             f"(second part:works_as_expected(_res2)) "
                             f"is {res.reversibility}.")

        except (TypeError, AttributeError) as error:
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"[{fingerprint}] '{module}': decoding failed ({error})")
            res = None

    if res is not None and res.reversibility is True:
        if wisteria.globs.PLATFORM_SYSTEM == "Windows":
            res.mem_usage = win_memory() - mem0
        else:
            res.mem_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - mem0

    return res


def serializer_marshal(action="serialize",
                       obj=None,
                       fingerprint="",
                       works_as_expected=None):
    """
        serializer_marshal()

        Serializer for the marshal module.

        Like every serializer_xxx() function:
        * this function may return (action='version') the version of the concerned module.
        * this function may try (action='serialize') to encode/decode an <obj>ect.
        * if the serializer raises an error, this error is silently converted and no exception
          is raised. If an internal error happpens, a WisteriaError exception is raised.

        This function assumes that the concerned module has already be imported.

        _______________________________________________________________________

        ARGUMENTS:
        o  action           : (str) either "version" either "serialize"
        o  obj              : the object to be serialized
        o  fingerprint      : a string describing the operation (usefull to debug)
        o  works_as_expected: (None or callable)if not None, will be called to check
                              the reversibility of the de-serialized object.

        RETURNED VALUE:
           - None if an error occcured
           - if <action> is (str)"version", return a string.
           - if <action> is (str)"serialize", return a SerializationResult object.
    """
    module = MODULES["marshal"]

    # -------------------
    # action == "version"
    # -------------------
    if action == "version":
        return f"version {module.version}; (Python version) {sys.version.replace(chr(0x0A), '- ')}"

    # ---------------------
    # action == "serialize"
    # ---------------------
    if action != "serialize":
        raise WisteriaError(f"(ERRORID033) Unknown 'action' keyword '{action}'.")

    # MEMOVERUSE# ---- --memoveruse ? -----------------------------------------------------
    # MEMOVERUSEif 'Python' in wisteria.globs.ARGS.memoveruse:
    # MEMOVERUSE    #   pylint: disable=possibly-unused-variable
    # MEMOVERUSE    dumbstr = "0123456789"*100000
    # MEMOVERUSEif 'C++' in wisteria.globs.ARGS.memoveruse:
    # MEMOVERUSE    MemOverUse().memoveruse()

    # ---- main computation ---------------------------------------------------
    res = SerializationResult()

    if wisteria.globs.PLATFORM_SYSTEM == "Windows":
        mem0 = win_memory()
    else:
        mem0 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    _error = False
    try:
        _res = module.dumps(obj)
        _timeit = timeit.Timer('module.dumps(obj)',
                               globals=locals())
        res.encoding_success = True
        res.encoding_strlen = _len(_res)
        res.encoding_time = _timeit.timeit(TIMEITNUMBER)

        if wisteria.globs.ARGS.verbosity >= VERBOSITY_DETAILS:
            msginfo(f"([{fingerprint}] '{module.__name__}' / '{type(obj)}') "
                    f"encoded string='{_res}'")

    except (TypeError, ValueError) as error:
        if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
            msgdebug(f"[{fingerprint}] '{module}': encoding failed ({error})")
        _error = True

    if not _error:
        try:
            _res2 = module.loads(_res)
            res.decoding_success = True
            _timeit = timeit.Timer("module.loads(_res)",
                                   globals=locals())
            res.decoding_time = _timeit.timeit(TIMEITNUMBER)

            if obj == _res2:
                res.reversibility = True
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"[{fingerprint}] res.reversibility (first part:obj == _res2) "
                         f"is {res.reversibility}")
            if res.reversibility and works_as_expected:
                res.reversibility = res.reversibility and works_as_expected(obj=_res2)
                if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                    msgdebug(f"[{fingerprint}] res.reversibility "
                             f"(second part:works_as_expected(_res2)) "
                             f"is {res.reversibility}.")

        except (TypeError, AttributeError) as error:
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"[{fingerprint}] '{module}': decoding failed ({error})")
            res = None

    if res is not None and res.reversibility is True:
        if wisteria.globs.PLATFORM_SYSTEM == "Windows":
            res.mem_usage = win_memory() - mem0
        else:
            res.mem_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - mem0

    return res


def serializer_pickle(action="serialize",
                      obj=None,
                      fingerprint="",
                      works_as_expected=None):
    """
        serializer_pickle()

        Serializer for the pickle module.

        Like every serializer_xxx() function:
        * this function may return (action='version') the version of the concerned module.
        * this function may try (action='serialize') to encode/decode an <obj>ect.
        * if the serializer raises an error, this error is silently converted and no exception
          is raised. If an internal error happpens, a WisteriaError exception is raised.

        This function assumes that the concerned module has already be imported.

        _______________________________________________________________________

        ARGUMENTS:
        o  action           : (str) either "version" either "serialize"
        o  obj              : the object to be serialized
        o  fingerprint      : a string describing the operation (usefull to debug)
        o  works_as_expected: (None or callable)if not None, will be called to check
                              the reversibility of the de-serialized object.

        RETURNED VALUE:
           - None if an error occcured
           - if <action> is (str)"version", return a string.
           - if <action> is (str)"serialize", return a SerializationResult object.
    """
    module = MODULES["pickle"]

    # -------------------
    # action == "version"
    # -------------------
    if action == "version":
        return f"(Python version) {sys.version.replace(chr(0x0A), '- ')}"

    # ---------------------
    # action == "serialize"
    # ---------------------
    if action != "serialize":
        raise WisteriaError(f"(ERRORID034) Unknown 'action' keyword '{action}'.")

    # MEMOVERUSE# ---- --memoveruse ? -----------------------------------------------------
    # MEMOVERUSEif 'Python' in wisteria.globs.ARGS.memoveruse:
    # MEMOVERUSE    #   pylint: disable=possibly-unused-variable
    # MEMOVERUSE    dumbstr = "0123456789"*100000
    # MEMOVERUSEif 'C++' in wisteria.globs.ARGS.memoveruse:
    # MEMOVERUSE    MemOverUse().memoveruse()

    # ---- main computation ---------------------------------------------------
    res = SerializationResult()

    if wisteria.globs.PLATFORM_SYSTEM == "Windows":
        mem0 = win_memory()
    else:
        mem0 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    _error = False
    try:
        _res = module.dumps(obj)
        _timeit = timeit.Timer('module.dumps(obj)',
                               globals=locals())
        res.encoding_success = True
        res.encoding_strlen = _len(_res)
        res.encoding_time = _timeit.timeit(TIMEITNUMBER)

        if wisteria.globs.ARGS.verbosity >= VERBOSITY_DETAILS:
            msginfo(f"([{fingerprint}] '{module.__name__}' / '{type(obj)}') "
                    f"encoded string='{_res}'")

    except TypeError as error:
        if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
            msgdebug(f"[{fingerprint}] '{module}': encoding failed ({error})")
        _error = True

    if not _error:
        try:
            _res2 = module.loads(_res)
            res.decoding_success = True
            _timeit = timeit.Timer("module.loads(_res)",
                                   globals=locals())
            res.decoding_time = _timeit.timeit(TIMEITNUMBER)

            if obj == _res2:
                res.reversibility = True
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"[{fingerprint}] res.reversibility (first part:obj == _res2) "
                         f"is {res.reversibility}")
            if res.reversibility and works_as_expected:
                res.reversibility = res.reversibility and works_as_expected(obj=_res2)
                if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                    msgdebug(f"[{fingerprint}] res.reversibility "
                             f"(second part:works_as_expected(_res2)) "
                             f"is {res.reversibility}.")

        except (TypeError, AttributeError) as error:
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"[{fingerprint}] '{module}': decoding failed ({error})")
            res = None

    if res is not None and res.reversibility is True:
        if wisteria.globs.PLATFORM_SYSTEM == "Windows":
            res.mem_usage = win_memory() - mem0
        else:
            res.mem_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - mem0

    return res


def serializer_pyyaml(action="serialize",
                      obj=None,
                      fingerprint="",
                      works_as_expected=None):
    """
        serializer_pyyaml()

        Serializer for the pyyaml module.

        Like every serializer_xxx() function:
        * this function may return (action='version') the version of the concerned module.
        * this function may try (action='serialize') to encode/decode an <obj>ect.
        * if the serializer raises an error, this error is silently converted and no exception
          is raised. If an internal error happpens, a WisteriaError exception is raised.

        This function assumes that the concerned module has already be imported.

        _______________________________________________________________________

        ARGUMENTS:
        o  action           : (str) either "version" either "serialize"
        o  obj              : the object to be serialized
        o  fingerprint      : a string describing the operation (usefull to debug)
        o  works_as_expected: (None or callable)if not None, will be called to check
                              the reversibility of the de-serialized object.

        RETURNED VALUE:
           - None if an error occcured
           - if <action> is (str)"version", return a string.
           - if <action> is (str)"serialize", return a SerializationResult object.
    """
    module = MODULES["yaml"]

    # -------------------
    # action == "version"
    # -------------------
    if action == "version":
        return module.__version__

    # ---------------------
    # action == "serialize"
    # ---------------------
    if action != "serialize":
        raise WisteriaError(f"(ERRORID044) Unknown 'action' keyword '{action}'.")

    # MEMOVERUSE# ---- --memoveruse ? -----------------------------------------------------
    # MEMOVERUSEif 'Python' in wisteria.globs.ARGS.memoveruse:
    # MEMOVERUSE    #   pylint: disable=possibly-unused-variable
    # MEMOVERUSE    dumbstr = "0123456789"*100000
    # MEMOVERUSEif 'C++' in wisteria.globs.ARGS.memoveruse:
    # MEMOVERUSE    MemOverUse().memoveruse()

    # ---- main computation ---------------------------------------------------
    res = SerializationResult()

    if wisteria.globs.PLATFORM_SYSTEM == "Windows":
        mem0 = win_memory()
    else:
        mem0 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    _error = False
    try:
        _res = module.dump(obj, Dumper=module.Dumper)
        _timeit = timeit.Timer('module.dump(obj, Dumper=module.Dumper)',
                               globals=locals())
        res.encoding_success = True
        res.encoding_strlen = _len(_res)
        res.encoding_time = _timeit.timeit(TIMEITNUMBER)

        if wisteria.globs.ARGS.verbosity >= VERBOSITY_DETAILS:
            msginfo(f"([{fingerprint}] '{module.__name__}' / '{type(obj)}') "
                    f"encoded string='{_res}'")

    except (ValueError, TypeError) as error:
        if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
            msgdebug(f"[{fingerprint}] '{module}': encoding failed ({error})")
        _error = True

    if not _error:
        try:
            _res2 = module.load(_res, Loader=module.Loader)
            res.decoding_success = True
            _timeit = timeit.Timer("module.load(_res, Loader=module.Loader)",
                                   globals=locals())
            res.decoding_time = _timeit.timeit(TIMEITNUMBER)

            if obj == _res2:
                res.reversibility = True
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"[{fingerprint}] res.reversibility (first part:obj == _res2) "
                         f"is {res.reversibility}")
            if res.reversibility and works_as_expected:
                res.reversibility = res.reversibility and works_as_expected(obj=_res2)
                if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                    msgdebug(f"[{fingerprint}] res.reversibility "
                             f"(second part:works_as_expected(_res2)) "
                             f"is {res.reversibility}.")

        except (module.constructor.ConstructorError, ValueError) as error:
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"[{fingerprint}] '{module}': decoding failed ({error})")
            res = None

    if res is not None and res.reversibility is True:
        if wisteria.globs.PLATFORM_SYSTEM == "Windows":
            res.mem_usage = win_memory() - mem0
        else:
            res.mem_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - mem0

    return res


def serializer_yajl(action="serialize",
                    obj=None,
                    fingerprint="",
                    works_as_expected=None):
    """
        serializer_yajl()

        Serializer for the yajl module.

        Like every serializer_xxx() function:
        * this function may return (action='version') the version of the concerned module.
        * this function may try (action='serialize') to encode/decode an <obj>ect.
        * if the serializer raises an error, this error is silently converted and no exception
          is raised. If an internal error happpens, a WisteriaError exception is raised.

        This function assumes that the concerned module has already be imported.

        _______________________________________________________________________

        ARGUMENTS:
        o  action           : (str) either "version" either "serialize"
        o  obj              : the object to be serialized
        o  fingerprint      : a string describing the operation (usefull to debug)
        o  works_as_expected: (None or callable)if not None, will be called to check
                              the reversibility of the de-serialized object.

        RETURNED VALUE:
           - None if an error occcured
           - if <action> is (str)"version", return a string.
           - if <action> is (str)"serialize", return a SerializationResult object.
    """
    module = MODULES["yajl"]

    # -------------------
    # action == "version"
    # -------------------
    if action == "version":
        return "unkown version"

    # ---------------------
    # action == "serialize"
    # ---------------------
    if action != "serialize":
        raise WisteriaError(f"(ERRORID044) Unknown 'action' keyword '{action}'.")

    # MEMOVERUSE# ---- --memoveruse ? -----------------------------------------------------
    # MEMOVERUSEif 'Python' in wisteria.globs.ARGS.memoveruse:
    # MEMOVERUSE    #   pylint: disable=possibly-unused-variable
    # MEMOVERUSE    dumbstr = "0123456789"*100000
    # MEMOVERUSEif 'C++' in wisteria.globs.ARGS.memoveruse:
    # MEMOVERUSE    MemOverUse().memoveruse()

    # ---- main computation ---------------------------------------------------
    res = SerializationResult()

    if wisteria.globs.PLATFORM_SYSTEM == "Windows":
        mem0 = win_memory()
    else:
        mem0 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    _error = False
    try:
        _res = module.dumps(obj)
        _timeit = timeit.Timer('module.dumps(obj)',
                               globals=locals())
        res.encoding_success = True
        res.encoding_strlen = _len(_res)
        res.encoding_time = _timeit.timeit(TIMEITNUMBER)

        if wisteria.globs.ARGS.verbosity >= VERBOSITY_DETAILS:
            msginfo(f"([{fingerprint}] '{module.__name__}' / '{type(obj)}') "
                    f"encoded string='{_res}'")

    except (ValueError, TypeError) as error:
        if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
            msgdebug(f"[{fingerprint}] '{module}': encoding failed ({error})")
        _error = True

    if not _error:
        try:
            _res2 = module.loads(_res)
            res.decoding_success = True
            _timeit = timeit.Timer("module.loads(_res)",
                                   globals=locals())
            res.decoding_time = _timeit.timeit(TIMEITNUMBER)

            if obj == _res2:
                res.reversibility = True
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"[{fingerprint}] res.reversibility (first part:obj == _res2) "
                         f"is {res.reversibility}")
            if res.reversibility and works_as_expected:
                res.reversibility = res.reversibility and works_as_expected(obj=_res2)
                if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                    msgdebug(f"[{fingerprint}] res.reversibility "
                             f"(second part:works_as_expected(_res2)) "
                             f"is {res.reversibility}.")

        except (ValueError,) as error:
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"[{fingerprint}] '{module}': decoding failed ({error})")
            res = None

    if res is not None and res.reversibility is True:
        if wisteria.globs.PLATFORM_SYSTEM == "Windows":
            res.mem_usage = win_memory() - mem0
        else:
            res.mem_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - mem0

    return res


def init_serializers():
    """
        init_serializers()

        Initialize wisteria.globs.SERIALIZERS
    """
    for serializerdata in (
            SerializerData(
                name="iaswn",
                module_name="iaswn",
                human_name="Iaswn",
                internet="https://github.com/suizokukan/iaswn",
                func=serializer_iaswn,
                cwc="iaswn"),
            SerializerData(
                name="json",
                module_name="json",
                human_name="json",
                internet="https://docs.python.org/3/library/json.html",
                func=serializer_json,
                cwc="default"),
            SerializerData(
                name="jsonpickle",
                module_name="jsonpickle",
                human_name="jsonpickle",
                internet="https://jsonpickle.github.io/",
                func=serializer_jsonpickle,
                cwc="default"),
            SerializerData(
                name="jsonpickle_keystrue",
                module_name="jsonpickle",
                human_name="jsonpickle(keys=True)",
                internet="https://jsonpickle.github.io/",
                func=serializer_jsonpickle_keystrue,
                cwc="default",
                comment="jsonpickle with keys=True"),
            SerializerData(
                name="marshal",
                module_name="marshal",
                human_name="marshal",
                internet="https://docs.python.org/3/library/marshal.html#module-marshal",
                func=serializer_marshal,
                cwc="default"),
            SerializerData(
                name="pickle",
                module_name="pickle",
                human_name="pickle",
                internet="https://docs.python.org/3/library/pickle.html",
                func=serializer_pickle,
                cwc="default"),
            SerializerData(
                name="pyyaml",
                module_name="yaml",
                human_name="pyyaml",
                internet="https://pyyaml.org/",
                func=serializer_pyyaml,
                cwc="default"),
            SerializerData(
                name="yajl",
                module_name="yajl",
                human_name="yajl",
                internet="https://lloyd.github.io/yajl/",
                func=serializer_yajl,
                cwc="default"),
            ):
        if trytoimport(serializerdata.module_name):
            wisteria.globs.SERIALIZERS[serializerdata.name] = serializerdata
            wisteria.globs.SERIALIZERS[serializerdata.name].version = serializerdata.func("version")
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"Successfully imported '{serializerdata.module_name}' module.")
        else:
            wisteria.globs.UNAVAILABLE_SERIALIZERS[serializerdata.name] = serializerdata
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"Could not import '{serializerdata.module_name}' module.")
