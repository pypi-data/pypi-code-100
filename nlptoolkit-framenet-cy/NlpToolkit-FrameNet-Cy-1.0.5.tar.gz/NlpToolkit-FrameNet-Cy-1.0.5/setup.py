from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["FrameNet/*.pyx"],
                          compiler_directives={'language_level': "3"}),
    name='NlpToolkit-FrameNet-Cy',
    version='1.0.5',
    packages=['FrameNet'],
    package_data={'FrameNet': ['*.pxd', '*.pyx', '*.c', '*.py']},
    url='https://github.com/StarlangSoftware/TurkishFrameNet-Cy',
    license='',
    author='olcaytaner',
    author_email='olcay.yildiz@ozyegin.edu.tr',
    description='FrameNet library',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
