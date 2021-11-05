# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gym_saturation',
 'gym_saturation.envs',
 'gym_saturation.logic_ops',
 'gym_saturation.parsing']

package_data = \
{'': ['*'],
 'gym_saturation': ['resources/*',
                    'resources/TPTP-mock/Axioms/*',
                    'resources/TPTP-mock/Problems/SET/*',
                    'resources/TPTP-mock/Problems/TST/*']}

install_requires = \
['gym', 'lark-parser']

extras_require = \
{':python_version < "3.7"': ['dataclasses'],
 ':python_version < "3.9" and python_version >= "3.7"': ['importlib_resources']}

setup_kwargs = {
    'name': 'gym-saturation',
    'version': '0.1.3',
    'description': 'An OpenAI Gym environment for saturation provers',
    'long_description': "[![PyPI version](https://badge.fury.io/py/gym-saturation.svg)](https://badge.fury.io/py/gym-saturation) [![CircleCI](https://circleci.com/gh/inpefess/gym-saturation.svg?style=svg)](https://circleci.com/gh/inpefess/gym-saturation) [![Documentation Status](https://readthedocs.org/projects/gym-saturation/badge/?version=latest)](https://gym-saturation.readthedocs.io/en/latest/?badge=latest) [![codecov](https://codecov.io/gh/inpefess/gym-saturation/branch/master/graph/badge.svg)](https://codecov.io/gh/inpefess/gym-saturation)\n[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/inpefess/gym-saturation/HEAD?labpath=examples%2Fexample.ipynb)\n\n# gym-saturation\n\n`gym-saturation` is an [OpenAI Gym](https://gym.openai.com/) environment for reinforcement learning (RL) agents capable of proving theorems. Currently, only theorems in CNF sublanguage of [TPTP](http://tptp.org) are supported. `gym-saturation` implements the 'given clause' algorithm (similar to one used in [Vampire](https://github.com/vprover/vampire) and [E Prover](https://github.com/eprover/eprover)). Although, being written in Python, `gym-saturation` is closer to [PyRes](https://github.com/eprover/PyRes). In contrast to monolithic architecture of a typical ATP, `gym-saturation` gives different agents opportunities to select clauses themselves and train from their experience. Combined with a particular agent, `gym-saturation` can work as an Automated Theorem Prover (ATP).\n\n`gym-saturation` can be interesting for RL practitioners willing to apply their experience to theorem proving without coding all the logic-related stuff themselves. It also can be useful for automated deduction researchers who want to create an RL-empowered ATP.\n\n# How to Install\n\nThe best way to install this package is to use `pip`:\n\n```sh\npip install gym-saturation\n```\n\nOne also can run it in a Docker container:\n\n```sh\ndocker build -t gym-saturation https://github.com/inpefess/gym-saturation.git\ndocker run -it --rm -p 8888:8888 gym-saturation jupyter-lab --ip=0.0.0.0 --port=8888 --no-browser\n```\n\n# How to use\n\nSee [the notebook](https://github.com/inpefess/gym-saturation/blob/master/examples/example.ipynb) or run it in [Binder](https://mybinder.org/v2/gh/inpefess/gym-saturation/HEAD?labpath=examples%2Fexample.ipynb) for more information.\n\n# How to Contribute\n\n[Pull requests](https://github.com/inpefess/gym-saturation/pulls) are welcome. To start:\n\n```sh\ngit clone https://github.com/inpefess/gym-saturation\ncd gym-saturation\n# activate python virtual environment with Python 3.6+\npip install -U pip\npip install -U setuptools wheel poetry\npoetry install\n# recommended but not necessary\npre-commit install\n```\n\nTo check the code quality before creating a pull request, one might run the script `show_report.sh`. It locally does nearly the same as the CI pipeline after the PR is created.\n\n\n# Reporting issues or problems with the software\n\nQuestions and bug reports are welcome on [the tracker](https://github.com/inpefess/gym-saturation/issues). \n\n# More documentation\n\nMore documentation can be found [here](https://gym-saturation.readthedocs.io/en/latest).\n",
    'author': 'Boris Shminke',
    'author_email': 'boris@shminke.ml',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/inpefess/gym-saturation',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<3.10',
}


setup(**setup_kwargs)
