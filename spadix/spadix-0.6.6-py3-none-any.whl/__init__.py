#!/usr/bin/env python3
# Copyright 2019 SafeAI, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import os
import os.path

import platform
import subprocess

import sys
from sys import stderr


###############################################################################
USAGE = """
Copyright (C) 2021 SafeAI
spadix is a friendly wrapper for colcon (collective construction build manager)

Usage:
spadix [Global options] [command] [command options] ...

[Global options]
--no-console  : Don't use the default console mode: `--event-handlers console_direct+`
--no-root-check  : Don't check that spadix being started from the root of a git project
--dry-run  : Don't run `colcon` command, instead print the command line and exit

Commands:
clean  :Clean all projects (`rm -rf log install build`)
clean:<project1>[,<project2>...]  :Clean selected, comma separated projects. Spaces not supported

build  :Build all projects using --merge-install settings
build:<project1>[,<project2>...]  Build selected, comma separated projects. Spaces not supported
    Build options:
        --release   : RelWithDebInfo (default in Linux)
        --debug   : Debug build (default in windows)
        --no-fif    : disable Failure Injection Framework (FIF enabled by default)

test  :Test all projects using --merge-install settings
test:[<project1>[,<project2>...]][:test1]  :Test selected, comma separated projects,
possibly running `test1` only

gtest:<project> [gtest parameters]  :Run gtest only ('<build base>/test_<project name>')
"""

RM_DIRS_UNX = ['rm', '-rf']
RM_DIRS_WIN = ['cmd', '/C', 'rd', '/s/q']


###############################################################################
def eprint(*args, **kwargs):
    print(*args, file=stderr, **kwargs)


###############################################################################
def is_windows():
    return (platform.system() == 'Windows')


###############################################################################
def quote_list(a_list):
    return ['"%s"' % an_element for an_element in a_list]


###############################################################################
def is_merged_install(install_folder_name, colcon_install_layout_file_name):
    positively_detected = False
    merged_install = False
    colcon_install_layout_path_name = \
        os.path.join(install_folder_name, colcon_install_layout_file_name)
    if os.path.isdir(install_folder_name) and os.path.isfile(colcon_install_layout_path_name):
        try:
            colcon_install_layout = open(colcon_install_layout_path_name, 'r')
            colcon_install_layout_string = colcon_install_layout.readline().strip()
            colcon_install_layout.close()
            if colcon_install_layout_string == 'merged':
                merged_install = True
                positively_detected = True
            elif colcon_install_layout_string == 'isolated':
                positively_detected = True
        finally:
            pass
    if not positively_detected:
        if is_windows():
            merged_install = True
    return merged_install


###############################################################################
class command_line_parser:

    def __init__(self):
        self.BUILD_BASE = 'build'
        self.INSTALL_BASE = 'install'
        self.LOG_BASE = 'log'
        self.no_console = False
        self.no_root_check = False
        self.cmd_line = ['colcon']
        self.arg_idx = 0
        self.retval = 0
        self.is_build = False
        self.dry_run = False
        self.is_test = False
        self.is_parallel_overridden = False

    ###########################################################################
    # Extract global options form the provided arguments
    # argv[in] is vector of arguments
    def parse_global_options(self, argv):
        if argv is None:
            argv = []
        if len(argv) > 0:
            for arg in argv:
                if arg.startswith('--'):
                    self.arg_idx += 1
                    if arg == '--no-console':
                        self.no_console = True
                    elif arg == '--no-root-check':
                        self.no_root_check = True
                    elif arg == '--dry-run':
                        self.dry_run = True
                    else:
                        self.cmd_line.append(arg)
                else:
                    break

    ###########################################################################
    def add_console_and_merge(self):
        if is_merged_install('install', '.colcon_install_layout'):
            self.cmd_line.append('--merge-install')
        if not self.no_console:
            self.cmd_line.append('--event-handlers')
            self.cmd_line.append('console_direct+')

    ###########################################################################
    # Extract global options form the provided arguments
    # argv[in] is vector of arguments
    def parse_command(self, argv):

        expect_BUILD_BASE = False
        expect_INSTALL_BASE = False
        expect_LOG_BASE = False

        is_debug = False
        if is_windows():
            is_debug = True

        if argv is None:
            argv = []
        if len(argv[self.arg_idx:]) > 0:
            for arg in argv[self.arg_idx:]:
                self.arg_idx += 1

                ###############################################################
                if arg == '--build-base':
                    self.cmd_line.append(arg)
                    expect_BUILD_BASE = True
                elif expect_BUILD_BASE:
                    self.cmd_line.append(arg)
                    self.BUILD_BASE = arg
                    expect_BUILD_BASE = False

                elif arg == '--install-base':
                    self.cmd_line.append(arg)
                    expect_INSTALL_BASE = True
                elif expect_INSTALL_BASE:
                    self.cmd_line.append(arg)
                    self.INSTALL_BASE = arg
                    expect_INSTALL_BASE = False

                elif arg == '--log-base':
                    self.cmd_line.append(arg)
                    expect_LOG_BASE = True
                elif expect_LOG_BASE:
                    self.cmd_line.append(arg)
                    self.LOG_BASE = arg
                    expect_LOG_BASE = False

                elif arg == '--dry-run':
                    self.dry_run = True

                elif (arg == '--parallel-workers') or (arg == '--executor'):
                    self.cmd_line.append(arg)
                    self.is_parallel_overridden = True

                ###############################################################
                # Clean
                elif arg == 'clean':
                    self.cmd_line = []
                    if is_windows():
                        self.cmd_line.extend(RM_DIRS_WIN)
                    else:
                        self.cmd_line.extend(RM_DIRS_UNX)
                    self.cmd_line.extend(['docs',
                                          self.LOG_BASE, self.INSTALL_BASE, self.BUILD_BASE])
                elif arg.startswith('clean:'):
                    self.cmd_line = []
                    params = arg[len('clean:'):]
                    packages = params.split(',')
                    if (len(params) == 0) or (len(packages) == 0):
                        eprint('Error: "clean" package list is empty. Aborting...')
                        self.retval = 1
                        break
                    package_build_dir_list = []
                    for package in packages:
                        package_build_dir = os.path.join(self.BUILD_BASE, package)
                        package_build_dir_list.append(package_build_dir)
                    if is_windows():
                        self.cmd_line.extend(RM_DIRS_WIN)
                    else:
                        self.cmd_line.extend(RM_DIRS_UNX)
                    self.cmd_line.extend(package_build_dir_list)

                ###############################################################
                # Build
                elif arg == 'build':
                    self.cmd_line.append('build')
                    self.add_console_and_merge()
                    self.is_build = True
                elif arg.startswith('build:'):
                    params = arg[len('build:'):]
                    packages = params.split(',')
                    if (len(params) == 0) or (len(packages) == 0):
                        eprint('Error: "build" package list is empty. Aborting...')
                        self.retval = 1
                        break
                    self.cmd_line.append('build')
                    self.add_console_and_merge()
                    self.cmd_line.append('--packages-select')
                    for package in packages:
                        self.cmd_line.append(package)
                    self.is_build = True

                elif arg == '--release':
                    if not self.is_build:
                        eprint('Error: "--release" option in a non-build run. Aborting...')
                        self.retval = 1
                        break
                    is_debug = False

                elif arg == '--debug':
                    if not self.is_build:
                        eprint('Error: "--debug" option in a non-build run. Aborting...')
                        self.retval = 1
                        break
                    is_debug = True

                elif arg == '--no-fif':
                    if not self.is_build:
                        eprint('Error: "--no-fif" option in a non-build run. Aborting...')
                        self.retval = 1
                        break
                    os.environ['SAFEAI_FIF_DISABLED'] = 'TRUE'
                ###############################################################
                # Test
                elif arg == 'test':
                    self.cmd_line.append('test')
                    self.add_console_and_merge()
                    self.is_test = True

                elif arg.startswith('test:'):
                    params = arg[len('test:'):]
                    packages = params.split(',')
                    if (len(params) == 0):
                        eprint('Error: "test" package list is empty. Aborting...')
                        self.retval = 1
                        break
                    self.is_test = True
                    found_test = packages[len(packages) - 1].find(':')
                    found_test_name = None
                    if found_test >= 0:
                        found_test_name = packages[len(packages) - 1][found_test + 1:]
                        packages[len(packages) - 1] = packages[len(packages) - 1][:found_test]
                        if len(packages[len(packages) - 1]) == 0:
                            del packages[len(packages) - 1]
                    self.cmd_line.append('test')
                    self.add_console_and_merge()
                    if len(packages) > 0:
                        self.cmd_line.append('--packages-select')
                        for package in packages:
                            self.cmd_line.append(package)
                    if found_test_name:
                        self.cmd_line.append('--ctest-args')
                        self.cmd_line.append('-R')
                        self.cmd_line.append(found_test_name)

                ###############################################################
                # GTest
                elif arg.startswith('gtest:'):
                    pkg_name = arg[len('gtest:'):]
                    self.cmd_line = []
                    test_path = os.path.join(self.BUILD_BASE, pkg_name, 'test_' + pkg_name)
                    if is_windows():
                        test_path = os.path.join(
                            self.BUILD_BASE, pkg_name, 'Debug', 'test_' + pkg_name)
                    self.cmd_line.append(test_path)
                else:
                    self.cmd_line.append(arg)

        if self.is_build:
            if is_debug:
                self.cmd_line.extend(['--cmake-args', '-DCMAKE_BUILD_TYPE=Debug'])
            else:
                self.cmd_line.extend(['--cmake-args', '-DCMAKE_BUILD_TYPE=RelWithDebInfo'])

        if self.is_test and (not self.is_parallel_overridden):
            self.cmd_line.extend(['--parallel-workers', '1'])

        if expect_BUILD_BASE:
            eprint('Error: --build-base not followed with path. Aborting...')
            self.retval = 1

        if expect_INSTALL_BASE:
            eprint('Error: --install-base not followed with path. Aborting...')
            self.retval = 1

        if expect_LOG_BASE:
            eprint('Error: --log-base not followed with path. Aborting...')
            self.retval = 1


##############################################################################
def main():
    arg_len = len(sys.argv[1:])
    if (arg_len == 0) or (sys.argv[1] == '--help') or (sys.argv[1] == '-h'):
        retval = subprocess.run(['colcon', '--help'])
        print('--------------------------------------------------------------')
        print(USAGE)
        return retval.returncode

    clp = command_line_parser()
    clp.parse_global_options(sys.argv[1:])

    if not clp.no_root_check:
        if not os.path.isdir('.git'):
            eprint("Error: Spadix is not running from the project's root directory. Aborting...\n")
            return 1

    clp.parse_command(sys.argv[1:])
    print(clp.cmd_line)
    retval = clp.retval
    if (retval == 0) and (not clp.dry_run):
        retval = subprocess.run(clp.cmd_line).returncode
    return retval


##############################################################################
if __name__ == '__main__':
    sys.exit(main())
