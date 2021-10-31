# SPDX-License-Identifier: MIT
# Copyright (c) 2014 Darío Cutillas Carrillo.

from __future__ import print_function

import itertools
import os
import re

from SCons.Scanner import Scanner, FindPathDirs
from SCons.Builder import Builder
import SCons.Action
import SCons.Util


def exists(env):
    return env.Detect(['bgdc', 'pxtb'])


def generate(env):
    include_files_scanner = Scanner(
        function=includes_scanner,
        skeys=[".prg", ".h"],
        path_function=FindPathDirs("DCBCPATH"),
        recursive=True,
    )

    dcb = Builder(
        generator=generate_dcb_actions,
        suffix=".dcb",
        src_suffix=[".prg"],
        emitter=libs_emitter,
    )

    lib = Builder(
        generator=generate_lib_actions,
        suffix=".dcl",
        src_suffix=[".prg", ".inc"],
        emitter=libs_emitter,
    )

    env["BUILDERS"]["Dcb"] = dcb
    env["BUILDERS"]["Dcl"] = lib
    env.Append(SCANNERS=include_files_scanner)

    # Path or executable to the DCB compiler
    env["DCBC"] = "bgdc"
    # Additional compilation flags
    env["DCBCFLAGS"] = SCons.Util.CLVar(" ")
    # A dict that defines macros to passed to the compiler
    env["DCBCMACROS"] = dict()
    # A list of additional paths where the compiler shall search for files
    env["DCBCPATH"] = []
    # A list of files to be passed to the compiler
    env["DCBCFILES"] = []
    # A list of dcb libraries (dcl) that shall be passed to the compiler
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

    # Mapping function to generate a string from $DCBCMACROS dict
    env["expandmacros"] = expandmacros
    # Mapping function to generate a string from $DCBCPATH list
    env["expandincludes"] = expandincludes
    # Mapping function to generate a string from $DCBCFILES list
    env["expandfiles"] = expandfiles
    # Mapping function to generate a string form a list $DCBCLIBS
    env["expandlibs"] = expandlibs

    env["_DCBMACROFLAGS"] = "$( ${expandmacros(DCBCMACROS, __env__)} $)"
    env["_DCBCINCFLAGS"] = "$( ${expandincludes(DCBCPATH, __env__)} $)"
    env["_DCBCFILEFLAGS"] = "$( ${expandfiles(DCBCFILES, __env__)} $)"
    env["_DCBCLIBFLAGS"] = "$( ${expandlibs(DCBCLIBS, __env__)} $)"

    # A function to handle execution of external commands
    env["SPAWN"] = spawn(env["SPAWN"])


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


def libs_emitter(target, source, env):
    """Append specified libraries to source."""

    for lib in env["DCBCLIBS"]:
        source.append(adjust_suffix(lib, env["DCBCLIBEXTENSION"]))

    return target, source


def includes_scanner(node, env, path):
    """Scan for #include "filename" in the node path and in path."""

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


def spawn(wrapped):
    """Handle non-zero exit code of bgdc indicating success."""

    def spawn(sh, escape, cmd, args, env):
        exit_code = wrapped(sh, escape, cmd, args, env)
        success_exit_code = 1 if "bgdc" in cmd else 0
        return 0 if exit_code == success_exit_code else 0

    return spawn


def expandmacros(defs, env):
    """Format macro dictionary as a string."""
    return " ".join([f"{env['DCBCMACROPREFIX']}{k}={v}" for (k, v) in defs.items()])


def expandlist(prefix, list, env):
    """Format list of nodes into a space separate string preppending prefix to each node."""
    return " ".join([f"{prefix}{x}" for x in list])


def expandfiles(files, env):
    """Format file list as a string with each file path prefixed with DCBCFILEPREFIX."""
    return expandlist(env["DCBCFILEPREFIX"], files, env)


def expandincludes(includes, env):
    """Format includes list as a string with each include path prefixed with DCBCINCPREFIX."""
    return expandlist(env["DCBCINCPREFIX"], includes, env)


def expandlibs(libs, env):
    """Format libs list as a string with each lib path prefixed with DCBCLIBPREFIX ensuring
    each lib path has the DCBCLIBEXTENSION.
    """

    def format_lib(lib):
        prefix = env["DBCLIBPREFIX"]
        lib_adjusted = adjust_suffix(lib, env["DCBCLIBEXTENSION"])
        return f"{prefix}{lib_adjusted}"

    return " ".join([format_lib(l) for l in libs])


def adjust_suffix(file, suffix):
    """Add suffix to filename if it hasn't already been added."""

    return SCons.Util.adjustixes(file, "", suffix, False)
