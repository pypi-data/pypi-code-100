# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['conesearch_alchemy', 'conesearch_alchemy.tests']

package_data = \
{'': ['*']}

install_requires = \
['sqlalchemy']

setup_kwargs = {
    'name': 'conesearch-alchemy',
    'version': '1.0.0',
    'description': 'SQLAlchemy extension for indexed cone searches in astronomical catalogs',
    'long_description': "# Cone Search Alchemy\n\nThe `conesearch_alchemy` Python package enhances [SQLAlchemy] to provide fast,\nindexed cone searches on astronomical catalogs using a PostgreSQL database. It\ndoes not rely on any database extensions.\n\n## Installation\n\nYou can install `conesearch_alchemy` the Python Package Index:\n\n    $ pip install conesearch-alchemy\n\n## Usage\n\n```python\nfrom conesearch_alchemy.point import Point\nfrom sqlalchemy.ext.declarative import declarative_base\n\nBase = declarative_base()\n\n\n# Create two tables Catalog1 and Catalog2 that both have spherical coordinates.\n\nclass Catalog1(Point, Base):\n    __tablename__ = 'catalog1'\n    id = Column(Integer, primary_key=True)\n\n\nclass Catalog2(Point, Base):\n    __tablename__ = 'catalog2'\n    id = Column(Integer, primary_key=True)\n\n\n...\n\n# Populate Catalog1 and Catalog2 tables with some sample data...\nsession.add(Catalog1(id=0, ra=320.5, dec=-23.5))\n...\nsession.add(Catalog2(id=0, ra=18.1, dec=18.3))\n...\nsession.commit()\n\n\n# Cross-match the two tables.\nseparation = 1  # separation in degrees\nquery = session.query(\n    Catalog1.id, Catalog2.id\n).join(\n    Catalog2,\n    Catalog1.within(point, separation)\n).order_by(\n    Catalog1.id, Catalog2.id\n)\nfor row in query:\n    ...  # do something with the query results\n\n\n# Do a cone search around literal ra, dec values.\nseparation = 1  # separation in degrees\npoint = Point(ra=212.5, dec=-33.2)\nquery = session.query(\n    Catalog1.id\n).filter(\n    Catalog1.within(point, separation)\n).order_by(\n    Catalog1.id\n)\nfor row in query:\n    ...  # do something with the query results\n```\n\n[SQLAlchemy]: https://www.sqlalchemy.org\n",
    'author': 'Leo Singer',
    'author_email': 'leo.singer@ligo.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/skyportal/conesearch-alchemy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
