# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uprate']

package_data = \
{'': ['*']}

extras_require = \
{'docs': ['Sphinx>=4.1.1,<5.0.0',
          'myst-parser>=0.15.1,<0.16.0',
          'furo>=2021.7.5-beta.38,<2022.0.0',
          'sphinx-copybutton>=0.4.0,<0.5.0']}

setup_kwargs = {
    'name': 'uprate',
    'version': '0.2.0',
    'description': 'Ratelimits. Dumbified. A fully typed, simple ratelimit library.',
    'long_description': '<h1 align="center">\n    <img src="https://github.com/WizzyGeek/WizzyGeek/raw/main/assets/uprate/uprate_logo_rev2.png">\n</h1>\n\n<div align="center">\n    A fully typed, simple ratelimit library.\n</div>\n\n<div align="center">\n    <br/>\n    <img src="https://forthebadge.com/images/badges/made-with-python.svg">\n    <img src="https://forthebadge.com/images/badges/built-with-love.svg">\n</div>\n\n<hr/>\n\n# About\n\nUprate is a robust, simple ratelimit library.<br/>\nWhile providing a simple to use api, it is also highly scalable\nand provides absolute control for fine-tuning.<br/> Hence, Uprate\ncan be used in all stages of your app from prototyping to production! 🚀\n<br/>\n[Here](#example) is a simple example.\n\n## Why?\n\nThere are two ways ratelimits are implemented in python for server-side\n - Make everything from scratch\n - Use a framework dependent ratelimit library.\n\nThe problem in the first way is obvious, it\'s harder, consumes more time.<br/>\nUsing a framework dependent ratelimit library is more feasible, but often\nthese libraries don\'t provide features like external stores, multiple ratelimits\nand manual key specification. While there are some awesome ratelimit libraries for\nframwork X, not everyone uses framework X 😕.\n\nRatelimits in client-sided coded also face similar problems. Often APIs enforce multiple\nratelimits. Making a ratelimiter from scratch for your API wrapper\nor a small scale data collector takes up valuable dev time, which is why uprate aims to also\nprovide tools for client-sided code.\n\n## [Documentation](https://uprate.readthedocs.io/en/latest/)\n\nThe documentation can be found at <https://uprate.readthedocs.io/en/latest/> <br/>\n\n# Getting Started\n\n## Installation\n\nYou can install the latest stable version from pypi by\n```\npip install uprate\n```\n*or* you can install the dev version from github\n```\npip install git+https://github.com/WizzyGeek/uprate.git@master#egg=uprate\n```\n## Usage\n\n```\nimport uprate\n```\n\nAnd you are good to go! 🤘\n\n## Example\n\nHere is a simple example that demonstrates Uprate\'s Awesomeness.\n\n```py\nimport uprate\n\n@uprate.ratelimit(1 / (uprate.Seconds(2) + uprate.Minutes(1)))\ndef limited():\n    ...\n\nlimited()\n\ntry:\n    # Within 62 seconds\n    limited()\nexcept uprate.RateLimitError:\n    print("called function too fast")\n```\n\nAnd **so much more**!\n\n<div align="center">\n    <h1></h1>\n    <h6>Thanks to <a href="https://github.com/someonetookmycode">@someonetookmycode</a> for the graphical assets</h6>\n    <h6>© WizzyGeek 2021</h6>\n</div>\n',
    'author': 'WizzyGeek',
    'author_email': 'ojasscoding@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/WizzyGeek/uprate#readme',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
