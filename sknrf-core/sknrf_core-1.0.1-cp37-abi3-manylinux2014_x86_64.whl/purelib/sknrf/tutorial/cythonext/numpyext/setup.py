from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy as np

ld = Extension(name="numpyext",
               sources=["numpyext.pyx"],
               include_dirs=[np.get_include()],
               compiler_directives={'language_level': 3})

setup(
    ext_modules = cythonize([ld])
)