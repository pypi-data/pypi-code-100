#!/usr/bin/python3
# -*- coding: utf-8 -*-
# vim: set ts=4
#
# Copyright 2021-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import argparse
from pathlib import Path
import sys
from urllib.parse import urlparse

from tuxrun import __version__
from tuxrun.assets import get_rootfs, get_test_definitions, ROOTFS
from tuxrun.devices import Device
import tuxrun.templates as templates
from tuxrun.tuxmake import TuxMakeBuild
from tuxrun.utils import TTYProgressIndicator


###########
# Helpers #
###########
def filter_options(options):
    keys = [
        "device",
        "tuxmake",
        "device_dict",
        "definition",
        "runtime",
        "image",
        "log_file",
        "results",
        "debug",
    ]
    return {k: getattr(options, k) for k in vars(options) if k not in keys}


def pathurlnone(string):
    if string is None:
        return None
    url = urlparse(string)
    if url.scheme in ["http", "https"]:
        return string
    if url.scheme not in ["", "file"]:
        raise argparse.ArgumentTypeError(f"Invalid scheme '{url.scheme}'")

    path = Path(string if url.scheme == "" else url.path)
    if not path.exists():
        raise argparse.ArgumentTypeError(f"{path} no such file or directory")
    return f"file://{path.expanduser().resolve()}"


def pathnone(string):
    if string is None:
        return None

    path = Path(string)
    if not path.exists():
        raise argparse.ArgumentTypeError(f"{path} no such file or directory")
    return path.expanduser().resolve()


def tuxmake_directory(s):
    try:
        return TuxMakeBuild(s)
    except TuxMakeBuild.Invalid as e:
        raise argparse.ArgumentTypeError(str(e))


###########
# Actions #
###########
class ListDevicesAction(argparse.Action):
    def __init__(
        self, option_strings, help, dest=argparse.SUPPRESS, default=argparse.SUPPRESS
    ):
        super().__init__(option_strings, dest=dest, default=default, nargs=0, help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        parser._print_message("\n".join(Device.list()) + "\n", sys.stderr)
        parser.exit()


class ListTestsAction(argparse.Action):
    def __init__(
        self, option_strings, help, dest=argparse.SUPPRESS, default=argparse.SUPPRESS
    ):
        super().__init__(option_strings, dest=dest, default=default, nargs=0, help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        parser._print_message("\n".join(templates.tests_list()) + "\n", sys.stderr)
        parser.exit()


class KeyValueAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        for value in values:
            key, value = value.split("=")
            getattr(namespace, self.dest)[key] = value


class UpdateCacheAction(argparse.Action):
    def __init__(
        self, option_strings, help, dest=argparse.SUPPRESS, default=argparse.SUPPRESS
    ):
        super().__init__(option_strings, dest=dest, default=default, nargs=0, help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        print("Updating local cache:")
        print("* Rootfs:")
        for device in [d for d in Device.list() if d in ROOTFS]:
            print(f"  * {device}")
            get_rootfs(
                device, progress=TTYProgressIndicator("Downloading root filesystem")
            )
        print("* Test definitions")
        get_test_definitions(
            progress=TTYProgressIndicator("Downloading test definitions")
        )
        parser.exit()


##########
# Setups #
##########
def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tuxrun", description="TuxRun")

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s, {__version__}"
    )
    parser.add_argument(
        "--device",
        default=None,
        metavar="NAME",
        help="Device type",
        choices=Device.list(),
    )

    group = parser.add_argument_group("listing")
    group.add_argument(
        "--list-devices", action=ListDevicesAction, help="List available devices"
    )
    group.add_argument(
        "--list-tests", action=ListTestsAction, help="List available tests"
    )

    group = parser.add_argument_group("cache")
    group.add_argument(
        "--update-cache", action=UpdateCacheAction, help="Update assets cache"
    )

    group = parser.add_argument_group("artefacts")

    def artefact(name):
        group.add_argument(
            f"--{name}",
            default=None,
            metavar="URL",
            type=pathurlnone,
            help=f"{name} URL",
        )

    artefact("bios")
    artefact("dtb")
    artefact("kernel")
    artefact("mcp-fw")
    artefact("mcp-romfw")
    artefact("modules")
    group.add_argument(
        "--overlay",
        default=[],
        metavar="URL",
        type=pathurlnone,
        help="Tarball with overlay for rootfs. Can be specified multiple times",
        action="append",
        dest="overlays",
    )
    group.add_argument(
        "--partition",
        default=None,
        metavar="NUMBER",
        type=int,
        help="rootfs partition number",
    )
    artefact("rootfs")
    artefact("scp-fw")
    artefact("scp-romfw")
    group.add_argument(
        "--tuxmake",
        metavar="DIRECTORY",
        default=None,
        type=tuxmake_directory,
        help="directory containing a TuxMake build",
    )
    artefact("uefi")

    group = parser.add_argument_group("test parameters")
    group.add_argument(
        "--parameters",
        metavar="K=V",
        default={},
        type=str,
        help="test parameters as key=value",
        action=KeyValueAction,
        nargs="+",
    )

    group.add_argument(
        "--tests",
        nargs="+",
        default=[],
        metavar="T",
        help="test suites",
        choices=templates.tests_list(),
    )
    group.add_argument(
        "command",
        nargs="*",
        help="Command to run inside the VM",
    )

    group = parser.add_argument_group("run options")
    group.add_argument(
        "--boot-args", default="", metavar="ARGS", help="extend boot arguments"
    )

    group = parser.add_argument_group("configuration files")
    group.add_argument(
        "--device-dict", default=None, type=pathnone, help="Device configuration"
    )
    group.add_argument(
        "--definition", default=None, type=pathnone, help="Job definition"
    )

    group = parser.add_argument_group("runtime")
    group.add_argument(
        "--runtime",
        default="podman",
        metavar="RUNTIME",
        choices=["docker", "null", "podman"],
        help="Runtime",
    )
    group.add_argument(
        "--image",
        default="docker.io/lavasoftware/lava-dispatcher:latest",
        help="Image to use",
    )

    group = parser.add_argument_group("output")
    group.add_argument("--log-file", default=None, type=Path, help="Store logs to file")
    group.add_argument(
        "--results", default=None, type=Path, help="Save test results to file (JSON)"
    )

    group = parser.add_argument_group("debugging")
    group.add_argument(
        "--debug",
        default=False,
        action="store_true",
        help="Print more debug information about tuxrun",
    )

    return parser
