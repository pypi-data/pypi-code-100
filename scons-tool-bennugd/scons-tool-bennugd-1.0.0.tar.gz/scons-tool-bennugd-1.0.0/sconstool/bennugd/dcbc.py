# MIT License
# Copyright (c) 2014 Darío Cutillas Carrillo. 

from __future__ import print_function

import itertools
import os
import re

from SCons.Scanner import Scanner, FindPathDirs
from SCons.Builder import Builder
import SCons.Action
import SCons.Util


# Adds libraries in DCBCLIBS as dependencies of the source node
def emit_libs(target, source, env):
    for lib in env["DCBCLIBS"]:
        source.append(lib + env["DCBCLIBEXTENSION"])

    return target, source


# Scans #include directives and add included sources as dependencies of the source nodes
def scan_for_includes(node, env, path):
    """
    Scans for #include "filename" in the node folder and any other
    folder of the path
    """
    include_re = re.compile(r'^#include\s+"(\S+)"\s*$', re.M)

    contents = node.get_text_contents()
    includes = include_re.findall(contents)

    results = []

    source_folder = node.get_dir().get_path()

    for include in includes:
        for dir in itertools.chain([source_folder], [x.get_path() for x in path]):
            file = os.path.join(dir, include)
            if os.path.exists(file):
                results.append(env.File(file))

    return results


def _macros(defs, env):
    return " ".join([env["DCBCMACROPREFIX"] + k + "=" + v for (k, v) in defs.items()])


def _prefix(prefix, nodes, env):
    return " ".join([prefix + x for x in nodes])


def _expandlibs(prefix, nodes, env):
    return " ".join([prefix + x + env["DCBCLIBEXTENSION"] for x in nodes])


def generate_dcb_actions(source, target, env, for_signature):
    return SCons.Action.Action(
        "$DCBC \
        $DCBCFLAGS \
        $_DCBMACROFLAGS \
        $_DCBCINCFLAGS \
        $_DCBCFILEFLAGS \
        $_DCBCLIBFLAGS \
        -o$TARGET \
        $SOURCE",
        "$DCBCSRC",
    )


def generate_lib_actions(source, target, env, for_signature):
    return SCons.Action.Action(
        "$DCBC --libmode \
        $DCBCFLAGS \
        $_DCBMACROFLAGS \
        $_DCBCINCFLAGS \
        $_DCBCFILEFLAGS \
        $_DCBCLIBFLAGS \
        -o$TARGET \
        $SOURCE",
        "$DCBCSRC",
    )


include_files_scanner = Scanner(
    function=scan_for_includes,
    skeys=[".prg", ".h"],
    path_function=FindPathDirs("DCBCPATH"),
    recursive=True,
)

dcb = Builder(
    generator=generate_dcb_actions,
    suffix=".dcb",
    src_suffix=[".prg"],
    emitter=emit_libs,
)

lib = Builder(
    generator=generate_lib_actions,
    suffix=".dcl",
    src_suffix=[".prg", ".inc"],
    emitter=emit_libs,
)


def generate(env):
    env["BUILDERS"]["Dcb"] = dcb
    env["BUILDERS"]["Dcl"] = lib
    env.Append(SCANNERS=include_files_scanner)

    # The name of the binary executable used as the compiler
    env["DCBC"] = "bgdc"
    # Additional compilation flags
    env["DCBCFLAGS"] = SCons.Util.CLVar(" ")
    # A dictionary containing macros to be defined during compilation
    env["DCBCMACROS"] = dict()
    # A list of additional paths where the compiler shall search for files
    env["DCBCPATH"] = []
    # A list of files that shall be included in the compiler
    env["DCBCFILES"] = []
    # A list of libraries that shall be included in the compiler
    env["DCBCLIBS"] = []
    # The extension used by files compiled with the --libmode option
    env["DCBCLIBEXTENSION"] = ".dcl"
    # Option passed to the compiler to define a macro
    env["DCBCMACROPREFIX"] = "-D"
    # Option passed to the compiler to add directories to the PATH
    env["DCBCINCPREFIX"] = "-i"
    # Option passed to the compiler to add a single file to the DCB
    env["DCBCFILEPREFIX"] = "-f"
    # Option passed to the compiler to include a library (dcl).
    env["DBCLIBPREFIX"] = "-L"

    # A function that translates $DCBCMACROS entries into strings
    # prefixed by $DCBCMACROPREFIX.
    env["_macros"] = _macros
    # A function that translates $DCBCPATH, $DCBCFILES and $DCBCLIBS
    # into prefixed strings by $DCBCINCPREFIX, $DCBCFILEPREFIX and
    # $DBCLIBPREFIX respectively
    env["_prefix"] = _prefix
    env["_expandlibs"] = _expandlibs

    env["_DCBMACROFLAGS"] = "$( ${_macros(DCBCMACROS, __env__)} $)"
    env["_DCBCINCFLAGS"] = "$( ${_prefix(DCBCINCPREFIX, DCBCPATH, __env__)} $)"
    env["_DCBCFILEFLAGS"] = "$( ${_prefix(DCBCFILEPREFIX, DCBCFILES, __env__)} $)"
    env["_DCBCLIBFLAGS"] = "$( ${_expandlibs(DBCLIBPREFIX, DCBCLIBS, __env__)} $)"

    # TODO: Not yet implemented
    # env['DCBCSTUBPATH'] = ''

    # Handles differences between BennuGd and PixTudio return codes
    env["SPAWN"] = spawn(env["SPAWN"])


def exists(env):
    if not env.WhereIs('pxtb') and not env.WhereIs('bgdc'):
        return False

    return True


def spawn(wrapped):
    def spawn(sh, escape, cmd, args, env):
        exit_code = wrapped(sh, escape, cmd, args, env)
        success_exit_code = 1 if "bgdc" in cmd else 0
        return 0 if exit_code == success_exit_code else 0

    return spawn
