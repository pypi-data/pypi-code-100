# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geojson_length']

package_data = \
{'': ['*']}

install_requires = \
['geopy==2.0.0']

setup_kwargs = {
    'name': 'geojson-length',
    'version': '0.3.0',
    'description': 'Calculate the length of a GeoJSON LineString or MultiLineString',
    'long_description': '# geojson-length\n\n[![Build](https://github.com/zaitra/geojson-length/actions/workflows/release.yml/badge.svg)](https://github.com/zaitra/geojson-length/actions/workflows/release.yml) [![Pypi](https://img.shields.io/pypi/v/geojson-length.svg)](https://pypi.python.org/pypi/geojson-length)\n\n\nCalculate the length of a GeoJSON LineString or MultiLineString\n\n\n## Installation\n------------\n\n```\n$ pip3 install geojson-length\n```\n\n## Usage\n------------\n\n```python\n  >>> from geojson_length import calculate_distance, Unit\n  >>> from geojson import Feature, LineString\n\n  >>> line = Feature(geometry=LineString([[19.6929931640625,48.953170117120976],[19.5556640625,48.99283383694351]]))\n  >>> calculate_distance(line, Unit.meters)\n  10979.098283583924\n```\n\n> Note: You need to install [python-geojson](https://github.com/jazzband/geojson) first or you can define GeoJSON as python dict:\n\n```python\n    line = {\n      "type": "Feature",\n      "properties": {},\n      "geometry": {\n        "type": "LineString",\n        "coordinates": [\n          [\n            19.6929931640625,\n            48.953170117120976\n          ],\n          [\n            19.5556640625,\n            48.99283383694351\n          ]\n        ]\n      }\n    }\n```\n\n## Run test suite\n\n1. `$ pip install pytest`\n2. `$ poetry run pytest --color=yes --verbose --showlocals tests`\n\n\n> You may need to run `poetry install` first.\n\n\n## Credits\n-------\n\nThis package was created with Cookiecutter_ and the [audreyr/cookiecutter-pypackage`](https://github.com/audreyr/cookiecutter-pypackage) project template.\n\nThe idea was inspired by [geojson-length](https://github.com/tyrasd/geojson-length) package written in JS.\n\n## License\n\nFree software: MIT license\n',
    'author': 'Zaitra',
    'author_email': 'info@zaitra.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
