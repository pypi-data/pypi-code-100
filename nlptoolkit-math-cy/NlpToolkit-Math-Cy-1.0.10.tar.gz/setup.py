from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["Math/*.pyx", "Math/*.pxd"],
                          compiler_directives={'language_level': "3"}),
    name='NlpToolkit-Math-Cy',
    version='1.0.10',
    packages=['Math'],
    package_data={'Math': ['*.pxd', '*.pyx', '*.c']},
    url='https://github.com/StarlangSoftware/Math-Cy',
    license='',
    author='olcaytaner',
    author_email='olcay.yildiz@ozyegin.edu.tr',
    description='Math library',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
