# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['david_home_automation']

package_data = \
{'': ['*'], 'david_home_automation': ['static/*']}

install_requires = \
['Flask>=2.0.2,<3.0.0',
 'click>=8.0.0,<9.0.0',
 'pyyaml>=5.0,<6.0',
 'wakeonlan>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'david-home-automation',
    'version': '0.1.29',
    'description': '',
    'long_description': '# Home automation\n\n## Installation\n```shell\npip3 install david-home-automation==0.1.29\n(sudo apt install --yes expect && cd $(mktemp -d) && git clone https://github.com/Heckie75/eQ-3-radiator-thermostat.git x && cd x && cp eq3.exp $HOME/.local/bin)\n\n# (Optional) find your thermostat MACs via\nbluetoothctl devices\n\n# Create your config once \ncat > ~/.config/david-home-automation.yaml <<EOF\nthermostats:\n  - mac_address: XX:XX:XX:XX:XX:XX\n    name: Arbeitszimmer\nhosts:\n  - broadcast_ip: 192.168.178.1\n    mac_address: XX:XX:XX:XX:XX:XX\n    name: Desktop\nEOF\n\n# You can also pass your config file path via an env variable\nexport HOME_AUTOMATION_CONFIG=your/path\n\npython3 -m david_home_automation.server --server-host=0.0.0.0 --server-port 5000\n```\n\n## Development\n\n- [Install poetry](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions)\n\n```\nFLASK_ENV=development FLASK_APP=david_home_automation/main poetry run flask run --host=0.0.0.0 --port 5050\n```\n\n## As a service\n\n```shell\n./install.sh\n```',
    'author': 'David Gengenbach',
    'author_email': 'info@davidgengenbach.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
