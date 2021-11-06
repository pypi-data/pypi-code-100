from distutils.core import setup, Extension
from Cython.Build import cythonize

ld = Extension(name="pythonext",
               sources=["pythonext.pyx"],
               include_dirs=[],
               compiler_directives={'language_level': 3}
               )

setup(
    ext_modules = cythonize([ld])
)