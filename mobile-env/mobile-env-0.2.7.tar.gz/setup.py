# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mobile_env',
 'mobile_env.baselines',
 'mobile_env.core',
 'mobile_env.handlers',
 'mobile_env.scenarios',
 'mobile_env.wrappers']

package_data = \
{'': ['*']}

install_requires = \
['Shapely>=1.7.0,<2.0.0',
 'gym>=0.17.1,<0.18.0',
 'matplotlib>=3.4,<4.0',
 'numpy>=1.2.0,<2.0.0',
 'pygame>=2.0,<3.0',
 'svgpath2mpl>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'mobile-env',
    'version': '0.2.7',
    'description': 'mobile-env: A minimalist environment for decision making in wireless mobile networks.',
    'long_description': '[![Python package](https://github.com/stefanbschneider/mobile-env/actions/workflows/python-package.yml/badge.svg)](https://github.com/stefanbschneider/mobile-env/actions/workflows/python-package.yml)\n[![Documentation Status](https://readthedocs.org/projects/mobile-env/badge/?version=latest)](https://mobile-env.readthedocs.io/en/latest/?badge=latest)\n[![Publish](https://github.com/stefanbschneider/mobile-env/actions/workflows/python-publish.yml/badge.svg)](https://github.com/stefanbschneider/mobile-env/actions/workflows/python-publish.yml)\n#  [Try Mobile-Env on Google Colab!   ![Open in colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/stefanbschneider/mobile-env/blob/master/examples/tutorial.ipynb)\nMobile-Env is a minimalist OpenAI-Gym environment for training and evaluating intelligent coordination algorithms in wireless mobile networks. At each time step, it must be decided what connections should be established among user equipments (UEs) and basestations (BSs) in order to maximize Quality of Experience (QoE) globally. To maximize the QoE of single UEs, the UE intends to connect to as many BSs as possible, which yields higher (macro) data rates. However, BSs multiplex resources among connected UEs (e.g. schedule physical resource blocks) and, therefore, UEs compete for limited resources (conflicting goals). To maximize QoE globally, the policy must recognize that (1) the data rate of any connection is governed by the channel (e.g. SNR) between UE and BS and (2) QoE of single UEs not necessarily grows linearly with increasing data rate.\n\nMobile-Env supports multi-agent and centralized reinforcement learning policies. It provides various choices for rewards and observations. Mobile-Env is also easily extendable, so that anyone may add another channel models (e.g. path loss), movement patterns, utility functions, etc.\n\n<p align="center">\n    <img src="https://user-images.githubusercontent.com/36734964/139288123-7732eff2-24d4-4c25-87fd-ac906f261c93.gif" width="65%"/>\n</p>\n\n\n## Installation\n```bash\npip install mobile-env\n```\n\n## Example Usage\n\n```python\nimport gym\nimport mobile_env\n\nenv = gym.make("mobile-medium-central-v0")\nobs = env.reset()\ndone = False\n\nwhile not done:\n    action = ... # Your agent code here\n    obs, reward, done, info = env.step(action)\n    env.render()\n```\n\n## Customizability\nMobile-Env supports custom channel models, movement patterns, arrival & departure models, resource multiplexing schemes and utility functions. For example, replacing the default [Okumura–Hata](https://en.wikipedia.org/wiki/Hata_model) channel model by a (simplified) path loss model can be as easy as this:\n```python\nimport numpy as np\nfrom mobile_env.core.base import MComCore\nfrom mobile_env.core.channel import Channel\n\n\nclass PathLoss(Channel):\n    def __init__(self, gamma, **kwargs):\n        super().__init__(**kwargs)\n        # path loss exponent\n        self.gamma = gamma\n\n    def power_loss(self, bs, ue):\n        """Computes power loss between BS and UE."""\n        dist = bs.point.distance(ue.point)\n        loss = 10 * self.gamma * np.log10(4 * np.pi * dist * bs.frequency)\n        return loss\n\n\n# replace default channel model in configuration \nconfig = MComCore.default_config()\nconfig[\'channel\'] = PathLoss\n\n# pass init parameters to custom channel class!\nconfig[\'channel_params\'].update({\'gamma\': 2.0})\n\n# create environment with custom channel model\nenv = gym.make(\'mobile-small-central-v0\', config=config)\n...\n```\n\n## Documentation\nRead the [documentation online](https://mobile-env.readthedocs.io/en/latest/index.html).\n\n\n## DeepCoMP\nMobile-Env builds on [DeepCoMP](https://github.com/CN-UPB/DeepCoMP) and makes its simulation accessible via an OpenAI Gym interface that is independent of any specific reinforcement learning framework.\n',
    'author': 'Stefan Schneider',
    'author_email': 'stefan.schneider@upb.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stefanbschneider/mobile-env',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
