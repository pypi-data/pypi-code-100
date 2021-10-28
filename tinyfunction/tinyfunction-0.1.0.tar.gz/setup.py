from setuptools import setup

setup(
    name='tinyfunction',
    version='0.1.0',    
    description='A simple and tiny function python lib',
    url='https://github.com/prakis/tinyfunction-pip',
    author='Kishore',
    author_email='prakis@gmail.com',
    license='BSD 2-clause',
    packages=['tinyfunction'],
    install_requires=['mpi4py>=2.0',
                      'numpy',                     
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