# SPDX-License-Identifier: Apache-2.0
# Copyright © 2021 Intel Corporation

"""Abstraction for Cython language compilers."""

import typing as T

from .. import coredata
from ..mesonlib import EnvironmentException, OptionKey
from .compilers import Compiler

if T.TYPE_CHECKING:
    from ..coredata import KeyedOptionDictType
    from ..environment import Environment


class CythonCompiler(Compiler):

    """Cython Compiler."""

    language = 'cython'
    id = 'cython'

    def needs_static_linker(self) -> bool:
        # We transpile into C, so we don't need any linker
        return False

    def get_always_args(self) -> T.List[str]:
        return ['--fast-fail']

    def get_werror_args(self) -> T.List[str]:
        return ['-Werror']

    def get_output_args(self, outputname: str) -> T.List[str]:
        return ['-o', outputname]

    def get_optimization_args(self, optimization_level: str) -> T.List[str]:
        # Cython doesn't have optimization levels itself, the underlying
        # compiler might though
        return []

    def sanity_check(self, work_dir: str, environment: 'Environment') -> None:
        code = 'print("hello world")'
        with self.cached_compile(code, environment.coredata) as p:
            if p.returncode != 0:
                raise EnvironmentException(f'Cython compiler {self.id!r} cannot compile programs')

    def get_buildtype_args(self, buildtype: str) -> T.List[str]:
        # Cython doesn't implement this, but Meson requires an implementation
        return []

    def get_pic_args(self) -> T.List[str]:
        # We can lie here, it's fine
        return []

    def compute_parameters_with_absolute_paths(self, parameter_list: T.List[str],
                                               build_dir: str) -> T.List[str]:
        new: T.List[str] = []
        for i in parameter_list:
            new.append(i)

        return new

    def get_options(self) -> 'KeyedOptionDictType':
        opts = super().get_options()
        opts.update({
            OptionKey('version', machine=self.for_machine, lang=self.language): coredata.UserComboOption(
                'Python version to target',
                ['2', '3'],
                '3',
            )
        })
        return opts

    def get_option_compile_args(self, options: 'KeyedOptionDictType') -> T.List[str]:
        args: T.List[str] = []
        key = options[OptionKey('version', machine=self.for_machine, lang=self.language)]
        args.append(f'-{key.value}')
        return args
