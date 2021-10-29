# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libsv']

package_data = \
{'': ['*'],
 'libsv': ['counters/*',
           'decoders/*',
           'encoders/*',
           'latches/*',
           'math/*',
           'muxes/*']}

setup_kwargs = {
    'name': 'libsv',
    'version': '0.1.0',
    'description': 'An open source parameterized SystemVerilog hardware IP library',
    'long_description': '.. image:: https://raw.githubusercontent.com/bensampson5/libsv/main/docs/source/_images/libsv_logo.svg\n   :align: center\n   :height: 150\n   :alt: LibSV\n\n------------------------------------------------------------------------------------------------------------------------\n\n.. image:: https://img.shields.io/pypi/v/libsv\n   :target: https://pypi.org/project/libsv/\n   :alt: PyPI\n\n.. image:: https://github.com/bensampson5/libsv/actions/workflows/ci.yml/badge.svg\n   :target: https://github.com/bensampson5/libsv/actions/workflows/ci.yml\n\n.. image:: https://readthedocs.org/projects/libsv/badge/?version=latest\n   :target: https://libsv.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n\nWelcome to LibSV! `Click here to go to LibSV’s\ndocumentation <https://libsv.readthedocs.io/en/latest/>`_.\n\nLibSV is an open source, parameterized SystemVerilog digital hardware IP library.\nWhile similar libraries may already exist, LibSV is unique in that it takes advantage\nof open-source, state-of-the-art development best practices and tools from across the\nsoftware and digital design community, including:\n\n* Trivial installation. `LibSV is hosted on PyPI <https://pypi.org/project/libsv/>`_ and can easily be installed using \n  `pip <https://pip.pypa.io/en/stable/>`_ or whichever Python package manager of your choice.\n* Easy-to-use. Simply add ```include "libsv/<path>/<to>/<module>.sv"`` to the top of your sourcefile and then add the\n  ``site-packages/`` folder, where LibSV was installed, to the include path when you go to build your project.\n* Automated testbenches, written in Python, that use `pytest <https://github.com/pytest-dev/pytest>`_ to run\n  `Cocotb <https://github.com/cocotb/cocotb>`_ + `Verilator <https://github.com/verilator/verilator>`_ under the hood for \n  simple and fast logic simulation\n* All testbenches output waveform files in FST format for viewing with `GTKWave <http://gtkwave.sourceforge.net/>`_\n* `Extensive documention <https://libsv.readthedocs.io/en/latest/>`_ using `Sphinx <https://www.sphinx-doc.org/en/master/>`_\n  that includes circuit schematics for each module\n* Automated formatting and lint checks using `Verible <https://github.com/google/verible>`_\n* `Continuous integration (CI) workflows <https://github.com/bensampson5/libsv/actions>`_ integrated with \n  `Docker <https://www.docker.com/>`_\n* `LibSV Docker images <https://hub.docker.com/repository/docker/bensampson5/libsv>`_ published to\n  `Docker Hub <https://hub.docker.com/>`_\n\nGetting Started\n---------------\n\nLibSV is very easy to use. First, install the ``libsv`` package from PyPI:\n\n.. code-block:: bash\n\n  pip install libsv\n\nWe recommend using a Python virtual environment so that the installation is project-specific and\nisolated from the rest of your system.\n\nThen add the ``site-packages/`` folder, where LibSV was just installed, to your include path when building your\nproject so that your design tools can find LibSV.\n\nFinally, at the top of your design file where you want to use LibSV modules, for each module you want to use, add:\n\n.. code-block:: SystemVerilog\n\n  `include "libsv/<path>/<to>/<module>.sv"\n\nRunning Testbenches\n-------------------\n\nRunning the LibSV testbenches require `Cocotb <https://github.com/cocotb/cocotb>`_, \n`Verilator <https://github.com/verilator/verilator>`_, and a number of other dependencies to be installed.\nInstead of trying to install everything manually on your machine, the easier and recommended way to run the\nLibSV testbenches is to use the pre-built \n`LibSV Docker images on Docker Hub <https://hub.docker.com/repository/docker/bensampson5/libsv>`__ that have the\ncomplete set of LibSV developer tools already installed.\n\nTo use a LibSV Docker image, first you’ll need to install `Docker <https://www.docker.com/get-started>`__, \nif you don’t already have it.\n\nNext, pull the latest LibSV Docker image:\n\n.. code-block:: bash\n\n  docker build --pull -f Dockerfile.dev \\\n    --build-arg UID=$(id -u) \\\n    --build-arg GID=$(id -g) \\\n    -t libsv .\n\nThen, start a new Docker container using the LibSV image and mount the project folder to the container:\n\n.. code-block:: bash\n\n  docker run --rm -it -v $(pwd):/code libsv\n\nFinally, within the Docker container, run ``pytest``:\n\n.. code-block:: bash\n\n  pytest\n\nThis will run all the LibSV testbenches for the entire library (*Warning: This may take a while!*).\n\nInstead, to list all the available LibSV testbenches, run:\n\n.. code-block:: bash\n\n  pytest --co\n\nThen, you can run an individual or subset of testbenches using the ``-k`` flag which will only run tests which\nmatch the given substring expression:\n\n.. code-block:: bash\n\n  pytest -k EXPRESSION\n\nEach testbench generates an associated ``.fst`` waveform file that is written to the ``build/`` directory and can be\nviewed using `GTKWave <http://gtkwave.sourceforge.net/>`_.\n\nBugs/Feature Requests\n---------------------\n\nPlease use `LibSV\'s GitHub issue tracker <https://github.com/bensampson5/libsv/issues>`_ to submit bugs or request features.\n\nContributing\n------------\n\nContributions are much welcomed and appreciated! Take a look at the Contributing page to get started.\n\nLicense\n-------\n\nDistributed under the terms of the `MIT <https://github.com/bensampson5/libsv/blob/main/LICENSE>`_ license, LibSV is free\nand open source software.',
    'author': 'Ben Sampson',
    'author_email': 'bensampson5@gmail.com',
    'maintainer': 'Ben Sampson',
    'maintainer_email': 'bensampson5@gmail.com',
    'url': 'https://libsv.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
