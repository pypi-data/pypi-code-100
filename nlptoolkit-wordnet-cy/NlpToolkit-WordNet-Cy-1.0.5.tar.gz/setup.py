from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["WordNet/*.pyx", "WordNet/Similarity/*.pyx"],
                          compiler_directives={'language_level': "3"}),
    name='NlpToolkit-WordNet-Cy',
    version='1.0.5',
    packages=['WordNet', 'WordNet.Similarity'],
    package_data={'WordNet': ['*.pxd', '*.pyx', '*.c', '*.py'],
                  'WordNet.Similarity': ['*.pxd', '*.pyx', '*.c']},
    url='https://github.com/StarlangSoftware/TurkishWordNet-Cy',
    license='',
    author='olcay',
    author_email='olcay.yildiz@ozyegin.edu.tr',
    description='Turkish WordNet KeNet',
    install_requires=['NlpToolkit-MorphologicalAnalysis-Cy'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
