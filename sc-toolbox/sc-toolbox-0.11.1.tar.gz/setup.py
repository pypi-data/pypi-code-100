# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sc_toolbox',
 'sc_toolbox.api',
 'sc_toolbox.api.calc',
 'sc_toolbox.api.plot',
 'sc_toolbox.api.util',
 'sc_toolbox.cli',
 'sc_toolbox.cli.commands']

package_data = \
{'': ['*'],
 'sc_toolbox.api.calc': ['markers/*'],
 'sc_toolbox.cli.commands': ['templates/simple_docker/*',
                             'templates/simple_docker/{{ '
                             'cookiecutter.project_slug }}/*']}

install_requires = \
['Jinja2>=2.11.3',
 'PyYAML>=5.4.1',
 'adjustText>=0.7.3',
 'click>=7.0.0',
 'cookiecutter>=1.7.2',
 'matplotlib>=3.4.1',
 'pandas>=1.2.4',
 'questionary>=1.9.0',
 'requests>=2.25.1',
 'rich>=10.1.0',
 'scanpy>=1.7.2',
 'scikit-learn>=0.24.1',
 'scipy>=1.6.3',
 'seaborn>=0.11.1',
 'typing-extensions>=3.10.0']

entry_points = \
{'console_scripts': ['sc-toolbox = sc_toolbox.__main__:main']}

setup_kwargs = {
    'name': 'sc-toolbox',
    'version': '0.11.1',
    'description': 'A collection of project templates and useful code snippets for single-cell data analysis with Scanpy.',
    'long_description': ".. image:: https://user-images.githubusercontent.com/21954664/116578141-65a85180-a911-11eb-9c33-925a2ec600c6.png\n    :target: https://github.com/schillerlab/sc-toolbox\n    :alt: sc-toolbox logo\n    :align: center\n    :width: 200px\n\n\nsc-toolbox\n==========\n\n|PyPI| |Downloads| |Python Version| |License| |Read the Docs| |Build| |Tests| |Codecov| |pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/sc-toolbox.svg\n   :target: https://pypi.org/project/sc-toolbox/\n   :alt: PyPI\n.. |Downloads| image:: https://pepy.tech/badge/sc-toolbox\n    :target: https://pepy.tech/badge/sc-toolbox\n    :alt: PyPI Downloads\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/sc-toolbox\n   :target: https://pypi.org/project/sc-toolbox\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/github/license/schillerlab/sc-toolbox\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/sc-toolbox/latest.svg?label=Read%20the%20Docs\n   :target: https://sc-toolbox.readthedocs.io/\n   :alt: Read the documentation at https://sc-toolbox.readthedocs.io/\n.. |Build| image:: https://github.com/schillerlab/sc-toolbox/workflows/Build%20sc-toolbox%20Package/badge.svg\n   :target: https://github.com/schillerlab/sc-toolbox/actions?workflow=Package\n   :alt: Build Package Status\n.. |Tests| image:: https://github.com/schillerlab/sc-toolbox/workflows/Run%20sc-toolbox%20Tests/badge.svg\n   :target: https://github.com/schillerlab/sc-toolbox/actions?workflow=Tests\n   :alt: Run Tests Status\n.. |Codecov| image:: https://codecov.io/gh/schillerlab/sc-toolbox/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/schillerlab/sc-toolbox\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n.. warning::\n    This package is still under heavy development. It is primarily designed for in-house analyses at the `Theislab <https://github.com/theislab>`_\n    and `Schillerlab <https://github.com/schillerlab>`_. Don't yet expect it to be well tested or documented.\n    However, contributions are highly welcome and we will provide guidance if required.\n\n\nFeatures\n--------\n\n* Create minimal best-practice containers for single-cell data analysis with Scanpy\n* API for advanced Scanpy based plots and analyses\n\n.. figure:: https://user-images.githubusercontent.com/21954664/116225631-5fb84200-a752-11eb-9489-16571428918f.png\n   :alt: Preview plot\n\n.. figure:: https://user-images.githubusercontent.com/21954664/116225765-824a5b00-a752-11eb-8cbf-c14ebd9ac030.png\n   :alt: Preview plot 2\n\n.. figure:: https://user-images.githubusercontent.com/21954664/116226005-c5a4c980-a752-11eb-9846-8dc72315d373.png\n   :alt: Preview plot 3\n\nInstallation\n------------\n\nYou can install *sc-toolbox* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install sc-toolbox\n\nUsage\n-----\n\n.. code:: python\n\n   import sc_toolbox.api as sct\n\nPlease see the `Usage documentation <Usage_>`_.\n\nCredits\n-------\n\nThis package was created with cookietemple_ using cookiecutter_ based on Hypermodern_Python_Cookiecutter_.\nMost scripts were developed by `Meshal Ansari <https://github.com/mesh09/>`_ and the package was designed by `Lukas Heumos <https://github.com/zethson>`_.\n\n.. _cookietemple: https://cookietemple.com\n.. _cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT: http://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern_Python_Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _pip: https://pip.pypa.io/\n.. _Usage: https://sc-toolbox.readthedocs.io/en/latest/usage.html\n.. _API: https://sc-toolbox.readthedocs.io/en/latest/api.html\n",
    'author': 'Lukas Heumos',
    'author_email': 'lukas.heumos@posteo.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/schillerlab/sc-toolbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
