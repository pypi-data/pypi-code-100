from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension

ext_modules = [
    Extension("cythonex",
              sources=["cythonex.pyx"],
              libraries=["m"] # Unix-like specific
              )
]
setup(
    ext_modules = cythonize(ext_modules)
)