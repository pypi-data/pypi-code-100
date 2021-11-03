# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['safety_road_mapping']

package_data = \
{'': ['*'],
 'safety_road_mapping': ['examples/*',
                         'extract_data/*',
                         'extract_data/data/.gitignore',
                         'maps/*']}

install_requires = \
['Unidecode>=1.2.0,<2.0.0',
 'colour>=0.1.5,<0.2.0',
 'folium>=0.12.1,<0.13.0',
 'geopy>=2.2.0,<3.0.0',
 'openrouteservice>=2.3.3,<3.0.0',
 'pandas>=1.3.2,<2.0.0',
 'patool>=1.12,<2.0',
 'plotly>=5.2.2,<6.0.0',
 'python-dotenv>=0.19.0,<0.20.0',
 'typeguard>=2.12.1,<3.0.0',
 'typing-extensions>=3.10.0,<4.0.0']

setup_kwargs = {
    'name': 'safety-road-mapping',
    'version': '0.1.7',
    'description': 'Module to generate a safety score for brazilian roads.',
    'long_description': "# General Instructions\n\n## Generating API token\n\nThis project uses [openrouteservice API](https://openrouteservice.org) to plot maps and routes.\nSo the following steps are necessary at first:\n\n1. Sign up on [openrouteservice.org](https://openrouteservice.org/dev/#/signup) to generate an API token;\n2. Create a `.env` file with the following content: `TOKEN=XXXXXXXXXXXXXXX`, where `XXXXXXXXXXXXXXX` is the token generated in the step before;\n3. Install the lib: `pip install safety-road-mapping`\n4. Get the road accidents according the instructions bellow: [Getting accident road data](#getting-accident-road-data)\n5. See the documentation on: [safety documentation](docs/safety_road_mapping/safety.md)\n6. See the examples on how to use the lib on: [how-to-use.ipynb](./safety_road_mapping/examples/how-to-use.ipynb)\n\n## Getting accident road data\n\n- The accidents data used were extracted from the [Polícia Rodoviária Federal website](https://www.gov.br/prf/pt-br).\n- The notebook [get_data.ipynb](./safety_road_mapping/extract_data/get_data.ipynb) is responsible to download and extract the data used.\n- If you want to directly download the files you can [click here](https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-acidentes).\n- To consolidate all the accidents by year on an unique `.csv` file use the notebook [consolidate_data.ipynb](./safety_road_mapping/extract_data/consolidate_data.ipynb).\n- For a simple explore data analysis from the data look at [eda_accidents.ipynb](./safety_road_mapping/extract_data/eda_accidents.ipynb)\n\n### Adding São Paulo data\n\n- Access the [infosiga website](http://www.respeitoavida.sp.gov.br/relatorios/)\n- Download the xlsx file with fatal accidents: [Fatal accidents](http://painelderesultados.infosiga.sp.gov.br/bases/acidentes_fatais.xlsx)\n- Download the csv file with non fatal accidents: [Non-fatal accidents](http://painelderesultados.infosiga.sp.gov.br/bases/acidentes_naofatais.csv)\n- Use the notebook [treat_data_from_SP.ipynb](./safety_road_mapping/extract_data/treat_data_from_SP.ipynb) to transform and concatenate the data generating a final file that will be used as input for the safety map code.\n\n## Other possible steps on the project\n\n- The accidents data used comes just from road federal police source, so there are some routes that don't receive score because they are state highways.\n- Create some unit tests.\n- Use [Renaest](https://www.gov.br/infraestrutura/pt-br/assuntos/transito/arquivos-denatran/docs/renaest) data (currently only [SP has geolocation data](http://www.infosiga.sp.gov.br)).\n- Include other variables in the score calculation.\n- Include driver behaviors data.\n- Implement an algorithm to predict accidents.\n- The routes subsections are not connected, once they are plotted individually in the map. Visually it can be interesting to connect them. (Is it possible or necessary?).\n",
    'author': 'Gabriel Aparecido Fonseca',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cervejaria-ambev/safety_road_mapping',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
