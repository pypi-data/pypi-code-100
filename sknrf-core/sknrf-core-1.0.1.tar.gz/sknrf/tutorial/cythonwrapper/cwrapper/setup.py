from distutils.core import setup, Extension
from Cython.Build import cythonize

ld = Extension(name="cwrapper",
               sources=["cwrapper.pyx"],
               libraries=["calg"])

setup(
    ext_modules = cythonize([ld])
)
