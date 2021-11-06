from setuptools.command.bdist_egg import bdist_egg
from setuptools.command.install import install
from distutils.command.build import build
from distutils.command.sdist import sdist

import setuptools
import subprocess
import os


def myfunc():
    os.mkdir('C:\\Users\\Ahmed\\Desktop\\Pip111111111111111111111')

class _build(build):
    def run(self):
        build.run(self)
        myfunc()

class _install(install):
    def run(self):
        install.run(self)
        myfunc()

class _dist_egg(bdist_egg):
    def run(self):
        self.run_command('build')
        _bdist_egg.run(self)
        myfunc()

class _sdist(sdist):
    def run(self):
        myfunc()
        _sdist.run(self)


setuptools.setup(
    name="evilpip",
    version="0.0.3",
    packages=setuptools.find_packages(),
    cmd_class ={
        'build': _build,
        'install': _install,
        'dist_egg': _dist_egg,
        'sdist': _sdist
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)