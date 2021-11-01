# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gabriel_puc_csv_converter', 'gabriel_puc_csv_converter._tests']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['converter = gabriel_puc_csv_converter.main:converter']}

setup_kwargs = {
    'name': 'gabriel-puc-csv-converter',
    'version': '0.2.0',
    'description': 'Convert csv to json. Publishing only for learning purposes at PUC.',
    'long_description': "# File Converter\n\n- CSV para conversor JSON.\n- JSON para conversor CSV.\n\n## Introdução\n\n### O que este projeto pode fazer\n\n- Leia um arquivo **csv** ou uma **pasta** com csv's e converta-os em **JSON**.\n- Leia um arquivo **json** ou uma **pasta** com json's e converta-os em **CSV**.\n\nEste projeto é um programa em execução no terminal, de preferência instalado com pipx:\n\n`` `bash\npipx install gabriel-puc-csv-converter\n`` `\n\nPara usar, basta digitar:\n\n`` `bash\n$ converter --help\n`` `\n\nIsso listará todas as opções disponíveis.\n\n`` `\nUsage: converter [OPTIONS] {csv|json}\n\n  Convert Single file or list of CSV files to json or json to convert json\n  files to csv.\n\nOptions:\n  -i, --input TEXT            Path where the files will be loaded for conversion.\n  -o, --output TEXT           Path where the converted files will be saved.\n  -d, --delimiter [,|;|:|\\t]  Separator used to split the files.\n  -p, --prefix TEXT           Prefix used to prepend to the name of the converted\n                            file saved on disk. The suffix will be a number\n                            starting from 0. ge: file_0.json.\n  --help                      Show this message and exit.\n`` `\n",
    'author': 'Gabriel Vargas',
    'author_email': 'gabrielvargas@usp.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gabgovar/csv_converter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
