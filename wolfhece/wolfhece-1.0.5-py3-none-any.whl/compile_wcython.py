from distutils.core import Extension,setup
from Cython.Build import cythonize

ext=Extension(name="wolfogl", sources=["WolfOGL.pyx"], libraries = ['opengl32']) #, extra_compile_args=['-O3'])
setup(
    #name="DefCOpenGL"
    #ext_modules =  cythonize("cOpenGL.pyx")
    ext_modules =  cythonize(ext)
)

#Launch --> python compile_wcython.py build_ext --inplace
# In a Pyhton environment !!