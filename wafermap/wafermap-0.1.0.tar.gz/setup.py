# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests', 'wafermap']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.4.0,<9.0.0',
 'branca>=0.4.2,<0.5.0',
 'folium>=0.12.1,<0.13.0',
 'numpy>=1.21.3,<2.0.0']

extras_require = \
{'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0'],
 'test': ['selenium==4.0.0',
          'black>=20.8b1,<21.0',
          'isort>=5.6.4,<6.0.0',
          'flake8>=3.8.4,<4.0.0',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'pytest>=6.1.2,<7.0.0',
          'pytest-cov>=2.10.1,<3.0.0'],
 'with_png': ['selenium==4.0.0']}

setup_kwargs = {
    'name': 'wafermap',
    'version': '0.1.0',
    'description': 'A python package to plot maps of semiconductor wafers..',
    'long_description': '# Wafermap\n\n\n<p align="center">\n<a href="https://pypi.python.org/pypi/wafermap">\n    <img src="https://img.shields.io/pypi/v/wafermap.svg"\n        alt = "Release Status">\n</a>\n\n<a href="https://github.com/cap1tan/wafermap/actions">\n    <img src="https://github.com/cap1tan/wafermap/actions/workflows/release.yml/badge.svg?branch=release" alt="CI Status">\n</a>\n\n<!-- <a href="https://wafermap.readthedocs.io/en/latest/?badge=latest">\n    <img src="https://readthedocs.org/projects/wafermap/badge/?version=latest" alt="Documentation Status">\n</a> -->\n\n</p>\n\n\nA python package to plot maps of semiconductor wafers.\n\n\n* Free software: MIT\n\n\n## Features\n\n* Circular wafers with arbitrary notch orientations.\n* Edge-exclusion and grids with optional margin.\n* Hover-able points, vectors and images.\n* Tooltips with embeddable images.\n* Export zoom-able maps to HTML.\n* Toggle layers on/off individually.\n* Export to png with selenium, geckodriver and Mozilla\n\n\n## Examples\n\nSave the [demo html](examples/test_wafermap_example.html) file and open in a browser for the scrollable/zoomable version.\n\nStatic png image:\n\n![Example_wafermap](examples/test_wafermap_example.png)\n\n\n## Installation\n\nTo install Wafermap, run this command in your\nterminal:\n\n``` console\n$ pip install wafermap\n```\n\nThis is the preferred method to install Wafermap, as it will always install the most recent stable release.\n\nIf you don\'t have [pip][] installed, this [Python installation guide][]\ncan guide you through the process.\n\n### From source\n\nThe source for Wafermap can be downloaded from\nthe [Github repo][].\n\nYou can clone the public repository:\n\n``` console\n$ git clone git://github.com/cap1tan/wafermap\n```\n\n\n  [pip]: https://pip.pypa.io\n  [Python installation guide]: http://docs.python-guide.org/en/latest/starting/installation/\n  [Github repo]: https://github.com/%7B%7B%20cookiecutter.github_username%20%7D%7D/%7B%7B%20cookiecutter.project_slug%20%7D%7D\n\n\n## Usage\n\nTo use Wafermap in a project\n\n```python\n    import wafermap\n```\n\nFirst let\'s define a Wafermap:\n```python\nwm = wafermap.WaferMap(wafer_radius=100e-3,             # all length dimensions in meters\n                       cell_size=(10e-3, 20e-3),        # (sizeX, sizeY)\n                       cell_margin=(8e-3, 15e-3),       # distance between cell borders (x, y)\n                       grid_offset=(-2.05e-3, -4.1e-3), # grid offset in (x, y)\n                       edge_exclusion=2.2e-3,           # margin from the wafer edge where a red edge exclusion ring is drawn\n                       coverage=\'full\',                 # \'full\': will cover wafer with cells, partial cells allowed\n                                                        # \'inner\': only full cells allowed\n                       notch_orientation=270)           # angle of notch in degrees. 270 corresponds to a notch at the bottom\n```\n\nTo add an image at a specific cell/relative cell coordinates simply:\n```python\nwm.add_image(image_source_file="inspection1.jpg",\n             cell=(1, 0),                               # (cell_index_x, cell_index_y)\n             offset=(2.0e-3, 2.0e-3))                   # relative coordinate of the image within the cell\n```\n\nAdding vectors is just as easy. Just define cell and \\[(start_rel_coordinates), (end_rel_coordinates)\\]:\n```python\nvectors = [\n            ((3, 0), [(0, 0), (1e-3, 1e-3)]),\n            ((3, 0), [(1e-3, 0), (-5e-3, 5e-3)]),\n            ((3, 0), [(0, 1e-3), (10e-3, -10e-3)]),\n            ((3, 0), [(1e-3, 1e-3), (-20e-3, -20e-3)]),\n            ]\ncolors = [\'green\', \'red\', \'blue\', \'black\']\nfor color, (cell, vector) in zip(colors, vectors):\n    wm.add_vector(vector_points=vector, cell=cell, vector_style={\'color\': color}, root_style={\'radius\': 1, \'color\': color})\n```\n\nLet\'s throw in some points in a normal distribution for good measure too:\n```python\n# add 50 points per cell, in a random distribution\nimport random as rnd\ncell_size = (10e-3, 20e-3)\ncell_points = [(cell, [(rnd.gauss(cell_size[1]/2, cell_size[1]/6), rnd.gauss(cell_size[0]/2, cell_size[0]/6)) for _ in range(50)]) for cell in wm.cell_map.keys()]\nfor cell, cell_points_ in cell_points:\n    for cell_point in cell_points_:\n        wm.add_point(cell=cell, offset=cell_point)\n```\n\nFinally, nothing would matter if we couldn\'t see the result:\n```python\n# save to html\nwm.save_html(f"wafermap.html")\n\n# save to png (Mozilla must be installed)\nwm.save_png(f"wafermap.png")\n```\n\n\n## Dependencies\n\n- Folium\n- branca\n- Pillow\n- Optional for exporting to .png images: selenium, geckodriver and Mozilla browser installed.\n\n\n## Contributing\n\nContributions are welcome, and they are greatly appreciated! Every little bit\nhelps, and credit will always be given.\n\nYou can contribute in many ways:\n\n### Types of Contributions\n\n#### Report Bugs\n\nReport bugs at https://github.com/cap1tan/wafermap/issues.\n\nIf you are reporting a bug, please include:\n\n* Your operating system name and version.\n* Any details about your local setup that might be helpful in troubleshooting.\n* Detailed steps to reproduce the bug.\n\n#### Fix Bugs\n\nLook through the GitHub issues for bugs. Anything tagged with "bug" and "help\nwanted" is open to whoever wants to implement it.\n\n#### Implement Features\n\nLook through the GitHub issues for features. Anything tagged with "enhancement"\nand "help wanted" is open to whoever wants to implement it.\n\n#### Write Documentation\n\nWafermap could always use more documentation, whether as part of the\nofficial Wafermap docs, in docstrings, or even on the web in blog posts,\narticles, and such.\n\n#### Submit Feedback\n\nThe best way to send feedback is to file an issue at https://github.com/cap1tan/wafermap/issues.\n\nIf you are proposing a feature:\n\n* Explain in detail how it would work.\n* Keep the scope as narrow as possible, to make it easier to implement.\n* Remember that this is a volunteer-driven project, and that contributions\n  are welcome :)\n\n### Get Started!\n\nReady to contribute? Here\'s how to set up `wafermap` for local development.\n\n1. Fork the `wafermap` repo on GitHub.\n2. Clone your fork locally\n\n```\n    $ git clone git@github.com:your_name_here/wafermap.git\n```\n\n3. Ensure [poetry](https://python-poetry.org/docs/) is installed.\n4. Install dependencies and start your virtualenv:\n\n```\n    $ poetry install -E test -E doc -E dev\n```\n\n5. Create a branch for local development:\n\n```\n    $ git checkout -b name-of-your-bugfix-or-feature\n```\n\n   Now you can make your changes locally.\n\n6. When you\'re done making changes, check that your changes pass the\n   tests, including testing other Python versions, with tox:\n\n```\n    $ tox\n```\n\n7. Commit your changes and push your branch to GitHub:\n\n```\n    $ git add .\n    $ git commit -m "Your detailed description of your changes."\n    $ git push origin name-of-your-bugfix-or-feature\n```\n\n8. Submit a pull request through the GitHub website.\n\n### Pull Request Guidelines\n\nBefore you submit a pull request, check that it meets these guidelines:\n\n1. The pull request should include tests.\n2. If the pull request adds functionality, the docs should be updated. Put\n   your new functionality into a function with a docstring, and add the\n   feature to the list in README.md.\n3. The pull request should work for Python 3.6, 3.7, 3.8, 3.9 and for PyPy. Check\n   https://github.com/cap1tan/wafermap/actions\n   and make sure that the tests pass for all supported Python versions.\n\n### Tips\n```\n    $ python -m unittest tests.test_wafermap\n```\nTo run a subset of tests.\n\n\n### Deploying\n\nA reminder for the maintainers on how to deploy.\nMake sure all your changes are committed (including an entry in HISTORY.md).\nThen run:\n\n```\n$ poetry patch # possible: major / minor / patch\n$ git push\n$ git push --tags\n```\n\nGithub Actions will then deploy to PyPI if tests pass.\n',
    'author': 'Sotiris Thomas',
    'author_email': 'sothomas88@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cap1tan/wafermap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
