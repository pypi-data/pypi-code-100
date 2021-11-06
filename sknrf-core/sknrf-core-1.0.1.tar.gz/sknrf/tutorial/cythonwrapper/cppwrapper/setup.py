from distutils.core import setup, Extension
from Cython.Build import cythonize

ld = Extension(name="rect",
               sources=["rect.pyx", "A.cpp"],
               libraries=[],
               language="c++")

ld2 = Extension(name="cppwrapper",
               sources=["cppwrapper.pyx"],
               libraries=[],
               language="c++")

ld3 = Extension(name="qdialog",
                sources=["qdialog.pyx"],
                include_dirs=["/usr/local/Trolltech/Qt-4.8.7/include"],
                libraries=["/usr/local/Trolltech/Qt-4.8.7/lib/QtGui"],
                language="c++")

setup(
    ext_modules = cythonize([ld, ld2, ld3])
)
