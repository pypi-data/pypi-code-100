# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webots_web_log_interface']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.3,<4.0.0', 'numpy>=1.21.3,<2.0.0']

setup_kwargs = {
    'name': 'webots-web-log-interface',
    'version': '0.2.0',
    'description': 'A python library used to interact with webots robocup game web logs',
    'long_description': '# Webots Web Log Interface\nA python library used to interact with webots robocup game web logs\n\n## Installation\n\n```bash\npip3 install webots-web-log-interface\n```\n\n## Documentation\n\nYou can find the interface documentation [here](https://bit-bots.github.io/webots-web-log-interface/html/webots_web_log_interface/interface.html).\n\n## Examples\n\nDownload example data\n\n```bash\nmkdir data\ncd data\nwget https://games.bit-bots.de/k-ko-sf2/K-KO-SF2.json\nwget https://games.bit-bots.de/k-ko-sf2/K-KO-SF2.x3d\ncd ..\n```\n\nNow you are able to use the interface\n\n```python\nfrom webots_web_log_interface.interface import WebotsGameLogParser\n\ngp = WebotsGameLogParser(log_folder="data")\n\n# Now some examples\n# Get ball\nball = gp.x3d.get_ball_id()\n# Get velocities for ball\nprint(gp.game_data.get_velocity_vectors_for_id(ball))\n# Get player names\nprint(gp.x3d.get_player_names())\n# Plot player paths\ngp.plot_player_paths()\n```\n\n## Build it yourself\n\n```bash\ngit clone https://github.com/bit-bots/webots-web-log-interface.git\ncd webots-web-log-interface\n\npoetry install\npoetry shell\n```\n',
    'author': 'Florian Vahl',
    'author_email': 'florian@flova.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://bit-bots.github.io/webots-web-log-interface',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
