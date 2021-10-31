import os
from os.path import abspath, dirname
import re
import sys
import platform
import subprocess
from click import style
from colorama import init
from distutils.version import LooseVersion
from setuptools import Extension
from setuptools.command.build_ext import build_ext


class CMakeTarget(Extension):
    def __init__(self, name: str):
        Extension.__init__(self, name, sources=[])


class __CMakeProject(build_ext):
    source_dir: str = ...

    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the following extensions: " +
                ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(re.search(r'version\s*([\d.]+)',
                                         out.decode()).group(1))
            if cmake_version < '3.1.0':
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        print(style(f"Configuring CMake using {os.path.join(abspath(self.source_dir),'CMakeLists.txt')}", fg="cyan", bold=True))

        self.cfg = 'Debug' if self.debug else 'Release'
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath("foo"))) if not self.inplace else self.source_dir

        self.cmake_args = [
            '-DPYTHON_EXECUTABLE=' + sys.executable,
            '-DCMAKE_BUILD_TYPE=' + self.cfg,
            '-DSETUPTOOLS_CMAKE_DIR=' + dirname(__file__),
            '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
            '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(self.cfg.upper(), extdir),
        ]
        self.build_args = ['--config', self.cfg, ]
        self.build_args += ['--', '/m'] if platform.system() == "Windows" else ['--', '-j2']

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get('CXXFLAGS', ''), self.distribution.get_version())

        os.makedirs(self.build_temp, exist_ok=True)

        subprocess.check_call(['cmake', self.source_dir] + self.cmake_args, cwd=self.build_temp, env=env)

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext: CMakeTarget):
        print(style(f"Building extension '{ext.name}' and dependencies", fg="cyan", bold=True))
        subprocess.check_call(['cmake', '--build', '.', "--target", ext.name] + self.build_args, cwd=self.build_temp)
        print()


def cmake_project(source_directory: str):
    class __CmakeProjectClass(__CMakeProject):
        source_dir = abspath(source_directory)

    return __CmakeProjectClass


init()
