from setuptools import setup, find_packages
import os


# extract version
with open(os.path.join(os.path.dirname(__file__),
                       "fitmulticell", "version.py")) as f:
    version = f.read().split("\n")[0].split("=")[-1].strip(' ').strip('"')


# read a file
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="fitmulticell",
    version=version,
    python_requires='>=3.7.1',
    install_requires=[
        'numpy>=1.16.2', 'scipy>=1.2.1', 'pandas>=0.25.0', 'matplotlib',
        'pyabc', 'imageio', 'PEtab_MS>=0.1.19'
    ],
    extra_requires={},
    packages=find_packages(exclude=["doc", "test*"]),
    author="The FitMultiCell developers",
    author_email='yannik.schaelte@gmail.com',
    platforms='all',
    url="https://gitlab.com/fitmulticell/fit",
    description="Tool for fitting multi-cellular models",
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
    ],
    license='BSD-3-Clause',
    keywords='fitmulticell, morpheus, pyabc, likelihood-free, '
             'approximate bayesian computation, abc',
)
