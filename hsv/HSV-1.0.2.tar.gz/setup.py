# BUILD THE PROJECT WITH THE CORRECT PYTHON VERSION
# pip install wheel

# python setup.py bdist_wheel
# OR python setup.py sdist bdist_wheel (to include the source)

# for python 3.8
# C:\Users\yoann\AppData\Roaming\Python\Python38\Scripts\twine upload
# --verbose --repository testpypi dist/HSV-1.0.3-cp38-cp38-win_amd64.whl

# for python 3.6
# C:\Users\yoann\AppData\Roaming\Python\Python36\Scripts\twine upload
# --verbose --repository testpypi dist/HSV-1.0.3-cp36-cp36-win_amd64.whl

# python setup.py bdist_wheel
# twine upload --verbose --repository testpypi dist/*

# PRODUCTION v:
# version 1.0.2
# C:\Users\yoann\AppData\Roaming\Python\Python38\Scripts\twine upload --verbose dist/HSV-1.0.2*

# CREATING EXECUTABLE
# pyinstaller --onefile pyinstaller_config.spec

import setuptools
from Cython.Build import cythonize
from setuptools import setup, Extension

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name                         ="HSV",
    version                      ="1.0.2",
    author                       ="Yoann Berenguer",
    author_email                 ="yoyoberenguer@hotmail.com",
    description                  ="HSV conversion tools",
    long_description             =long_description,
    long_description_content_type="text/markdown",
    url                          ="https://github.com/yoyoberenguer/HSV",
    packages                     =setuptools.find_packages(),
    ext_modules                  =cythonize([
        Extension("HSV.hsv", ["hsv.pyx"],
                  extra_compile_args=["/Qpar", "/fp:fast", "/O2", "/Oy", "/Ot"], language="c"),
        Extension("HSV.testing", ["testing.pyx"],
                  extra_compile_args=["/Qpar", "/fp:fast", "/O2", "/Oy", "/Ot"], language="c")]),
    license                      ='MIT',
    # classifiers                  =['License :: OSI Approved :: MIT License', ],

    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Cython',
        'Programming Language :: C',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        # 'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        # 'Programming Language :: Python :: 3 :: Only',
    ],

    install_requires=[
        'setuptools>=49.2.1',
        'Cython>=0.28'
    ],
    python_requires         ='>=3.0',
    platforms               =['any'],
    include_package_data    =True,
    data_files=[('./lib/site-packages/HSV',
                 ['example.py',
                  'hsv.pxd',
                  'hsv.pyx',
                  'hsv_c.c',
                  'LICENSE',
                  'MANIFEST.in',
                  'requirements.txt',
                  'setup_hsv.py',
                  # 'build/lib.win-amd64-3.8/
                  # 'build/lib.win-amd64-3.8/H
                  '__init__.pxd',
                  '__init__.py',
                  'testing.pyx',
                  'pyproject.toml',

                  ]),
                ('./lib/site-packages/HSV/test',
                 [
                  'test/HSV_testing.py',
                 ])
                ],

    project_urls = {  # Optional
                   'Bug Reports': 'https://github.com/yoyoberenguer/HSV/issues',
                   'Source'     : 'https://github.com/yoyoberenguer/HSV',
               },
)
