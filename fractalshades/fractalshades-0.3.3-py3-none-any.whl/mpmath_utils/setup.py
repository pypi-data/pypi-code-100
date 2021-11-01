"A minimal setup.py for compiling test_gmpy2.pyx"

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import sys

ext = Extension(
    "test_gmpy2",
    ["test_gmpy2.pyx"],
    include_dirs=sys.path,
    libraries=['gmp', 'mpfr', 'mpc'],
)

setup(
    name="cython_gmpy_test",
    ext_modules=cythonize([ext], include_path=sys.path, language_level = "3"),
)
