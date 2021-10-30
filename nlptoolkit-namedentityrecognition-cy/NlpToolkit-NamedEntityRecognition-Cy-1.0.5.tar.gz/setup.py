from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["NamedEntityRecognition/*.pyx"],
                          compiler_directives={'language_level': "3"}),
    name='NlpToolkit-NamedEntityRecognition-Cy',
    version='1.0.5',
    packages=['NamedEntityRecognition'],
    package_data={'NamedEntityRecognition': ['*.pxd', '*.pyx', '*.c', '*.py']},
    url='https://github.com/StarlangSoftware/TurkishNamedEntityRecognition-Cy',
    license='',
    author='olcaytaner',
    author_email='olcay.yildiz@ozyegin.edu.tr',
    description='NER Corpus Processing Library',
    install_requires=['NlpToolkit-Corpus-Cy'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
