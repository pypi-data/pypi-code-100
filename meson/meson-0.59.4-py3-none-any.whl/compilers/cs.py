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

import os.path, subprocess
import textwrap
import typing as T

from ..mesonlib import EnvironmentException
from ..linkers import RSPFileSyntax

from .compilers import Compiler, MachineChoice, mono_buildtype_args
from .mixins.islinker import BasicLinkerIsCompilerMixin

if T.TYPE_CHECKING:
    from ..envconfig import MachineInfo
    from ..environment import Environment

cs_optimization_args = {'0': [],
                        'g': [],
                        '1': ['-optimize+'],
                        '2': ['-optimize+'],
                        '3': ['-optimize+'],
                        's': ['-optimize+'],
                        }  # type: T.Dict[str, T.List[str]]


class CsCompiler(BasicLinkerIsCompilerMixin, Compiler):

    language = 'cs'

    def __init__(self, exelist: T.List[str], version: str, for_machine: MachineChoice,
                 info: 'MachineInfo', comp_id: str, runner: T.Optional[str] = None):
        super().__init__(exelist, version, for_machine, info)
        self.id = comp_id
        self.runner = runner

    @classmethod
    def get_display_language(cls) -> str:
        return 'C sharp'

    def get_always_args(self) -> T.List[str]:
        return ['/nologo']

    def get_linker_always_args(self) -> T.List[str]:
        return ['/nologo']

    def get_output_args(self, fname: str) -> T.List[str]:
        return ['-out:' + fname]

    def get_link_args(self, fname: str) -> T.List[str]:
        return ['-r:' + fname]

    def get_werror_args(self) -> T.List[str]:
        return ['-warnaserror']

    def get_pic_args(self) -> T.List[str]:
        return []

    def compute_parameters_with_absolute_paths(self, parameter_list: T.List[str],
                                               build_dir: str) -> T.List[str]:
        for idx, i in enumerate(parameter_list):
            if i[:2] == '-L':
                parameter_list[idx] = i[:2] + os.path.normpath(os.path.join(build_dir, i[2:]))
            if i[:5] == '-lib:':
                parameter_list[idx] = i[:5] + os.path.normpath(os.path.join(build_dir, i[5:]))

        return parameter_list

    def get_pch_use_args(self, pch_dir: str, header: str) -> T.List[str]:
        return []

    def get_pch_name(self, header_name: str) -> str:
        return ''

    def sanity_check(self, work_dir: str, environment: 'Environment') -> None:
        src = 'sanity.cs'
        obj = 'sanity.exe'
        source_name = os.path.join(work_dir, src)
        with open(source_name, 'w', encoding='utf-8') as ofile:
            ofile.write(textwrap.dedent('''
                public class Sanity {
                    static public void Main () {
                    }
                }
                '''))
        pc = subprocess.Popen(self.exelist + self.get_always_args() + [src], cwd=work_dir)
        pc.wait()
        if pc.returncode != 0:
            raise EnvironmentException('C# compiler %s can not compile programs.' % self.name_string())
        if self.runner:
            cmdlist = [self.runner, obj]
        else:
            cmdlist = [os.path.join(work_dir, obj)]
        pe = subprocess.Popen(cmdlist, cwd=work_dir)
        pe.wait()
        if pe.returncode != 0:
            raise EnvironmentException('Executables created by Mono compiler %s are not runnable.' % self.name_string())

    def needs_static_linker(self) -> bool:
        return False

    def get_buildtype_args(self, buildtype: str) -> T.List[str]:
        return mono_buildtype_args[buildtype]

    def get_debug_args(self, is_debug: bool) -> T.List[str]:
        return ['-debug'] if is_debug else []

    def get_optimization_args(self, optimization_level: str) -> T.List[str]:
        return cs_optimization_args[optimization_level]


class MonoCompiler(CsCompiler):
    def __init__(self, exelist: T.List[str], version: str, for_machine: MachineChoice,
                 info: 'MachineInfo'):
        super().__init__(exelist, version, for_machine, info, 'mono',
                         runner='mono')

    def rsp_file_syntax(self) -> 'RSPFileSyntax':
        return RSPFileSyntax.GCC


class VisualStudioCsCompiler(CsCompiler):
    def __init__(self, exelist: T.List[str], version: str, for_machine: MachineChoice,
                 info: 'MachineInfo'):
        super().__init__(exelist, version, for_machine, info, 'csc')

    def get_buildtype_args(self, buildtype: str) -> T.List[str]:
        res = mono_buildtype_args[buildtype]
        if not self.info.is_windows():
            tmp = []
            for flag in res:
                if flag == '-debug':
                    flag = '-debug:portable'
                tmp.append(flag)
            res = tmp
        return res

    def rsp_file_syntax(self) -> 'RSPFileSyntax':
        return RSPFileSyntax.MSVC
