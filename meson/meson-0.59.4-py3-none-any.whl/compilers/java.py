# Copyright 2012-2017 The Meson development team

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os.path
import shutil
import subprocess
import textwrap
import typing as T

from ..mesonlib import EnvironmentException, MachineChoice
from .compilers import Compiler, java_buildtype_args
from .mixins.islinker import BasicLinkerIsCompilerMixin

if T.TYPE_CHECKING:
    from ..envconfig import MachineInfo
    from ..environment import Environment

class JavaCompiler(BasicLinkerIsCompilerMixin, Compiler):

    language = 'java'

    def __init__(self, exelist: T.List[str], version: str, for_machine: MachineChoice,
                 info: 'MachineInfo', full_version: T.Optional[str] = None):
        super().__init__(exelist, version, for_machine, info, full_version=full_version)
        self.id = 'unknown'
        self.javarunner = 'java'

    def get_werror_args(self) -> T.List[str]:
        return ['-Werror']

    def get_output_args(self, subdir: str) -> T.List[str]:
        if subdir == '':
            subdir = './'
        return ['-d', subdir, '-s', subdir]

    def get_pic_args(self) -> T.List[str]:
        return []

    def get_pch_use_args(self, pch_dir: str, header: str) -> T.List[str]:
        return []

    def get_pch_name(self, name: str) -> str:
        return ''

    def get_buildtype_args(self, buildtype: str) -> T.List[str]:
        return java_buildtype_args[buildtype]

    def compute_parameters_with_absolute_paths(self, parameter_list: T.List[str],
                                               build_dir: str) -> T.List[str]:
        for idx, i in enumerate(parameter_list):
            if i in ['-cp', '-classpath', '-sourcepath'] and idx + 1 < len(parameter_list):
                path_list = parameter_list[idx + 1].split(os.pathsep)
                path_list = [os.path.normpath(os.path.join(build_dir, x)) for x in path_list]
                parameter_list[idx + 1] = os.pathsep.join(path_list)

        return parameter_list

    def sanity_check(self, work_dir: str, environment: 'Environment') -> None:
        src = 'SanityCheck.java'
        obj = 'SanityCheck'
        source_name = os.path.join(work_dir, src)
        with open(source_name, 'w', encoding='utf-8') as ofile:
            ofile.write(textwrap.dedent(
                '''class SanityCheck {
                  public static void main(String[] args) {
                    int i;
                  }
                }
                '''))
        pc = subprocess.Popen(self.exelist + [src], cwd=work_dir)
        pc.wait()
        if pc.returncode != 0:
            raise EnvironmentException('Java compiler %s can not compile programs.' % self.name_string())
        runner = shutil.which(self.javarunner)
        if runner:
            cmdlist = [runner, obj]
            pe = subprocess.Popen(cmdlist, cwd=work_dir)
            pe.wait()
            if pe.returncode != 0:
                raise EnvironmentException('Executables created by Java compiler %s are not runnable.' % self.name_string())
        else:
            m = "Java Virtual Machine wasn't found, but it's needed by Meson. " \
                "Please install a JRE.\nIf you have specific needs where this " \
                "requirement doesn't make sense, please open a bug at " \
                "https://github.com/mesonbuild/meson/issues/new and tell us " \
                "all about it."
            raise EnvironmentException(m)

    def needs_static_linker(self) -> bool:
        return False

    def get_optimization_args(self, optimization_level: str) -> T.List[str]:
        return []
