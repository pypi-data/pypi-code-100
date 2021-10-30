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
    'version': '0.2.0',
    'description': 'Reserve and execute commands on EC2 Spot instance with ease',
    'long_description': '==============\ngeojson-length\n==============\n\n\n.. image:: https://img.shields.io/pypi/v/geojson-length.svg\n        :target: https://pypi.python.org/pypi/geojson-length\n\n.. image:: https://img.shields.io/travis/zaitra/geojson-length.svg\n        :target: https://travis-ci.org/zaitra/geojson-length\n\n\nCalculate the length of a GeoJSON LineString or MultiLineString\n\n\n* Free software: MIT license\n\n\nInstallation\n------------\n\n.. code::\n\n  $ pip3 install geojson-length\n\n\nUsage\n------------\n\n.. code:: python\n\n  >>> from geojson_length import calculate_distance, Unit\n  >>> from geojson import Feature, LineString\n\n  >>> line = Feature(geometry=LineString([[19.6929931640625,48.953170117120976],[19.5556640625,48.99283383694351]]))\n  >>> calculate_distance(line, Unit.meters)\n  10979.098283583924\n\nNote: You need to install python-geojson_ first or you can define GeoJSON as python dict:\n\n.. _python-geojson: https://github.com/jazzband/geojson\n\n.. code:: python\n\n    line = {\n      "type": "Feature",\n      "properties": {},\n      "geometry": {\n        "type": "LineString",\n        "coordinates": [\n          [\n            19.6929931640625,\n            48.953170117120976\n          ],\n          [\n            19.5556640625,\n            48.99283383694351\n          ]\n        ]\n      }\n    }\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.\n\nThe idea was inspired by geojson-length_ package written in JS.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage\n.. _`geojson-length`: https://github.com/tyrasd/geojson-length\n',
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
