#!/usr/bin/env python
# -*- coding: utf-8 -*-

setup_packages = ['bob.extension']
bob_packages = []

from setuptools import setup, dist, find_packages, distutils
dist.Distribution(dict(setup_requires=setup_packages + bob_packages))

# from bob.extension import Extension, build_ext
from pybind11.setup_helpers import Pybind11Extension, build_ext

import sys

# load the requirements.txt for additional requirements
from bob.extension.utils import load_requirements
requirements = setup_packages + bob_packages + load_requirements()

version = open("version.txt").read().rstrip()

def has_flag(compiler, flagname):
    """Return a boolean indicating whether a flag name is supported on
    the specified compiler.
    """
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.cpp') as f:
        f.write('int main (int argc, char **argv) { return 0; }')
        try:
            compiler.compile([f.name], extra_postargs=[flagname])
        except distutils.errors.CompileError:
            return False
    return True


def cpp_flag(compiler):
    """Return the -std=c++[11/14/17] compiler flag.
    The newer version is prefered over c++11 (when it is available).
    """
    flags = ['-std=c++14', '-std=c++11']

    for flag in flags:
        if has_flag(compiler, flag): return flag

    raise RuntimeError('Unsupported compiler -- at least C++11 support '
                       'is needed!')

class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""
    c_opts = {
        'msvc': ['/EHsc'],
        'unix': [],
    }
    l_opts = {
        'msvc': [],
        'unix': [],
    }

    if sys.platform == 'darwin':
        darwin_opts = ['-stdlib=libc++', '-mmacosx-version-min=10.12']
        c_opts['unix'] += darwin_opts
        l_opts['unix'] += darwin_opts

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        link_opts = self.l_opts.get(ct, [])
        if ct == 'unix':
            opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
            opts.append(cpp_flag(self.compiler))
            if has_flag(self.compiler, '-fvisibility=hidden'):
                opts.append('-fvisibility=hidden')
        elif ct == 'msvc':
            opts.append('/DVERSION_INFO=\\"%s\\"' % self.distribution.get_version())
        for ext in self.extensions:
            ext.extra_compile_args = opts
            ext.extra_link_args = link_opts
        build_ext.build_extensions(self)


setup(

    name='bob.ip.stereo',
    version=open("version.txt").read().rstrip(),
    description='Stereo matching and image reprojection',
    url='https://gitlab.idiap.ch/bob/bob.ip.stereo',
    license='GPLv3',

    # there may be multiple authors (separate entries by comma)
    author='David Geissbühler',
    author_email='david.geissbuhler@idiap.ch',

    # there may be a maintainer apart from the author - you decide
    #maintainer='?'
    #maintainer_email='email@example.com'

    # you may add more keywords separating those by commas (a, b, c, ...)
    keywords = "bob, stereo",

    long_description=open('README.rst').read(),

    # leave this here, it is pretty standard
    packages=find_packages(),
    include_package_data=True,
    zip_safe = False,

    install_requires=requirements,

    # We are defining two extensions here. Each of them will be compiled
    # independently into a separate .so file.
    ext_modules = 
    [

      # The second extension contains the actual C++ code and the Python bindings
      Pybind11Extension("bob.ip.stereo._library",
        # list of files compiled into this extension
        [
          # the pure C++ code
          "bob/ip/stereo/reproject.cpp"
        ],
        # additional parameters, see Extension documentation
        version = version,
        bob_packages = bob_packages,
      ),
    ],

    cmdclass={'build_ext': BuildExt},

    entry_points={
      # scripts should be declared using this entry:
      'console_scripts': [
        'stereo_matcher.py = bob.ip.stereo.stereo_matcher:main',
        'calibration.py = bob.ip.stereo.calibration:main',
        'warp_calibration.py = bob.ip.stereo.warp_calibration:main',
      ],
    },

    # check classifiers, add and remove as you see fit
    # full list here: https://pypi.org/classifiers/
    # don't remove the Bob framework unless it's not a bob package
    classifiers = [
      'Framework :: Bob',
      'Development Status :: 4 - Beta',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Natural Language :: English',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      'Topic :: Scientific/Engineering :: Artificial Intelligence',
      'Topic :: Software Development :: Libraries :: Python Modules',
      ],

)