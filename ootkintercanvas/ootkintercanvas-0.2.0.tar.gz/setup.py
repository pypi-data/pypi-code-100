from setuptools import setup

# https://betterscientificsoftware.github.io/python-for-hpc/tutorials/python-pypi-packaging/
setup(
    name='ootkintercanvas',
    version='0.2.0',
    description='An Object Oriented Extention for tkinter Canvas',
    url='https://gitlab.com/esrari/ootkintercanvas',
    author='Alireza Esrari',
    author_email='alireza.esrari@gmail.com',
    license='BSD 2-clause',
    packages=['ootkintercanvas'],
    install_requires=['tk',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Topic :: Multimedia :: Graphics :: Editors :: Vector-Based',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Version Control :: Git',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.8',
    ],
)
