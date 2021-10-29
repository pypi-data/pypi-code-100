# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geolib',
 'geolib.geometry',
 'geolib.models',
 'geolib.models.dfoundations',
 'geolib.models.dsettlement',
 'geolib.models.dsheetpiling',
 'geolib.models.dstability',
 'geolib.service',
 'geolib.soils']

package_data = \
{'': ['*'],
 'geolib.models.dfoundations': ['soil_csv/*', 'templates/*'],
 'geolib.models.dsettlement': ['templates/*'],
 'geolib.models.dsheetpiling': ['templates/*']}

install_requires = \
['jinja2>=2.11.2,<3.0.0',
 'jsonschema>=3.2,<4.0',
 'pydantic[dotenv]>=1.6.1,<1.7.0',
 'requests>=2.24.0,<3.0.0',
 'zipp>=3.1.0,<4.0.0']

extras_require = \
{'server': ['fastapi>=0.58.1,<0.59.0', 'uvicorn>=0.11.5,<0.12.0']}

entry_points = \
{'console_scripts': ['geolib_server = geolib.service.main:app']}

setup_kwargs = {
    'name': 'd-geolib',
    'version': '0.1.6',
    'description': 'Python wrappers around the input and output files of the Deltares D-Serie models',
    'long_description': 'GEOLib\n=============================\n\nGEOLib is a Python package to generate, execute and parse several D-Serie numerical models.\n\nRequirements\n------------\n\nTo install the required dependencies to run GEOLib code, run:\n\n.. code-block:: bash\n\n    $ pip install -r requirements\n\nOr, when having poetry installed (you should):\n\n.. code-block:: bash\n\n    $ poetry install\n\n\nTesting & Development\n---------------------\n\nMake sure to have the server dependencies installed: \n\n.. code-block:: bash\n\n    $ poetry install -E server\n\nIn order to run the testcode, from the root of the repository, run:\n\n.. code-block:: bash\n\n    $ pytest\n\nor, in case of using Poetry\n\n.. code-block:: bash\n\n    $ poetry run pytest\n\nRunning flake8, mypy is also recommended. For mypy use:\n\n.. code-block:: bash\n\n    $ mypy --config-file pyproject.toml geolib\n\n\nDocumentation\n-------------\n\nIn order to run the documentation, from the root of the repository, run:\n\n.. code-block:: bash\n\n    $ cd docs\n    $ sphinx-build . build -b html -c .\n\n\nThe documentation is now in the `build` subfolder, where you can open \nthe `index.html` in your browser.\n',
    'author': 'Maarten Pronk',
    'author_email': 'maarten.pronk@deltares.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://deltares.github.io/geolib/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
