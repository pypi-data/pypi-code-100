# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['file_converter']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['file_converter = '
                     'file_converter.file_converter:file_converter']}

setup_kwargs = {
    'name': 'file-converter-fgsm',
    'version': '0.1.1',
    'description': 'Class project to convert files from CSV to JSON and vice-versa',
    'long_description': '==============\nFile Converter\n==============\n\nConverts files from CSV to JSON formats and vice-versa.\n\nThis is meant to be used as the final project for the Python course from the Artificial Intelligence program at PUC Minas.\n\nIt has nothing groundbreaking, so you should safely ignore it. In any case, if you managed to get here, feel free to check my other (hopefully) more useful projects:\n\n- `Python TSP <https://github.com/fillipe-gsm/python-tsp>`_: a TSP solver;\n- `Python Kanban <https://github.com/fillipe-gsm/python-kanban>`_: a Kanban board for the command line.\n\nInstallation\n============\n\n.. code:: bash\n\n  pip install file-converter-fgsm\n\nThis assumes you are inside a virtual environment. If you wish to install it globally on the system (which I do not recommend for this class project), add ``sudo`` at the beginning.\n\nUsage\n=====\n\nOnce installed, a ``file_converter`` command becomes available.\n\nType\n\n.. code:: bash\n\n  file_converter --help\n\nto get further help.\n\nExamples\n========\n\nConverting a single file\n------------------------\n\nSuppose you have a file ``sample_file.csv`` in the current directory with the contents\n\n.. code:: csv\n\n  header1,header2,header3\n  1,"a",1.5\n  2,"b",3.2\n\nTo convert it into a ``json`` format, run\n\n.. code:: bash\n\n  file_converter --conversion=csv2json --input_path=./sample_file.csv\n\nand then you should have a ``sample_file.json`` in the same directory with the contents:\n\n.. code:: json\n\n  [\n      {\n          "header1": 1,\n          "header2": "\\"a\\"",\n          "header3": 1.5\n      },\n      {\n          "header1": 2,\n          "header2": "\\"b\\"",\n          "header3": 3.2\n      }\n  ]\n\n\nNotice how the quotes have been escaped.\n\nThe previous command is short for\n\n.. code:: bash\n\n  file_converter --conversion=csv2json --input_path=./sample_file.csv --output_path=. --separator=, --prefix=""\n\nExperiment running again but with a different ``--output_path``.\n\nThe command supports the other way for the conversion as well. To test that, let us convert the recently converted ``json`` file but prefixing the resulting file name with a ``new_``:\n\n.. code:: bash\n\n  file_converter --conversion=json2csv --input_path=./sample_file.json --prefix="new_"\n\nNotice the ``csv2json`` became ``json2csv`` in the ``--conversion`` attribute. Also, we should have a ``new_sample_file.csv`` with the same contents of the first.\n\nConverting all files in a folder\n--------------------------------\n\nIf instead of a single file path you pass a folder in the ``--input_path`` parameter, the command will attempt to convert all files inside of it. Notice they all should have the same separator.\n\nExperiment passing the current directory like\n\n\n.. code:: bash\n\n  file_converter --conversion=csv2json --input_path=. --prefix="from_folder_"\n\nIf you followed the previous example, you should have two new ``json`` files starting with ``from_folder_``.\n',
    'author': 'Fillipe Goulart',
    'author_email': 'fillipe.gsm@tutanota.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fillipe-gsm/file-converter-puc-ia',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
