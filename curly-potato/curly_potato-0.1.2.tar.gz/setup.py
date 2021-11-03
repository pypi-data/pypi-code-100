from setuptools import setup
import curly_potato

setup(
    name='curly_potato',
    version=curly_potato.__version__,    
    description='An example Python package',
    url='https://github.com/UnrealEugene/curly_potato',
    author=curly_potato.__author__,
    author_email='chernatskiy2001@gmail.com',    
    license='BSD 2-clause',
    packages=['curly_potato'],
    
    install_requires=[
        'numpy>=1.21.0',
        'matplotlib',
    ],
    
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
