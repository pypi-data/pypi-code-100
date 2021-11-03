# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['traffic',
 'traffic.algorithms',
 'traffic.console',
 'traffic.core',
 'traffic.data',
 'traffic.data.adsb',
 'traffic.data.airspaces',
 'traffic.data.basic',
 'traffic.data.datasets',
 'traffic.data.eurocontrol',
 'traffic.data.eurocontrol.b2b',
 'traffic.data.eurocontrol.b2b.xml',
 'traffic.data.eurocontrol.ddr',
 'traffic.data.faa',
 'traffic.data.samples',
 'traffic.data.samples.ambulances',
 'traffic.data.samples.calibration',
 'traffic.data.samples.collections',
 'traffic.data.samples.featured',
 'traffic.data.samples.firefighting',
 'traffic.data.samples.gliders',
 'traffic.data.samples.military',
 'traffic.data.samples.onground',
 'traffic.data.samples.surveillance',
 'traffic.data.samples.surveys',
 'traffic.data.samples.tv_relay',
 'traffic.data.weather',
 'traffic.drawing',
 'traffic.plugins']

package_data = \
{'': ['*'], 'traffic.data.samples': ['airspaces/*']}

install_requires = \
['Cartopy>=0.19.0,<0.20.0',
 'Shapely>=1.7.1,<2.0.0',
 'altair>=4.1.0,<5.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'cartes>=0.5,<1.0',
 'ipyleaflet>=0.14.0,<0.15.0',
 'ipywidgets>=7.6.3,<8.0.0',
 'lxml>=4.6.3,<5.0.0',
 'matplotlib>=3.4.2,<4.0.0',
 'metar>=1.8.0,<2.0.0',
 'numpy>=1.18,<2.0',
 'openap>=1.1,<2.0',
 'pandas>=1.2.4,<2.0.0',
 'paramiko>=2.7.2,<3.0.0',
 'pyModeS>=2.9,<3.0',
 'pyOpenSSL>=20.0,<21.0',
 'pyarrow>=4.0,<5.0',
 'pyproj>=3.1.0,<4.0.0',
 'requests-pkcs12>=1.10,<2.0',
 'requests>=2.25.1,<3.0.0',
 'scipy>=1.7.0,<2.0.0',
 'tqdm>=4.61.1,<5.0.0',
 'typing-extensions>=3.10.0,<4.0.0']

extras_require = \
{'all': ['xarray>=0.18.2,<0.19.0',
         'libarchive>=0.4.7,<0.5.0',
         'scikit-learn>=1.0,<2.0',
         'fastkml>=0.11,<0.12',
         'keplergl>=0.3.2,<0.4.0',
         'pre-commit>=2.13.0,<3.0.0',
         'isort>=5.9.1,<6.0.0',
         'black>=21.6b0,<22.0',
         'flake8>=3.9.2,<4.0.0',
         'mypy>=0.902,<0.903'],
 'dev': ['pre-commit>=2.13.0,<3.0.0',
         'isort>=5.9.1,<6.0.0',
         'black>=21.6b0,<22.0',
         'flake8>=3.9.2,<4.0.0',
         'mypy>=0.902,<0.903']}

entry_points = \
{'console_scripts': ['traffic = traffic.console:main'],
 'traffic.plugins': ['Bluesky = traffic.plugins.bluesky',
                     'CesiumJS = traffic.plugins.cesiumjs',
                     'Kepler = traffic.plugins.kepler',
                     'Leaflet = traffic.plugins.leaflet']}

setup_kwargs = {
    'name': 'traffic',
    'version': '2.6.6',
    'description': 'A toolbox for manipulating and analysing air traffic data',
    'long_description': '# A toolbox for processing and analysing air traffic data\n\n[![Documentation Status](https://github.com/xoolive/traffic/workflows/docs/badge.svg)](https://traffic-viz.github.io/)\n[![tests](https://github.com/xoolive/traffic/actions/workflows/run-tests.yml/badge.svg?branch=master&event=push)](https://github.com/xoolive/traffic/actions/workflows/run-tests.yml)\n[![Code Coverage](https://img.shields.io/codecov/c/github/xoolive/traffic.svg)](https://codecov.io/gh/xoolive/traffic)\n[![Codacy Badge](https://img.shields.io/codacy/grade/eea673ed15304f1b93490726295d6de0)](https://www.codacy.com/manual/xoolive/traffic)\\\n[![Checked with mypy](https://img.shields.io/badge/mypy-checked-blue.svg)](https://mypy.readthedocs.io/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/psf/black)\n![License](https://img.shields.io/pypi/l/traffic.svg)\n[![Join the chat at https://gitter.im/xoolive/traffic](https://badges.gitter.im/xoolive/traffic.svg)](https://gitter.im/xoolive/traffic?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)\\\n[![JOSS paper](http://joss.theoj.org/papers/10.21105/joss.01518/status.svg)](https://doi.org/10.21105/joss.01518)\n![PyPI version](https://img.shields.io/pypi/v/traffic)\n[![PyPI downloads](https://img.shields.io/pypi/dm/traffic)](https://pypi.org/project/traffic)\n![Conda version](https://img.shields.io/conda/vn/conda-forge/traffic)\n[![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/traffic.svg)](https://anaconda.org/conda-forge/traffic)\n[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/traffic-viz/traffic_static/blob/master/notebooks/quickstart.ipynb)\n\nThe traffic library helps working with common sources of air traffic data.\n\nIts main purpose is to offer basic cumbersome data analysis methods commonly\napplied to trajectories and ATC sectors. When a specific function is not\nprovided, the access to the underlying structure is direct, through an attribute\npointing to a pandas dataframe.\n\nThe library also offers facilities to parse and/or access traffic data from open\nsources of ADS-B traffic like the [OpenSky Network](https://opensky-network.org/)\nor Eurocontrol DDR files. It is designed to be easily extendable to other\nsources of data.\n\nStatic visualisation (images) exports are accessible via Matplotlib/Cartopy.\nMore dynamic visualisation frameworks are easily accessible in Jupyter\nenvironments with [ipyleaflet](http://ipyleaflet.readthedocs.io/) and\n[altair](http://altair-viz.github.io/); or through exports to other formats,\nincluding CesiumJS or Google Earth.\n\n## Installation\n\n### Latest release\n\nYou may install `traffic` in a fresh conda environment:\n\n```sh\n# Recommended options if not set up yet\nconda config --set channel_priority strict\nconda config --add channels conda-forge\n\n# Installation\nconda create -n traffic -c conda-forge python=3.9 traffic\n```\n\nAdjust the Python version (>=3.7) and append packages you may need for future works (e.g. `bpython`, `jupyterlab`, etc.)\n\nThen activate the environment each time you need to use the `traffic` library:\n\n```sh\nconda activate traffic\n```\n\n**Warning:**\n\nPlease only report installation issues in fresh conda environments.\n\n### Updating traffic\n\n```sh\n# -n option is followed by the name of the environment\nconda update -n traffic -c conda-forge traffic\n```\n\n\n### Development version\n\nYou may also install or update `traffic` in an existing environment with pip:\n\n```sh\npip install --upgrade traffic\n```\n\nFor the most recent development version, clone the Github repository:\n\n```sh\ngit clone https://github.com/xoolive/traffic\ncd traffic\npip install .[dev]\n```\n\nIf you intend to file a pull request, please activate `pre-commit` hooks:\n\n```sh\npre-commit install\n```\n\n\n\nFor troubleshootings, refer to the appropriate\n[documentation section](https://traffic-viz.github.io/installation.html#troubleshooting).\n\n## Credits\n\n[![JOSS badge](http://joss.theoj.org/papers/10.21105/joss.01518/status.svg)](https://doi.org/10.21105/joss.01518)\n\nIf you find this project useful for your research and use it in an academic\nwork, you may cite it as:\n\n```bibtex\n@article{olive2019traffic,\n    author={Xavier {Olive}},\n    journal={Journal of Open Source Software},\n    title={traffic, a toolbox for processing and analysing air traffic data},\n    year={2019},\n    volume={4},\n    pages={1518},\n    doi={10.21105/joss.01518},\n    issn={2475-9066},\n}\n```\n\nAdditionally, you may consider adding a star to the repository. This token of appreciation is often interpreted as a positive feedback and improves the visibility of the library.\n\n## Documentation\n\n[![Documentation Status](https://github.com/xoolive/traffic/workflows/docs/badge.svg)](https://traffic-viz.github.io/)\n[![Join the chat at https://gitter.im/xoolive/traffic](https://badges.gitter.im/xoolive/traffic.svg)](https://gitter.im/xoolive/traffic?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)\n\nDocumentation available at [https://traffic-viz.github.io/](https://traffic-viz.github.io/)\\\nJoin the Gitter chat: https://gitter.im/xoolive/traffic\n\n## Tests and code quality\n\n[![tests](https://github.com/xoolive/traffic/actions/workflows/run-tests.yml/badge.svg?branch=master&event=push)](https://github.com/xoolive/traffic/actions/workflows/run-tests.yml)\n[![Code Coverage](https://img.shields.io/codecov/c/github/xoolive/traffic.svg)](https://codecov.io/gh/xoolive/traffic)\n[![Codacy Badge](https://img.shields.io/codacy/grade/eea673ed15304f1b93490726295d6de0)](https://www.codacy.com/manual/xoolive/traffic)\n[![Checked with mypy](https://img.shields.io/badge/mypy-checked-blue.svg)](https://mypy.readthedocs.io/)\n\nUnit and non-regression tests are written in the `tests/` directory. You may\nrun `pytest` from the root directory.\n\nTests are checked on [Github Actions](https://github.com/xoolive/traffic/actions/workflows/run-tests.yml)\nplatform upon each commit. Latest status and coverage are displayed with\nstandard badges hereabove.\n\nIn addition, code is checked against static typing with [mypy](https://mypy.readthedocs.io/)\n([pre-commit](https://pre-commit.com/) hooks are available in the repository) and\nextra quality checks performed by [Codacy](https://www.codacy.com/manual/xoolive/traffic).\n\n## Command line tool\n\nThe `traffic` tool scripts around the library for common usecases.\n\nThe most basic use case revolves around exploring the embedded data. You may check\nthe help with `traffic data -h`.\n\n```\ntraffic data -p Tokyo\n     altitude country iata  icao   latitude   longitude                                name\n3820       21   Japan  HND  RJTT  35.552250  139.779602  Tokyo Haneda International Airport\n3821      135   Japan  NRT  RJAA  35.764721  140.386307  Tokyo Narita International Airport\n```\n\nMore details in the [documentation](https://traffic-viz.github.io/).\n\n## Feedback and contribution\n\nAny input, feedback, bug report or contribution is welcome.\n\nShould you encounter any issue, you may want to file it in the [issue](https://github.com/xoolive/traffic/issues/new) section of this repository. Please first activate the `DEBUG` messages recorded using Python logging mechanism with the following snippet:\n\n```python\nimport logging\nlogging.basicConfig(level=logging.DEBUG)\n```\n\nBug fixes and improvements in the library are also helpful.\n\nIf you share a fix together with the issue, I can include it in the code for\nyou. But since you did the job, pull requests (PR) let you keep the authorship\non your additions. For details on creating a PR see GitHub documentation\n[Creating a pull\nrequest](https://help.github.com/en/articles/creating-a-pull-request). You can\nadd more details about your example in the PR such as motivation for the example\nor why you thought it would be a good addition. You will get feedback in the PR\ndiscussion if anything needs to be changed. To make changes continue to push\ncommits made in your local example branch to origin and they will be\nautomatically shown in the PR.\n\nYou may find the process troublesome but please keep in mind it is actually\neasier that way to keep track of corrections and to remember why things are the\nway they are.\n\n## Frequently asked questions\n\n[![Join the chat at https://gitter.im/xoolive/traffic](https://badges.gitter.im/xoolive/traffic.svg)](https://gitter.im/xoolive/traffic?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)\n\n- I want to know more about Eurocontrol NM files\n\nWe download these files from Eurocontrol [Network Manager Demand Data\nRepository (DDR)](https://www.eurocontrol.int/ddr) under Dataset Files >\nAirspace Environment Datasets. [Access\nconditions](https://www.eurocontrol.int/ddr#access-conditions) are managed by\nEUROCONTROL.\n\nShould you have no such access, basic FIRs are provided in `eurofirs` from\n`traffic.data`.\n\n- I want to know more about Eurocontrol AIXM files\n\nWhen you import `aixm_airspaces` from `traffic.data`, you need to set a path\nto a directory containing AIRAC files. These are XML files following the\n[AIXM](http://aixm.aero/) standard and produced by Eurocontrol. We download\nthese files from Eurocontrol [Network Manager B2B web\nservices](https://eurocontrol.int/service/network-manager-business-business-b2b-web-services).\nYou have to own a B2B certificate granted by EUROCONTROL to get access to\nthis data.\n\n- What does AIRAC mean?\n\nAeronautical Information Publications are updated every 28 days according to\nfixed calendar. This cycle is known as AIRAC (Aeronautical Information\nRegulation And Control) cycle.\n',
    'author': 'Xavier Olive',
    'author_email': 'git@xoolive.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xoolive/traffic/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
