# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pollencli', 'pollencli.pyline_removal']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['rm-pyline = pollencli.pyline_removal.cli:main']}

setup_kwargs = {
    'name': 'pollencli-pyline-removal',
    'version': '0.0.5a0',
    'description': 'Remove lines from python file',
    'long_description': '# pollencli-pyline-removal\n\n<p align="center">\n  <a href="https://github.com/psf/black">\n    <img\n      alt="Issues"\n      src="https://img.shields.io/badge/code%20style-black-000000.svg"\n    />\n</p>\n\n## How to use\n\n`rm-pyline <name_id> <src_filepath>` command\n\n```bash\nrm-pyline\n```\n\n### example\n\ninput python file : `input.py`\n\n```py\ndef main():\n    x: int = 1\n    print(f"Hello, World! : {x}")\n\n\nif __name__ == "__main__":\n    main()\n\n```\n\n```sh\nrm-pyline print ./input.py > output.py\n```\n\n`output.py`\n\n- not formatted file\n- There is no guarantee that the output is valid python code even if the input is.\n\n```py\ndef main():\n    x: int = 1\nif __name__ == \'__main__\':\n    main()\n```\n',
    'author': 'pollenjp',
    'author_email': 'polleninjp@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pollenjp/pollencli-pyline-removal',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
