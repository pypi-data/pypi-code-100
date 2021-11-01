# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csvio', 'csvio.processors', 'csvio.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'csvio',
    'version': '0.3.0',
    'description': 'CSV Wrapper for conveniently processing csv files',
    'long_description': '.. image:: https://github.com/s-raza/csvio/blob/master/docs/source/_static/csvio_logo_240x160px.png?raw=True\n   :align: center\n   :target: https://github.com/s-raza/csvio\n   :alt: csvio Logo\n\ncsvio: Python Library for processing CSV files\n==============================================\n\n.. image:: https://img.shields.io/github/license/s-raza/csvio?color=bright\n    :alt: GitHub License\n    :target: https://github.com/s-raza/csvio/blob/master/LICENSE\n\n.. image:: https://img.shields.io/badge/python-3.8%2B-bright\n    :alt: Python Versions\n\n.. image:: https://img.shields.io/readthedocs/csvio/latest\n    :alt: Readthedocs\n    :target: https://csvio.readthedocs.io/en/latest\n\ncsvio is a Python library that provides a wrapper around Python\'s built in\n``csv.DictReader`` and ``csv.DictWriter``, for ease of reading and\nwriting CSV files.\n\nRows in a CSV are represented and processed as a list of dictionaries. Each\nitem in this list is a dictionary that represents a row. The key, value pairs\nin each dictionary is a mapping between the column and its associated row value\nfrom the CSV.\n\nInstallation\n------------\n\n.. code-block:: bash\n\n   pip install csvio\n\nDocumentation\n-------------\n\n`Readthedocs <https://csvio.readthedocs.io>`_\n\nReading CSVs\n------------\n\n.. code-block:: python\n\n   >>> from csvio import CSVReader\n   >>> reader = CSVReader("fruit_stock.csv")\n   >>> reader.fieldnames\n   [\'Supplier\', \'Fruit\', \'Quantity\']\n   >>> len(reader.rows)\n   4\n\n   >>> import json\n   >>> print(json.dumps(reader.rows, indent=4))\n   [\n      {\n            "Supplier": "Big Apple",\n            "Fruit": "Apple",\n            "Quantity": "1"\n      },\n      {\n            "Supplier": "Big Melons",\n            "Fruit": "Melons",\n            "Quantity": "2"\n      },\n      {\n            "Supplier": "Long Mangoes",\n            "Fruit": "Mango",\n            "Quantity": "3"\n      },\n      {\n            "Supplier": "Small Strawberries",\n            "Fruit": "Strawberry",\n            "Quantity": "4"\n      }\n   ]\n\n*CSV file contents:*\n\n.. code-block:: bash\n\n   Supplier,Fruit,Quantity\n   Big Apple,Apple,1\n   Big Melons,Melons,2\n   Long Mangoes,Mango,3\n   Small Strawberries,Strawberry,4\n\nWriting CSVs\n------------\n\n.. code-block:: python\n\n   >>> from csvio import CSVWriter\n   >>> writer = CSVWriter("fruit_stock.csv", fieldnames=["Supplier", "Fruit", "Quantity"])\n   >>> row1 = {"Supplier": "Big Apple", "Fruit": "Apple", "Quantity": 1}\n   >>> writer.add_rows(row1)\n   >>> rows2_3_4 = [\n   ...     {"Supplier": "Big Melons", "Fruit": "Melons", "Quantity": 2},\n   ...     {"Supplier": "Long Mangoes", "Fruit": "Mango", "Quantity": 3},\n   ...     {"Supplier": "Small Strawberries", "Fruit": "Strawberry", "Quantity": 4}\n   ... ]\n   >>> writer.add_rows(rows2_3_4)\n   >>> len(writer.pending_rows)\n   4\n\n   >>> len(writer.rows)\n   0\n\n   >>> writer.flush()\n   >>> len(writer.pending_rows)\n   0\n\n   >>> len(writer.rows)\n   4\n\nOnce flush is called a CSV file with the name *fruit_stock.csv* will be\nwritten with the following contents.\n\n.. code-block:: bash\n\n      Supplier,Fruit,Quantity\n      Big Apple,Apple,1\n      Big Melons,Melons,2\n      Long Mangoes,Mango,3\n      Small Strawberries,Strawberry,4\n\n.. ignore-below-marker\n\n`Readthedocs for more example code <https://csvio.readthedocs.io>`_\n',
    'author': 'Salman Raza',
    'author_email': 'raza.salman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://csvio.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
