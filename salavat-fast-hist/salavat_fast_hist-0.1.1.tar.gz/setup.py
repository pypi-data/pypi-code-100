from setuptools import setup
from setuptools import find_packages

setup(
    name='salavat_fast_hist',
    version='0.1.1',    
    description='A example Python package',
    url='',
    author='Salavat Mukhamedzhanov',
    author_email='',
    license='BSD 2-clause',
    install_requires=['numpy<=1.15.0'],                     
    packages=['src'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
