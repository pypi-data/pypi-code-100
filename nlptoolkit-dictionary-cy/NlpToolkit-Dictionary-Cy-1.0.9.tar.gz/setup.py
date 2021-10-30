from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["Dictionary/*.pyx", "Dictionary/Trie/*.pyx", "Language/*.pyx", "Syllibification/*.pyx"],
                          compiler_directives={'language_level': "3"}),
    name='NlpToolkit-Dictionary-Cy',
    version='1.0.9',
    packages=['Language', 'Dictionary', 'Dictionary.Trie', 'Syllibification'],
    package_data={'Language': ['*.pxd', '*.pyx', '*.c'],
                  'Dictionary': ['*.pxd', '*.pyx', '*.c', '*.py'],
                  'Dictionary.Trie': ['*.pxd', '*.pyx', '*.c'],
                  'Syllibification': ['*.pxd', '*.pyx', '*.c']},
    url='https://github.com/StarlangSoftware/Dictionary-Cy',
    license='',
    author='olcaytaner',
    author_email='olcay.yildiz@ozyegin.edu.tr',
    description='Simple Dictionary Processing',
    install_requires=['NlpToolkit-Math-Cy'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
