"""
Setuptools based setup module
"""
from setuptools import setup, find_packages
import versioneer

setup(
    name='aproc',
    version=versioneer.get_version(),
    description='aproc - for asynchronous multiprocessing',
    long_description='aproc extends the multiprocessing library by combining a multiprocessing pool '
                     'with a multiprocessing queue',
    url='https://github.com/pyiron/aproc',
    author='Jan Janssen',
    author_email='janssen@mpie.de',
    license='BSD',

    classifiers=['Development Status :: 5 - Production/Stable',
                 'Topic :: Scientific/Engineering :: Physics',
                 'License :: OSI Approved :: BSD License',
                 'Intended Audience :: Science/Research',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 'Programming Language :: Python :: 3.9'
                ],

    keywords='aproc',
    packages=find_packages(exclude=["*tests*", "*binder*", "*notebooks*"]),
    cmdclass=versioneer.get_cmdclass(),
    )
