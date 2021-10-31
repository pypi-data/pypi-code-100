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
    Wisteria project : wisteria/cfgfile.py

    Config file reading & downloading.

    ___________________________________________________________________________

    o  downloadconfigfile()
    o  read_cfgfile(filename)
"""
import configparser
import os.path
import shutil
import urllib.error
import urllib.request

from wisteria.globs import DEFAULT_CONFIG_FILENAME, DEFAULTCFGFILE_URL
from wisteria.globs import VERBOSITY_NORMAL, VERBOSITY_DETAILS, VERBOSITY_DEBUG
from wisteria.utils import normpath
from wisteria.msg import msginfo, msgerror, msgdebug
import wisteria.globs


def downloadconfigfile():
    """
        downloadconfigfile()

        Download default config file.
        _______________________________________________________________________

        RETURNED VALUE: (bool)success
    """
    targetname = DEFAULT_CONFIG_FILENAME

    if wisteria.globs.ARGS.verbosity >= VERBOSITY_NORMAL:
        msginfo(f"Trying to download '{DEFAULTCFGFILE_URL}' "
                f"which will be written as '{targetname}' ('{normpath(targetname)}').")

    try:
        with urllib.request.urlopen(DEFAULTCFGFILE_URL) as response, \
             open(targetname, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)

        if wisteria.globs.ARGS.verbosity >= VERBOSITY_NORMAL:
            msginfo(f"Successfully downloaded '{DEFAULTCFGFILE_URL}', "
                    f"written as '{targetname}' ('{normpath(targetname)}').")
        return True

    except urllib.error.URLError as exception:
        msgerror(f"(ERRORID000) An error occured: {exception}")
        return False


def read_cfgfile(filename):
    """
        read_cfgfile()

        Read the configuration file <filename>, return the corresponding dict.

        _______________________________________________________________________

        ARGUMENT: (str)filename, the file to be read.

        RETURNED VALUE: (None if a problem occured or a dict is success)
            (pimydoc)config file format
            ⋅
            ⋅----------------------------------------------------------------
            ⋅config file format                 read_cfgfile() returned value
            ⋅----------------------------------------------------------------
            ⋅(data selection)                   〖"data selection"〗 = {}
            ⋅    data selection=all             〖"data selection"〗〖"data selection"〗 = str
            ⋅                   only if yes
            ⋅                   data set/xxx
            ⋅data sets                          〖"data sets"〗= {}
            ⋅    data set/xxx=                  〖"data sets"〗〖"data set/xxx"〗 = set1;set2;...
            ⋅data objects
            ⋅    set1 = yes or false             〖"data objects"〗〖"set1"〗 = (bool)True/False
            ⋅    set2 = yes or false
            ⋅    ...
    """
    if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
        msgdebug(f"Trying to read '{filename}' ({normpath(filename)}) as a config file.")

    if not os.path.exists(filename):
        if not wisteria.globs.ARGS.checkup:
            msgerror(f"(ERRORID001) Missing config file '{filename}' ({normpath(filename)}).")
        return None

    res = {"data selection": {},
           "data sets": {},
           "data objects": {},
           }

    # ------------------------------------------------------------------
    # (1/4) let's read <filename> using configparser.ConfigParser.read()
    # ------------------------------------------------------------------
    try:
        config = configparser.ConfigParser()
        config.read(filename)
    except (configparser.DuplicateOptionError,) as error:
        msgerror(f"(ERRORID002) While reading config file '{filename}': {error} .")
        return None

    # -------------------------------
    # (2/4) well formed config file ?
    # -------------------------------
    success = True
    if "data selection" not in config:
        msgerror(f"(ERRORID003) While reading config file '{filename}': "
                 "missing '\\[data selection]' section.")
        success = False
    if "data sets" not in config:
        msgerror(f"(ERRORID004) While reading config file '{filename}': "
                 "missing '\\[data sets]' section.")
        success = False
    if "data objects" not in config:
        msgerror(f"(ERRORID005) While reading config file '{filename}': "
                 "missing '\\[data objects]' section.")
        success = False
    if "data selection" not in config["data selection"]:
        msgerror(f"(ERRORID006) While reading config file '{filename}': "
                 "missing '\\[data selection]data selection=' entry.")
        success = False
    if not success:
        return None

    if config["data selection"]["data selection"] in ('all', 'only if yes'):
        # ok, nothing to do.
        pass
    elif config["data selection"]["data selection"].startswith("data set/"):
        setname = config["data selection"]["data selection"]
        if setname not in config["data sets"]:
            msgerror(f"(ERRORID007) While reading config file '{filename}': "
                     f"undefined data set '{setname}' "
                     "used in \\[data selection] section but not defined in \\[data sets] section")
            return None
    else:
        msgerror(f"(ERRORID008) While reading config file '{filename}': "
                 "can't interpret the value of config['data selection']['data selection']: "
                 f"what is '{config['data selection']['data selection']}' ?")
        return None

    for data_set in config['data sets']:
        for data_set__subitem in config['data sets'][data_set].split(";"):
            if data_set__subitem.strip() != "" and \
               data_set__subitem not in config['data objects']:
                msgerror("(ERROR014) Wrong definition in \\[data sets]; unknown data object "
                         f"'{data_set__subitem}', not defined in \\[data objects].")
                return None

    # --------------------------------------------------------
    # (3/4) if everything is in order, let's initialize <res>.
    # --------------------------------------------------------
    res['data selection']['data selection'] = config['data selection']['data selection']
    for dataobject_name in config['data objects']:
        res['data objects'][dataobject_name] = config['data objects'].getboolean(dataobject_name)
    for data_set in config['data sets']:
        res['data sets'][data_set] = \
            (data for data in config['data sets'][data_set].split(";") if data.strip() != "")

    # --------------------------------------------------------------
    # (4/4) check: are all DATA/UNAVAILABLE_DATA keys defined in the
    #              configuration file, and vice-versa ?
    # --------------------------------------------------------------
    errors = []
    for dataobject_name in wisteria.globs.DATA:
        if dataobject_name not in config['data objects']:
            errors.append(f"(ERRORID037) '{dataobject_name}' is defined as a DATA key "
                          "but is not defined in the configuration file.")
    for dataobject_name in wisteria.globs.UNAVAILABLE_DATA:
        if dataobject_name not in config['data objects']:
            errors.append(f"(ERRORID038) '{dataobject_name}' is defined as an UNAVAILABLE_DATA key "
                          "but is not defined in the configuration file.")
    for dataobject_name in config['data objects']:
        if dataobject_name not in tuple(wisteria.globs.DATA.keys()) + \
           tuple(wisteria.globs.UNAVAILABLE_DATA.keys()):
            errors.append(f"(ERRORID039) '{dataobject_name}' is defined as a data key "
                          "in the configuration file but is not defined as a DATA key "
                          "or as an UNAVAILABLE_DATA key.")

    if errors:
        for error in errors:
            msgerror(error)
        return None

    # ----------------------
    # details/debug messages
    # ----------------------
    if wisteria.globs.ARGS.verbosity >= VERBOSITY_DETAILS:
        msginfo(f"Init file '{filename}' ({normpath(filename)}) has been read.")

    if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
        msgdebug(f"Successfully read '{filename}' ({normpath(filename)}) as a config file.")

    return res
