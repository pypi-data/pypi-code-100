# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['xleapp',
 'xleapp.artifacts',
 'xleapp.gui',
 'xleapp.helpers',
 'xleapp.log',
 'xleapp.report',
 'xleapp.templating',
 'xleapp.templating._partials']

package_data = \
{'': ['*'],
 'xleapp.report': ['_static/*',
                   '_static/MDB-Free_4.13.0/css/*',
                   '_static/MDB-Free_4.13.0/css/addons/*',
                   '_static/MDB-Free_4.13.0/img/overlays/*',
                   '_static/MDB-Free_4.13.0/img/svg/*',
                   '_static/MDB-Free_4.13.0/js/*',
                   '_static/MDB-Free_4.13.0/js/addons/*',
                   '_static/MDB-Free_4.13.0/js/modules/*'],
 'xleapp.templating': ['templates/*']}

install_requires = \
['Jinja2>=3.0.2,<4.0.0',
 'PySimpleGUI>=4.53.0,<5.0.0',
 'PyYAML>=6.0,<7.0',
 'prettytable>=2.2.1,<3.0.0',
 'python-magic-bin>=0.4.14,<0.5.0',
 'simplekml>=1.3.6,<2.0.0',
 'wrapt>=1.13.2,<2.0.0']

entry_points = \
{'console_scripts': ['xleapp = xleapp.__main__:cli']}

setup_kwargs = {
    'name': 'xleapp',
    'version': '0.1.1a0',
    'description': 'Multiplaform Logs, Events, And Plists Parser',
    'long_description': '# xLEAPP\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n**Development build. Please be cauious using on real cases.**\n\nFramework for Logs, Events, And Plists Parser (LEAPP)\n\nThis framework is a complete rewrite of the excellent tool iLEAPP.Details of iLEAPP can be found in this [blog post](https://abrignoni.blogspot.com/2019/12/xleapp-ios-logs-events-and-properties.html)\n\nxLEAPP is the framework created to merge several tools together. More information about the rewrite is given in by talk ([YouTube](https://www.youtube.com/watch?v=seTpCmSF0Gc)) at Black Hills Info Security&#39;s Wild West Hackin&#39; Fest (WWHF): Deadwood in 2021.\n\n<img src="https://user-images.githubusercontent.com/1879197/139466769-3155b3d9-75c6-4ef0-bbb0-73b77fdc349f.gif" width=700>\n\n## Features\n\n* Provides a centralized and modular framework\n* Provides a simplified way to write plugins (artifacts) for each different supported platform.\n* Parses iOS, macOS, Android, Chromebook, warranty returns, and Windows artifacts depending on the plugins installed.\n\n## Other Documentation\n\n* [Artifact Creation](docs/current/artifact-creation.md)\n\n## Pre-requisites\n\nThis project requires you to have Python >= 3.9\n\n## Plugins\n\nHere is a list of plugins that need to be completed. Plugin package suffixed with "non-free" use licenses that may not conform with MIT licenses and are seperated out.\n\n- [X] xleapp-ios [[Github](https://github.com/flamusdiu/xleapp-ios)] [[PyPI](https://pypi.org/project/xleapp-ios/)]\n- [ ] xleapp-ios-non-free [[Github](https://github.com/flamusdiu/xleapp-ios)]\n- [ ] xleapp-android\n- [ ] xleapp-android-non-free\n- [ ] xleapp-chrome\n- [ ] xleapp-chrome-non-free\n- [ ] xleapp-returns\n- [ ] xleapp-returns-non-free\n- [ ] xleapp-vehicles\n- [ ] xleapp-vehicles-non-free\n- [ ] xleapp-windows\n- [ ] xleapp-windows-non-free \n\n## Installation\n\n### Windows\n\n* Python\n\n  ```powershell\n  PS> py -3 -m pip install xleapp\n  PS> py -3 -m pip install xleapp-<plugin>\n  ```\n\n* PIPX\n\n  ```powershell\n  PS> py -3 -m pip install pipx\n  PS> pipx install xleapp\n  PS> pipx inject xleapp xleapp-<plugin>\n  ```\n\n### Linux\n\n* Python\n\n  ```bash\n  $ python3 -m pip install xleapp\n  $ python3 -m pip install xleapp-<plugin>\n  ```\n\n* PIPX\n\n  ```bash\n  $ python3 -m pip install pipx\n  $ pipx install xleapp\n  $ pipx inject xleapp xleapp-<plugin>\n  ```\n\n## Installation from Github and Development Information\n\n* [Windows](docs/current/windows.md)\n* [Linux](docs/current/linux.md)\n\n## VS Code configuration files\n\nThere are several [configuration files](https://github.com/flamusdiu/xleapp-project) that I have been using for VS Code.\n\n## Compile to executable\n\n**NOTE:** This may not work at this time with this alpha version.\n\nTo compile to an executable so you can run this on a system without python installed.\n\nTo create xleapp.exe, run:\n\n```bash\npyinstaller --onefile xleapp.spec\n```\n\nTo create xleappGUI.exe, run:\n\n```bash\npyinstaller --onefile --noconsole xleappGUI.spec\n```\n\n## Usage\n\n### CLI\n\n```bash\n$ xleapp -h\nusage: xleapp [-h] [-I] [-R] [-A] [-C] [-V] [-o OUTPUT_FOLDER] [-i INPUT_PATH]\n       [--artifacts [ARTIFACTS ...]] [-p] [-l] [--gui] [--version]\n\nxLEAPP: Logs, Events, and Plists Parser.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -I                    parse ios artifacts\n  -R                    parse Warrant Returns / User Generated Archives artifacts\n  -A                    parse android artifacts\n  -C                    parse Chromebook artifacts\n  -V                    parse vehicle artifacts\n  -o OUTPUT_FOLDER, --output_folder OUTPUT_FOLDER\n                        Output folder path\n  -i INPUT_PATH, --input_path INPUT_PATH\n                        Path to input file/folder\n  --artifact [ARTIFACT ...]\n                        Filtered list of artifacts to run. Allowed: core, <check artifact list in\n                        documentation>\n  -p, --artifact_paths  Text file list of artifact paths\n  -l, --artifact_table  Text file with table of artifacts\n  --gui                 Runs xLEAPP into graphical mode\n  --version             show program&#39;s version number and exit\n\n```\n\n### GUI\n\nThis needs work and may not work properly!\n\n```bash\n$ xleapp --gui \n\n```\n\n### Help\n\n```bash\n$ xleapp.py --help\n\n```\n\nThe GUI will open in another window.  \n\n## Acknowledgements\n\nThis tool is the result of a collaborative effort of many people in the DFIR community.\n\nThis product includes software developed by Sarah Edwards (Station X Labs, LLC, @iamevltwin, mac4n6.com) and other contributors as part of APOLLO (Apple Pattern of Life Lazy Output\'er).\n',
    'author': 'Jesse Spangenberger',
    'author_email': 'azuleonyx@digitalforensics.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/flamusdiu/xleapp',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
