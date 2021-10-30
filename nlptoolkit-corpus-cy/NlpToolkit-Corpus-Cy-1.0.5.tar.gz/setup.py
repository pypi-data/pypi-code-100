from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["Corpus/*.pyx"],
                          compiler_directives={'language_level': "3"}),
    name='NlpToolkit-Corpus-Cy',
    version='1.0.5',
    packages=['Corpus'],
    package_data={'Corpus': ['*.pxd', '*.pyx', '*.c', '*.py']},
    url='https://github.com/StarlangSoftware/Corpus-Cy',
    license='',
    author='olcaytaner',
    author_email='olcay.yildiz@ozyegin.edu.tr',
    description='Corpus library',
    install_requires=['NlpToolkit-Dictionary-Cy'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
