"""
For pip install installation.
"""

import os
import fnmatch

from numpy.distutils.command.sdist import sdist
import setuptools

from numpy.distutils.core import setup, numpy_cmdclass
from numpy.distutils.misc_util import Configuration

class sdist_checked(sdist):
    def run(self):
        sdist.run(self)

def ext_modules(config, _dir):
    """Fetch f90 files in src and automatically create an extension"""
    pattern = "*.f90"
    if os.path.isdir(_dir):
        for root, dirs, files in os.walk(_dir):
            match = fnmatch.filter(files, pattern)
            for name in match:
                f90_file = os.path.join(root, name)
                ext_name = os.path.splitext(f90_file)[0].replace("/", ".")
                config.add_extension(ext_name,
                                     [f90_file],
                                     f2py_options=['--quiet']
                                    )

with open('README.rst', 'r') as summary:
    LONG_DESCRIPTION = summary.read()

def run_setup():
    """Setup"""
    config = Configuration(None, '', '')
    ext_modules(config, "wurp")
    config.add_data_files(os.path.join("wurp", "LICENSE-short.txt"))
    setup(
        name="Wurp",
        version="1.2",
        author="Yamato's Lab",
        author_email="yamato@nagoya-u.jp",
        description="Inter-residue Current calculation in Proteins from MD \
            trajectory",
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/x-rst',
        url=("https://gitlab.com/yamato97/current-calculations-for-proteins"),
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Science/Research",
            "Operating System :: MacOS",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Fortran",
            "Topic :: Scientific/Engineering",
            "Topic :: Scientific/Engineering :: Bio-Informatics",
            "Topic :: Scientific/Engineering :: Physics",
            "Topic :: Scientific/Engineering :: Chemistry"
            ],
        cmdclass={"sdist": sdist_checked},

        install_requires=["numpy>=1.11.2,<1.17",
                          "nose",
                          "mpi4py>=2.0",
                          "benchmarker",
                          "pygraphviz<1.6",
                          "netCDF4>=1.2.4"],

        packages=setuptools.find_packages(),

        package_data={'wurp':['volume/random20.pdb.gz']},

        python_requires=">=2.7, <3.0",
        entry_points={
            "console_scripts": [
                "wurp = wurp.console:main",
                ]
            },
        **config.todict()
        )

if __name__ == '__main__':
    run_setup()
